# robot-skills

[English](README.md) | 简体中文

SpacemiT Robot SDK 的 Agent skills 包，用于让 Codex、Claude Code、Cursor
等 coding agent 更好地安装、识别、远程访问和开发 `spacemit_robot` SDK。

## 安装

```bash
# Codex
npx skills add spacemit-robotics/robot-skills --agent codex

# Claude Code
npx skills add spacemit-robotics/robot-skills --agent claude-code

# Cursor
npx skills add spacemit-robotics/robot-skills --agent cursor
```

也可以在 agent 对话里给出仓库链接并要求安装：

```text
请安装 https://github.com/spacemit-robotics/robot-skills
```

## 使用

安装后，用户不需要手动运行某个 skill。打开 Codex、Claude Code、Cursor
或其他支持 skills 的 coding agent，直接用自然语言描述 SDK 开发任务即可。
agent 应该按需加载相关 skills，选择开发模式，检查 SDK；只有在板子、
SDK root、target 或同步范围不明确时再询问用户。

即使 SDK 还没有下载，也可以开始使用。首次接触时，先把板子 SSH 地址告诉
agent。agent 应该先检查连通性，再确认 PC 或板端是否已经存在 SDK，然后推荐
开发模式；任何依赖安装、`repo init`、`repo sync` 这类初始化动作都应该先询问用户。
如果使用 hybrid 模式，PC 本地 SDK 默认下载路径是 `~/workspace/spacemit-robot`。

已知时，建议告诉 agent 的信息：

| 信息 | 示例 |
| --- | --- |
| 板子 SSH 地址 | `如bianbu@10.0.90.29` |
| SDK 状态 | 还没下载、不确定、或已知路径 |
| 期望开发模式 | `local`、`remote` 或 `hybrid` |
| 板端 SDK 路径，已知时提供 | `/home/bianbu/spacemit_robot` |
| PC SDK 路径，hybrid 模式 | 默认 `~/workspace/spacemit-robot` |
| 模块或任务 | `components/model_zoo/asr`、`application/native/lerobot_app`、构建、调试、运行、查看日志 |

示例提示词：

```text
开发板的地址是：bianbu@10.0.90.29，我使用hybrid模式进行开发，请帮我搭建SDK环境。
```

环境搭建好后可继续询问
```text
帮我跑一下开发板上大模型的性能，然后把数据给我。
```

## 开发模式

| Mode | 场景 | SDK 位置 | 构建/运行位置 |
| --- | --- | --- | --- |
| `local` | Board local | 板端 | 板端 |
| `remote` | PC remote | 板端 | 板端，通过 SSH |
| `hybrid` | PC local edit + board build | PC 和板端各一份 | 修改在 PC，同步到板端后在板端构建/运行 |

Hybrid 不做交叉编译，不使用 PC Docker 构建目标产物。它只负责 PC 到板子的显式单向同步，然后在板端执行构建、运行和验证。

## Skill Catalog

本仓库是一个会持续增长的 skill catalog。只查看当前 skill 列表、不安装时，可以执行：

```bash
npx skills add spacemit-robotics/robot-skills --list
```

维护仓库时，`skills.sh.json` 是安装 catalog，`config/skill-map.yaml` 负责把 skill 映射到 SDK 模块和主要 SDK 文档。README 只保留安装方式和开发模式说明，这样新增 skill 时不需要同步修改 README。

## 目录结构

```text
robot-skills/
├── skills/              # 可安装的 SKILL.md，每个目录一个 skill
├── config/
│   └── skill-map.yaml   # skill 与 SDK 内 primary docs 索引
├── tests/               # skill contract 测试
├── docs/                # 编写约定和设计说明
├── skills.sh.json       # skills catalog
├── .codex-plugin/       # Codex 安装元数据
├── .claude-plugin/      # Claude Code 安装元数据
└── .cursor-plugin/      # Cursor 安装元数据
```
