#!/usr/bin/env python3
# Copyright (C) 2026 SpacemiT (Hangzhou) Technology Co. Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import json
import os
import pathlib
import re
import subprocess
import sys


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / "skills"

BASE_SKILLS = {
    "spacemit-robot-shared",
    "spacemit-robot-sdk-bootstrap",
    "spacemit-robot-remote",
    "spacemit-robot-build",
    "spacemit-robot-sync",
}

COMPONENT_SKILLS = {
    "spacemit-robot-speech": (
        "components/multimedia/audio",
        "components/model_zoo/asr",
        "components/model_zoo/vad",
        "components/model_zoo/tts",
        "components/model_zoo/voiceprint",
        "components/multimedia/audio_process/doa",
    ),
    "spacemit-robot-llm": ("components/model_zoo/llm",),
    "spacemit-robot-lerobot-onnx-inference": ("components/thirdparty/lerobot/examples/onnx_inference",),
    "spacemit-robot-grasp": ("components/control/grasp",),
    "spacemit-robot-manipulator": ("components/control/manipulator",),
    "spacemit-robot-lerobot-app": ("application/native/lerobot_app",),
}

BASE_REFERENCES = (
    "spacemit-robot-shared",
    "spacemit-robot-build",
    "spacemit-robot-remote",
    "spacemit-robot-sync",
)

INSTALL_METADATA = (
    "skills.sh.json",
    ".codex-plugin/plugin.json",
    ".claude-plugin/plugin.json",
    ".cursor-plugin/plugin.json",
)


