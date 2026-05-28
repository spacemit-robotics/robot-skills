#!/usr/bin/env python3
# Copyright (C) 2026 SpacemiT (Hangzhou) Technology Co. Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os
import pathlib
import sys

import yaml


REQUIRED_SKILLS = {
    "spacemit-robot-asr": "components/model_zoo/asr",
    "spacemit-robot-tts": "components/model_zoo/tts",
    "spacemit-robot-audio": "components/multimedia/audio",
    "spacemit-robot-doa": "components/multimedia/audio_process/doa",
    "spacemit-robot-voiceprint": "components/model_zoo/voiceprint",
}


def fail(message: str) -> None:
    print(f"ASSERTION FAILED: {message}", file=sys.stderr)
    raise SystemExit(1)


def sdk_root() -> pathlib.Path:
    if os.environ.get("SROBOTIS_ROOT"):
        return pathlib.Path(os.environ["SROBOTIS_ROOT"]).resolve()
    return pathlib.Path(__file__).resolve().parents[2]


def load_yaml(path: pathlib.Path) -> object:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        fail(f"{path}: failed to parse YAML: {exc}")


def parse_frontmatter(path: pathlib.Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(f"{path}: missing YAML frontmatter")
    try:
        _, frontmatter, body = text.split("---", 2)
    except ValueError:
        fail(f"{path}: malformed YAML frontmatter")
    meta = yaml.safe_load(frontmatter)
    if not isinstance(meta, dict):
        fail(f"{path}: frontmatter must be a mapping")
    return meta, body


def main() -> int:
    root = sdk_root()
    skills_root = root / "robot-skills"
    skill_map_path = skills_root / "config" / "skill-map.yaml"
    skill_map = load_yaml(skill_map_path)
    if not isinstance(skill_map, dict) or not isinstance(skill_map.get("skills"), list):
        fail("config/skill-map.yaml must contain a skills list")

    map_entries = {
        item.get("name"): item for item in skill_map["skills"] if isinstance(item, dict)
    }

    local_skill_paths = sorted((skills_root / "skills").glob("*/SKILL.md"))
    if not local_skill_paths:
        fail("robot-skills must contain local SKILL.md files")

    for skill_path in local_skill_paths:
        expected_name = skill_path.parent.name
        meta, _body = parse_frontmatter(skill_path)
        if meta.get("name") != expected_name:
            fail(f"{skill_path}: frontmatter name must match directory name")
        if not meta.get("description"):
            fail(f"{skill_path}: description must not be empty")
        if expected_name not in map_entries:
            fail(f"{skill_path}: local skill must be registered in skill-map.yaml")

    for name, module_path in REQUIRED_SKILLS.items():
        skill_path = skills_root / "skills" / name / "SKILL.md"
        if not skill_path.exists():
            fail(f"{name}: SKILL.md is missing")

        entry = map_entries.get(name)
        if entry is None:
            fail(f"{name}: missing skill-map entry")
        if entry.get("category") != "components":
            fail(f"{name}: skill-map category must be components")

        meta, body = parse_frontmatter(skill_path)
        sdk_meta = (meta.get("metadata") or {}).get("sdk") or {}
        module_paths = sdk_meta.get("module_paths") or []
        if module_path not in module_paths:
            fail(f"{name}: metadata.sdk.module_paths must include {module_path}")

        for doc in entry.get("primary_docs") or []:
            if not (root / doc).exists():
                fail(f"{name}: primary doc does not exist: {doc}")

        text = skill_path.read_text(encoding="utf-8")
        list_cmd = f"scripts/test/robot-test list {module_path}"
        run_cmd = f"scripts/test/robot-test run {module_path} --scope pr"
        if list_cmd not in text and f"./{list_cmd}" not in text:
            fail(f"{name}: missing robot-test list command for {module_path}")
        if run_cmd not in text and f"./{run_cmd}" not in text:
            fail(f"{name}: missing robot-test run --scope pr command for {module_path}")
        if "必须真实执行命令" not in body:
            fail(f"{name}: skill must require agents to execute requested commands")
        if "k3-com260-minimal" in text or "codex/" in text:
            fail(f"{name}: skill must not hard-code targets or codex branch names")

    print("PASS robot-skills contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
