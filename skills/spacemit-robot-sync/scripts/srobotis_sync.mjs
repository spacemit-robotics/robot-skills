#!/usr/bin/env node
// Copyright (C) 2026 SpacemiT (Hangzhou) Technology Co. Ltd.
// SPDX-License-Identifier: Apache-2.0

import { spawnSync } from "node:child_process";
import { existsSync, readFileSync, statSync } from "node:fs";
import { homedir } from "node:os";
import { join, resolve } from "node:path";
import process from "node:process";

const defaultPcSdkRoot = join(homedir(), "workspace", "spacemit-robot");
const protectedParts = new Set([".repo", ".git", "output", "out", ".cache", "__pycache__"]);
const rsyncExcludes = [
  ".repo/",
  ".git/",
  "output/",
  "out/",
  ".cache/",
  "__pycache__/",
  "*.log",
  "*.tmp",
  "*.o",
  "*.a",
  "*.so",
  "*.pyc",
];

function usage() {
  console.log(`Usage: srobotis_sync.mjs --path <relative-sdk-path> [options]

Dry-run or apply one-way hybrid sync from a PC SDK to a board SDK.

Options:
  --local-root <path>    PC SDK root. Defaults to SROBOTIS_ROOT, then ~/workspace/spacemit-robot.
  --remote <user@host>   Board SSH target. Defaults to SROBOTIS_REMOTE.
  --remote-root <path>   Board SDK root. Defaults to SROBOTIS_REMOTE_ROOT.
  --path <path>          Relative SDK path to sync. Repeatable.
  --dry-run              Validate and print the plan without copying. Default.
  --apply                Actually copy files to the board.
  -h, --help             Show this help message.
`);
}

function parseArgs(argv) {
  const args = {
    localRoot: process.env.SROBOTIS_ROOT || defaultPcSdkRoot,
    remote: process.env.SROBOTIS_REMOTE,
    remoteRoot: process.env.SROBOTIS_REMOTE_ROOT,
    paths: [],
    dryRun: false,
    apply: false,
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "-h" || arg === "--help") {
      args.help = true;
    } else if (arg === "--local-root") {
      args.localRoot = argv[++index];
    } else if (arg === "--remote") {
      args.remote = argv[++index];
    } else if (arg === "--remote-root") {
      args.remoteRoot = argv[++index];
    } else if (arg === "--path") {
      args.paths.push(argv[++index]);
    } else if (arg === "--dry-run") {
      args.dryRun = true;
    } else if (arg === "--apply") {
      args.apply = true;
    } else {
      throw new Error(`unknown argument: ${arg}`);
    }
  }

  if (!args.apply) {
    args.dryRun = true;
  }
  return args;
}

function rejectPath(raw) {
  if (!raw) {
    throw new Error("empty path is not allowed");
  }
  if (raw.includes("\\")) {
    throw new Error(`use POSIX-style SDK paths with '/': ${raw}`);
  }
  if (/^[A-Za-z]:/.test(raw)) {
    throw new Error(`Windows drive paths are not allowed: ${raw}`);
  }
  if (raw.startsWith("/")) {
    throw new Error(`absolute path is not allowed: ${raw}`);
  }

  const parts = raw.split("/");
  for (const part of parts) {
    if (part === "" || part === "." || part === "..") {
      throw new Error(`path must be a clean relative path: ${raw}`);
    }
    if (protectedParts.has(part)) {
      throw new Error(`path touches protected directory ${part}: ${raw}`);
    }
  }
  return parts.join("/");
}

function loadProjectList(localRoot) {
  if (!localRoot) {
    return [];
  }
  const projectList = join(localRoot, ".repo", "project.list");
  if (!existsSync(projectList)) {
    return [];
  }
  return readFileSync(projectList, "utf8")
    .split(/\r?\n/)
    .map((line) => line.trim().replace(/\/$/, ""))
    .filter(Boolean);
}

function mappedProject(relPath, projects) {
  const candidates = projects.filter((project) => relPath === project || relPath.startsWith(`${project}/`));
  candidates.sort((left, right) => right.length - left.length);
  return candidates[0] ?? null;
}

function shellQuote(value) {
  return `'${String(value).replace(/'/g, "'\\''")}'`;
}

function ensureCommand(name) {
  const probe = spawnSync(name, ["--version"], { encoding: "utf8" });
  if (probe.error) {
    throw new Error(`${name} is required for --apply but was not found on PATH`);
  }
}

