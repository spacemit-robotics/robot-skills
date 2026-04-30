# robot-skills

供 Agent 使用的 SpacemiT Robot **静态 skill 包**（与 SDK 克隆目录相互独立）。

## 目录

```text
robot-skills/
├── skills/           # 可安装的 SKILL.md（每子目录一个 skill）
├── skill-template/   # 新建 skill 时可复制的模板
├── config/
│   └── skill-map.yaml   # skill 与 SDK 内 primary_docs 索引（路径相对 SDK 根）
└── docs/             # 命名、篇幅与编写约定
```

## Skills（当前仓库内）

| Skill | 作用 |
| ----- | ---- |
| `spacemit-robot-shared` | SDK 心智模型、`SPACEMIT_SDK_ROOT`、通用前置、路由 |
| `spacemit-robot-sdk-bootstrap` | 首次 `repo` 拉取、`envsetup`/`lunch`、导出根路径 |
| `spacemit-robot-llm` | `components/model_zoo/llm` 构建与运行入口 |

`skill-map.yaml` 中其余条目为预留或外置维护时与 SDK 文档对齐用。

## 设计要点

- **上下文**：`SKILL.md` 保持短正文；细节以 SDK 内 README / 头文件为准。
- **路径**：一律经 `$SPACEMIT_SDK_ROOT` 解析，勿假设 skill 与 SDK 的目录关系。
- **流程**：专项 skill 先判断 SDK 是否存在，再判断环境与构建状态，再检查运行前置，最后才执行测试并返回结果。
- **target 选择**：统一由 `spacemit-robot-shared` 定义规则；需要 target 时先解析当前机器 board，再显式选择 `lunch <target>`，不直接猜 `k1-*` 或 `k3-*` 方案名；同一 board 下若有多个 product 候选则先确认。
