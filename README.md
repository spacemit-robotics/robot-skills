# robot-skills

English | [简体中文](README.zh-CN.md)

Agent skills for the SpacemiT Robot SDK. This repository helps Codex,
Claude Code, Cursor, and other coding agents install the skills, discover the
SDK, access a development board remotely, and develop `spacemit_robot` modules.

## Install

```bash
# Codex
npx skills add spacemit-robotics/robot-skills --agent codex

# Claude Code
npx skills add spacemit-robotics/robot-skills --agent claude-code

# Cursor
npx skills add spacemit-robotics/robot-skills --agent cursor
```

You can also ask an agent to install from the repository URL:

```text
Please install https://github.com/spacemit-robotics/robot-skills
```

## Usage

After installation, you do not run a skill manually. Open Codex, Claude Code,
Cursor, or another supported coding agent and describe the SDK task in natural
language. The agent should load the relevant skills, choose a development mode,
inspect the SDK, and ask only when the board, SDK root, target, or sync scope is
still ambiguous.

You can start even if the SDK has not been downloaded yet. In that case, give
the agent the board SSH target first. The agent should check connectivity,
discover whether the SDK already exists on the board or PC, recommend a mode,
and ask before running dependency installation, `repo init`, or `repo sync`.
For hybrid mode, the default PC SDK checkout path is
`~/workspace/spacemit-robot`.

Useful information to give the agent, when known:

| Field | Example |
| --- | --- |
| Board SSH target | `for example, bianbu@10.0.90.29` |
| SDK status | not downloaded yet, unknown, or exists at a known path |
| Preferred mode | `local`, `remote`, or `hybrid` |
| Board SDK root, if known | `/home/bianbu/spacemit_robot` |
| PC SDK root, for hybrid mode | `~/workspace/spacemit-robot` by default |
| Module or task | `components/model_zoo/asr`, `application/native/lerobot_app`, build, debug, run, inspect logs |

Example prompts:

```text
The board address is bianbu@10.0.90.29. I want to use hybrid mode; please help me set up the SDK environment.
```

After the environment is ready, you can continue asking:

```text
Please run the LLM performance test on the development board and show me the data.
```

## Development Modes

| Mode | Scenario | SDK Location | Build / Run Location |
| --- | --- | --- | --- |
| `local` | Board local | Development board | Development board |
| `remote` | PC remote | Development board | Development board, through SSH |
| `hybrid` | PC local edit + board build | Both PC and development board | Edit on PC, sync to board, then build/run on board |

Hybrid mode does not cross-compile and does not build target artifacts through PC-side Docker. It only syncs explicit local changes from the PC to the board, then builds, runs, and validates on the board.

## Skill Catalog

This repository is a growing skill catalog. To inspect the current list without installing anything, run:

```bash
npx skills add spacemit-robotics/robot-skills --list
```

For repository maintenance, `skills.sh.json` is the install catalog and `config/skill-map.yaml` maps skills to SDK modules and primary SDK documents. Keep README focused on installation and workflow concepts so adding a new skill does not require editing this page.

## Repository Layout

```text
robot-skills/
├── skills/              # Installable SKILL.md files, one skill per directory
├── config/
│   └── skill-map.yaml   # Skill-to-SDK primary docs index
├── tests/               # Skill contract tests
├── docs/                # Authoring conventions and design notes
├── skills.sh.json       # Skills catalog
├── .codex-plugin/       # Codex plugin metadata
├── .claude-plugin/      # Claude Code plugin metadata
└── .cursor-plugin/      # Cursor plugin metadata
```
