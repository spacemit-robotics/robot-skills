# Skill 编写说明

新建 skill 可参考 `../skill-template/skill-template.md`。

## 规则

- 运行时 agent 只会看到 `skills/` 下安装后的 `SKILL.md`；因此运行时必须遵守的规则只能写进 `skills/`，不能只写在模板、`docs/` 或仓库说明里。
- 正文尽量短；重复内容归入 `spacemit-robot-shared` 或仅引用 SDK 文档路径。
- 在 `../config/skill-map.yaml` 登记 `name`、`category`、`primary_docs`（相对 SDK 根）。
- Frontmatter 必填：`name`、`description`；建议 `metadata.requires.bins`。
- 若该 skill 的构建倾向与 shared 默认推导不同，显式声明 `metadata.sdk.build_hint`。
- 专项 skill 不直接写死 `k1-*` 或 `k3-*` target 名；当需要 target 时，只说明“先解析 board，再显式选择 target”。
- 专项 skill 应把本模块最关键的 SDK 文档写进 `primary_docs`，但它们是按需回源资料，不是默认前置阅读。
- 正文优先写清“先做什么命令、失败时再回读什么文档”，不要默认要求每次都先读仓库级或组件级 README。
- 模板文件只是作者脚手架，章节顺序和表述应镜像运行时 skill，而不是额外新增运行时语义。

## 推荐结构

- `shared`：只保留全局规则与路由，例如读取优先级、SDK 根、`build_hint`、target 选择。
- `bootstrap`：只保留首次拉取与初始化，例如依赖、`repo init/sync`、导出 `SPACEMIT_SDK_ROOT`、验证目录。
- 专项 skill：统一优先使用以下章节：`何时使用`、`默认规则`、`固定流程`、`专项任务`、`禁止事项`、`常见任务与命令`。

## 目录

```text
robot-skills/skills/<skill-name>/
├── SKILL.md
└── references/     # 可选；仅当正文仍需拆出时才加
```