function remoteDirty(remote, remoteRoot, project) {
  const shell = [
    `cd ${shellQuote(remoteRoot)}`,
    `test -d ${shellQuote(project)}`,
    `cd ${shellQuote(project)}`,
    "(git rev-parse --is-inside-work-tree >/dev/null 2>&1 && git status --short || true)",
  ].join(" && ");
  const proc = spawnSync("ssh", [remote, `bash -lc ${shellQuote(shell)}`], { encoding: "utf8" });
  if (proc.status !== 0) {
    throw new Error(proc.stderr.trim() || proc.stdout.trim() || "remote dirty check failed");
  }
  return proc.stdout.trim();
}

function rsyncPath(localRoot, remote, remoteRoot, relPath) {
  const source = join(localRoot, relPath);
  if (!existsSync(source)) {
    throw new Error(`local path does not exist: ${source}`);
  }

  const relParts = relPath.split("/");
  const parent = relParts.slice(0, -1).join("/");
  const remoteParent = parent ? `${remoteRoot}/${parent}` : remoteRoot;
  console.error(`+ ssh ${remote} mkdir -p ${shellQuote(remoteParent)}`);
  const mkdir = spawnSync("ssh", [remote, "mkdir", "-p", remoteParent], { stdio: "inherit" });
  if (mkdir.status !== 0) {
    return mkdir.status ?? 1;
  }

  const rsyncArgs = ["-az"];
  for (const pattern of rsyncExcludes) {
    rsyncArgs.push("--exclude", pattern);
  }

  const isDirectory = statSync(source).isDirectory();
  if (isDirectory) {
    rsyncArgs.push(`${source}/`, `${remote}:${remoteRoot}/${relPath}/`);
  } else {
    rsyncArgs.push(source, `${remote}:${remoteRoot}/${relPath}`);
  }

  console.error(`+ rsync ${rsyncArgs.map(shellQuote).join(" ")}`);
  const proc = spawnSync("rsync", rsyncArgs, { stdio: "inherit" });
  return proc.status ?? 1;
}

function main() {
  let args;
  try {
    args = parseArgs(process.argv.slice(2));
  } catch (error) {
    console.error(`ERROR: ${error.message}`);
    return 2;
  }

  if (args.help) {
    usage();
    return 0;
  }
  if (args.dryRun && args.apply) {
    console.error("ERROR: --dry-run and --apply are mutually exclusive");
    return 2;
  }
  if (args.paths.length === 0) {
    console.error("ERROR: provide at least one --path");
    return 2;
  }

  let relPaths;
  try {
    relPaths = args.paths.map(rejectPath);
  } catch (error) {
    console.error(`ERROR: ${error.message}`);
    return 2;
  }

  const apply = args.apply;
  const localRoot = args.localRoot ? resolve(args.localRoot) : null;
  if (apply && !localRoot) {
    console.error("ERROR: --local-root or SROBOTIS_ROOT is required with --apply");
    return 2;
  }
  if (apply && !args.remote) {
    console.error("ERROR: --remote or SROBOTIS_REMOTE is required with --apply");
    return 2;
  }
  if (apply && !args.remoteRoot) {
    console.error("ERROR: --remote-root or SROBOTIS_REMOTE_ROOT is required with --apply");
    return 2;
  }

  const projects = loadProjectList(localRoot);
  const projectMap = relPaths.map((relPath) => [relPath, mappedProject(relPath, projects)]);

  console.log("SYNC PLAN");
  console.log(`mode: ${apply ? "apply" : "dry-run"}`);
  console.log(`local_root: ${localRoot ?? "<not provided>"}`);
  console.log(`remote: ${args.remote ?? "<not provided>"}`);
  console.log(`remote_root: ${args.remoteRoot ?? "<not provided>"}`);
  for (const [relPath, project] of projectMap) {
    console.log(`path: ${relPath}${project ? ` project=${project}` : ""}`);
  }

  if (!apply) {
    return 0;
  }

  try {
    ensureCommand("ssh");
    ensureCommand("rsync");
    for (const [relPath, project] of projectMap) {
      if (project) {
        const dirty = remoteDirty(args.remote, args.remoteRoot, project);
        if (dirty) {
          console.error(`ERROR: remote project has uncommitted changes: ${project}`);
          console.error(dirty);
          return 3;
        }
      }
      const rc = rsyncPath(localRoot, args.remote, args.remoteRoot, relPath);
      if (rc !== 0) {
        return rc;
      }
    }
  } catch (error) {
    console.error(`ERROR: ${error.message}`);
    return 2;
  }
  return 0;
}

process.exitCode = main();
