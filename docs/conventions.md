# Skill 约定

## 命名

- 目录名与 frontmatter `name`：统一用 `spacemit-robot-` 前缀，小写与连字符。

## 篇幅与内容

- 运行时只以 `skills/` 下安装后的 `SKILL.md` 为准；`skill-template/` 与 `docs/` 只提供作者指导，不能承载额外的运行时关键规则。
- **短正文**：共享流程只写在 `spacemit-robot-shared`；专项 skill 只写本组件独有前置、检查顺序、意图→命令表；**不**大段复制 SDK README。
- 专项 skill 开篇链到 `spacemit-robot-shared`；需要时链到 `spacemit-robot-sdk-bootstrap`。
- 用 `$SPACEMIT_SDK_ROOT` 拼接 SDK 内路径；`skill-map.yaml` 的 `primary_docs` 为相对 SDK 根的索引。
- 默认先读 shared 与专项 skill 正文，不把 `primary_docs`、组件 README 或仓库级 `README.md` 设为每次请求的固定前置。
- `primary_docs` 用于按需回源，不是默认前置阅读列表。
- 专项 skill 必须有明确的“工作流程”，至少覆盖：先判断 SDK 是否存在、再判断环境是否激活、再判断是否需要构建、再判断运行前置、最后执行任务并回传结果。
- 对“跑一下性能数据/帮我测一下”这类执行型请求，skill 不能只给命令入口，必须把“真正执行测试并返回指标/失败点”写成流程的一部分。
- target 或 board 选择规则统一写在 `spacemit-robot-shared`；专项 skill 不写死 `k1-*`、`k3-*` 目标名，只在需要时声明构建倾向与模块范围。
- 专项 skill 推荐统一章节：`何时使用`、`默认规则`、`固定流程`、`专项任务`、`禁止事项`、`常见任务与命令`。
- `bootstrap` 仅保留首次初始化流程；`shared` 仅保留全局规则与路由，不重复组件细节。

## build_hint

- `build_hint` 用于表达该 skill 的构建倾向，可选值仅有：`single_package_first`、`target_preferred`、`target_required`。
- `build_hint` 只表示是否需要 target 上下文，不直接绑定某个具体 target 文件名。
- 专项 skill 可在 frontmatter `metadata.sdk.build_hint` 中显式声明；若未声明，则按 `spacemit-robot-shared` 的默认路径规则推导。
- 先路由到专项 skill，再依据其 `build_hint` 决定构建路径。
- 当 `build_hint` 需要 target 时，应先确定 board；来源优先级为用户或环境显式给出，其次才是目标机的 `/sys/firmware/devicetree/base/compatible`；同一 board 下若有多个 product 候选，不自行猜测。

## 范围边界

- `spacemit-robot-sdk-bootstrap`：首次获取 SDK、基础依赖、`repo`、`SPACEMIT_SDK_ROOT`
- `spacemit-robot-build`（若维护）：target 与全量构建（见 `skill-map.yaml`）
- `spacemit-robot-shared`：根路径约定、通用前置、路由
- `spacemit-robot-llm`：`model_zoo/llm` 的构建、运行、示例与 API 入口指针