def fail(message: str) -> None:
    print(f"ASSERTION FAILED: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_json(path: pathlib.Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        fail(f"{path}: failed to parse JSON: {exc}")


def parse_frontmatter(path: pathlib.Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(f"{path}: missing YAML frontmatter")
    try:
        _, frontmatter, body = text.split("---", 2)
    except ValueError:
        fail(f"{path}: malformed YAML frontmatter")
    meta = parse_skill_frontmatter(frontmatter, path)
    return meta, body


def parse_skill_frontmatter(frontmatter: str, path: pathlib.Path) -> dict:
    meta: dict = {"metadata": {"sdk": {"module_paths": [], "primary_docs": []}}}
    current_list: str | None = None

    for raw_line in frontmatter.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped:
            continue
        if line.startswith("name:"):
            meta["name"] = stripped.removeprefix("name:").strip().strip('"')
            current_list = None
        elif line.startswith("description:"):
            meta["description"] = stripped.removeprefix("description:").strip().strip('"')
            current_list = None
        elif stripped == "module_paths:":
            current_list = "module_paths"
        elif stripped == "primary_docs:":
            current_list = "primary_docs"
        elif stripped.startswith("build_hint:"):
            meta["metadata"]["sdk"]["build_hint"] = stripped.removeprefix("build_hint:").strip()
            current_list = None
        elif stripped.startswith("- ") and current_list:
            meta["metadata"]["sdk"][current_list].append(stripped.removeprefix("- ").strip())

    if "name" not in meta or "description" not in meta:
        fail(f"{path}: frontmatter must contain name and description")
    return meta


def local_skill_paths() -> list[pathlib.Path]:
    paths = sorted(SKILLS_ROOT.glob("*/SKILL.md"))
    if not paths:
        fail("skills/ must contain local SKILL.md files")
    return paths


def skill_map_entries() -> dict[str, dict]:
    entries: dict[str, dict] = {}
    current: dict | None = None
    current_list: str | None = None
    path = REPO_ROOT / "config" / "skill-map.yaml"
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped == "skills:":
            continue
        if line.startswith("  - name:"):
            name = stripped.removeprefix("- name:").strip()
            current = {"name": name, "primary_docs": []}
            entries[name] = current
            current_list = None
        elif current is not None and stripped.startswith("category:"):
            current["category"] = stripped.removeprefix("category:").strip()
            current_list = None
        elif current is not None and stripped == "primary_docs:":
            current_list = "primary_docs"
        elif current is not None and current_list == "primary_docs" and stripped.startswith("- "):
            current["primary_docs"].append(stripped.removeprefix("- ").strip())
    if not entries:
        fail("config/skill-map.yaml must contain a skills list")
    for name, entry in entries.items():
        if not entry.get("category"):
            fail(f"config/skill-map.yaml entry missing category: {name}")
    return entries


def assert_frontmatter_and_map() -> None:
    entries = skill_map_entries()
    skill_names = {path.parent.name for path in local_skill_paths()}

    if set(entries) != skill_names:
        missing = sorted(skill_names - set(entries))
        stale = sorted(set(entries) - skill_names)
        fail(f"skill-map mismatch; missing={missing}, stale={stale}")

    for skill_path in local_skill_paths():
        expected_name = skill_path.parent.name
        meta, _body = parse_frontmatter(skill_path)
        if meta.get("name") != expected_name:
            fail(f"{skill_path}: frontmatter name must match directory name")
        if not isinstance(meta.get("description"), str) or not meta["description"].strip():
            fail(f"{skill_path}: description must not be empty")

    for name in BASE_SKILLS:
        if name not in skill_names:
            fail(f"{name}: required base skill is missing")


def assert_component_contracts() -> None:
    entries = skill_map_entries()
    for name, module_paths_expected in COMPONENT_SKILLS.items():
        skill_path = SKILLS_ROOT / name / "SKILL.md"
        if not skill_path.exists():
            fail(f"{name}: SKILL.md is missing")

        entry = entries.get(name)
        expected_category = "application" if name == "spacemit-robot-lerobot-app" else "components"
        if entry is None or entry.get("category") != expected_category:
            fail(f"{name}: skill-map category must be {expected_category}")

        meta, body = parse_frontmatter(skill_path)
        sdk_meta = (meta.get("metadata") or {}).get("sdk") or {}
        module_paths = sdk_meta.get("module_paths") or []
        for module_path in module_paths_expected:
            if module_path not in module_paths:
                fail(f"{name}: metadata.sdk.module_paths must include {module_path}")
        if not sdk_meta.get("build_hint"):
            fail(f"{name}: metadata.sdk.build_hint is required")


def assert_skill_reference_links() -> None:
    reference_pattern = re.compile(r"references/[A-Za-z0-9_.-]+\.md")
    for skill_path in local_skill_paths():
        _meta, body = parse_frontmatter(skill_path)
        for rel in sorted(set(reference_pattern.findall(body))):
            target = skill_path.parent / rel
            if not target.exists():
                fail(f"{skill_path}: referenced file is missing: {rel}")


def assert_sdk_root_variable_rules() -> None:
    legacy_root_var = "SPACEMIT" + "_SDK_ROOT"
    for skill_path in sorted(SKILLS_ROOT.glob("*/SKILL.md")):
        text = skill_path.read_text(encoding="utf-8")
        if legacy_root_var in text:
            fail(f"{skill_path}: SDK root variable must be SROBOTIS_ROOT only")


def assert_module_skill_template_rules() -> None:
    old_template = REPO_ROOT / "docs" / "reference-template.md"
    if old_template.exists():
        fail("docs/reference-template.md must be replaced by docs/module-skill-template.md")

    template = REPO_ROOT / "docs" / "module-skill-template.md"
    if not template.exists():
        fail("docs/module-skill-template.md: module skill template is missing")
    text = template.read_text(encoding="utf-8")
    if "SDK-relative" not in text:
        fail("docs/module-skill-template.md must require SDK-relative reference paths")
    for token in (
        "`SKILL.md` 是主入口",
        "不把 `product.md`、`overview.md` 作为标准文件",
        "References 设计",
        "Scripts 设计",
        "编写检查清单",
        "`scripts/` 是可选资源",
        "搭建环境",
        "跑通示例",
        "调用 API 做应用",
        "跑性能数据",
    ):
        if token not in text:
            fail(f"docs/module-skill-template.md must document: {token}")
    forbidden_heading_tokens = (
        "Product Knowledge Layer",
        "User Development Loop",
        "Recommended Layout",
        "Standard References",
        "Minimal Profiles",
        "How to List References",
        "File Template",
        "Writing Checklist",
        "Set up the environment",
        "Run examples",
        "Build an application with APIs",
        "Produce performance data",
    )
    for token in forbidden_heading_tokens:
        if token in text:
            fail(f"docs/module-skill-template.md must use Chinese wording instead of: {token}")
    forbidden_reference_tokens = (
        "references/product.md",
        "references/overview.md",
        "references/environment.md",
        "references/build.md",
        "references/runtime.md",
        "references/configuration.md",
        "references/data-io.md",
        "references/models.md",
        "references/hardware.md",
        "references/deploy-sync.md",
        "references/testing.md",
        "references/safety.md",
        "references/compatibility.md",
        "evals/",
        "`evals/`",
    )
    for token in forbidden_reference_tokens:
        if token in text:
            fail(f"docs/module-skill-template.md: {token} must not be a standard reference dimension")

    forbidden = ('cd "$SROBOTIS_ROOT"', "cd '$SROBOTIS_ROOT'", 'cd "$SROBOTIS_REMOTE_ROOT"')
    for token in forbidden:
        if token in text:
            fail(f"docs/module-skill-template.md must not hardcode execution root: {token}")


def assert_base_skill_contracts() -> None:
    build_text = (SKILLS_ROOT / "spacemit-robot-build" / "SKILL.md").read_text(encoding="utf-8")
    remote_text = (SKILLS_ROOT / "spacemit-robot-remote" / "SKILL.md").read_text(encoding="utf-8")
    sync_text = (SKILLS_ROOT / "spacemit-robot-sync" / "SKILL.md").read_text(encoding="utf-8")
    shared_text = (SKILLS_ROOT / "spacemit-robot-shared" / "SKILL.md").read_text(encoding="utf-8")
    bootstrap_text = (SKILLS_ROOT / "spacemit-robot-sdk-bootstrap" / "SKILL.md").read_text(encoding="utf-8")
    sync_script_text = (SKILLS_ROOT / "spacemit-robot-sync" / "scripts" / "srobotis_sync.mjs").read_text(
        encoding="utf-8"
    )

    for mode in ("local", "remote", "hybrid"):
        if mode not in shared_text:
            fail(f"spacemit-robot-shared must document mode: {mode}")
    if "python3" in remote_text.lower() or "srobotis_exec" in remote_text:
        fail("spacemit-robot-remote must not require a Python helper")
    if "node " not in sync_text or "srobotis_sync.mjs" not in sync_text:
        fail("spacemit-robot-sync must document the Node.js sync helper")
    for text, label in (
        (shared_text, "spacemit-robot-shared"),
        (bootstrap_text, "spacemit-robot-sdk-bootstrap"),
        (sync_text, "spacemit-robot-sync"),
        (sync_script_text, "srobotis_sync.mjs"),
    ):
        if "workspace/spacemit-robot" not in text:
            fail(f"{label}: hybrid PC SDK default path must be documented")
    for token in ("envsetup.sh", "lunch", "mm"):
        if token not in build_text:
            fail(f"spacemit-robot-build must cover {token}")


def assert_install_metadata() -> None:
    for rel in INSTALL_METADATA:
        path = REPO_ROOT / rel
        if not path.exists():
            fail(f"{rel}: install metadata is missing")
        load_json(path)

    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    zh_readme_path = REPO_ROOT / "README.zh-CN.md"
    if not zh_readme_path.exists():
        fail("README.zh-CN.md: Chinese README is missing")
    zh_readme = zh_readme_path.read_text(encoding="utf-8")
    if "[简体中文](README.zh-CN.md)" not in readme:
        fail("README.md must link to README.zh-CN.md")
    if "[English](README.md)" not in zh_readme:
        fail("README.zh-CN.md must link back to README.md")

    for command in (
        "npx skills add spacemit-robotics/robot-skills --agent codex",
        "npx skills add spacemit-robotics/robot-skills --agent claude-code",
        "npx skills add spacemit-robotics/robot-skills --agent cursor",
    ):
        if command not in readme:
            fail(f"README.md missing install command: {command}")
        if command not in zh_readme:
            fail(f"README.zh-CN.md missing install command: {command}")

    catalog = load_json(REPO_ROOT / "skills.sh.json")
    catalog_text = json.dumps(catalog, ensure_ascii=False)
    for skill_path in local_skill_paths():
        name = skill_path.parent.name
        if name not in catalog_text:
            fail(f"skills.sh.json missing skill: {name}")


def assert_runtime_helpers() -> None:
    remote_script_dir = SKILLS_ROOT / "spacemit-robot-remote" / "scripts"
    if remote_script_dir.exists() and list(remote_script_dir.glob("*")):
        fail("spacemit-robot-remote must stay script-free for Windows-friendly SSH usage")

    python_helpers = sorted(SKILLS_ROOT.glob("*/scripts/*.py"))
    if python_helpers:
        fail(f"runtime helpers must not require Python: {python_helpers}")

    sync_script = SKILLS_ROOT / "spacemit-robot-sync" / "scripts" / "srobotis_sync.mjs"
    if not sync_script.exists():
        fail(f"{sync_script}: required sync helper is missing")
    proc = subprocess.run(
        ["node", str(sync_script), "--help"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        fail(f"{sync_script}: --help failed: {proc.stderr or proc.stdout}")


def assert_sync_rejects_unsafe_paths() -> None:
    script = SKILLS_ROOT / "spacemit-robot-sync" / "scripts" / "srobotis_sync.mjs"
    bad_paths = ("/abs", "../bad", ".repo", "foo/.git/bar", "output", "foo/../bar", r"C:\sdk\file")
    for bad_path in bad_paths:
        proc = subprocess.run(
            ["node", str(script), "--path", bad_path, "--dry-run"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if proc.returncode == 0:
            fail(f"srobotis_sync.mjs should reject unsafe path: {bad_path}")
        if "ERROR:" not in proc.stderr:
            fail(f"srobotis_sync.mjs unsafe path error should be explicit: {bad_path}")


def assert_primary_docs_if_sdk_available() -> None:
    sdk_root = os.environ.get("SROBOTIS_ROOT")
    if not sdk_root:
        return
    root = pathlib.Path(sdk_root).expanduser().resolve()
    if not root.exists():
        return
    for name, entry in skill_map_entries().items():
        for doc in entry.get("primary_docs") or []:
            if not (root / doc).exists():
                fail(f"{name}: primary doc does not exist under SROBOTIS_ROOT: {doc}")


def main() -> int:
    checks = (
        assert_frontmatter_and_map,
        assert_component_contracts,
        assert_skill_reference_links,
        assert_sdk_root_variable_rules,
        assert_module_skill_template_rules,
        assert_base_skill_contracts,
        assert_install_metadata,
        assert_runtime_helpers,
        assert_sync_rejects_unsafe_paths,
        assert_primary_docs_if_sdk_available,
    )
    for check in checks:
        check()
    print("PASS robot-skills contract")
    return 0


def test_robot_skills_contract() -> None:
    main()


if __name__ == "__main__":
    raise SystemExit(main())
