# Skill 编写说明

新建 skill 可参考 `../skill-template/skill-template.md`。

## Rules

- 运行时 agent 只会看到安装后的 `SKILL.md`；必须遵守的规则只能写进 `skills/`。
- 正文尽量短；三模式、SDK root、target、构建和同步规则归入基础 skill。
- 在 `../config/skill-map.yaml` 登记 `name`、`category`、`primary_docs`。
- Frontmatter 必填：`name`、`description`；组件建议声明 `metadata.sdk.module_paths`、`primary_docs`、`build_hint`。
- SDK root 环境变量只使用 `SROBOTIS_ROOT`。
- 组件 skill 不写死 SSH 命令、host、target、board 或用户路径。
- 组件 skill 只声明模块路径、构建倾向、文档入口和专项注意事项。
- 组件 skill 需要执行命令时引用 `spacemit-robot-shared`、`spacemit-robot-build`、`spacemit-robot-remote`、`spacemit-robot-sync`。
- 日常开发验证不默认调用 `robot-test`；只有 CI、回归验证或用户明确要求时才使用。
- `primary_docs` 是按需回源索引，不是每次请求的固定前置阅读列表。
- 运行时 helper 不应要求用户额外安装 Python；能写成规则就写成规则，需要脚本时优先使用 Node.js，因为安装流程已经依赖 `npx`/npm。

## Recommended Structure

- `shared`: 三模式、配置优先级、SDK root、target、路由。
- `bootstrap`: 首次初始化、依赖、repo init/sync、SDK root 验证。
- `remote`: SSH 检查、远程 SDK root 检查、远程命令执行。
- `build`: `envsetup.sh`、`lunch`、`m`、`mm` 的构建决策。
- `sync`: hybrid 单向同步、dry-run、路径保护、repo preflight。
- 组件 skill: `Contract`、`Workflow`、`Notes`。

## Directory

```text
robot-skills/skills/<skill-name>/
├── SKILL.md
└── scripts/      # 可选；脆弱或重复的操作放脚本
```
