---
name: spacemit-robot-shared
description: SpacemiT Robot SDK 共享基线：SDK 根路径、读取优先级、构建决策与 skill 路由。
metadata:
  requires:
    bins: ["bash"]
---

# SpacemiT 共享规则

## 仓库心智模型（相对 SDK 根）

- 构建入口看 `build/README.md`（`envsetup.sh`、`lunch`、`m`、`mm`）。
- target 规则看 `target/README.md` 与 `target/*.json`。
- 组件与应用细节看 `components/`、`middleware/`、`application/` 各子目录 README。
- `target/*.json` 是板型或产品构建方案，不是用户能力入口。

## 读取优先级

1. 先读本文件，确认根路径、路由与通用规则。
2. 再路由到最匹配的专项 skill，先按 skill 正文给出的流程执行。
3. `primary_docs`、组件 README、头文件属于按需回源资料；只有命令细节不清、参数语义不清、或实际执行失败时再读。
4. 只有在以下场景才回读额外的总览文档：需要整体目录总览、当前没有命中的专项 skill、或多份文档表述冲突需要回源确认。
5. 不要每次请求都先读总览文档，也不要把各组件 README 设为固定前置。

## SDK 根路径

- `robot-skills` 与 SDK 目录相互独立；先确定完整 SDK 根，至少包含 `build/`、`components/`、`application/`、`target/`。
- 若找不到完整 SDK 根目录，则不要直接执行组件命令、`envsetup`、`lunch` 或 `mm`；先走 [`spacemit-robot-sdk-bootstrap`](../spacemit-robot-sdk-bootstrap/SKILL.md)。
- 文档中的相对路径均相对 SDK 根；执行构建、运行、测试前先在 `$SPACEMIT_SDK_ROOT` 下执行 `source build/envsetup.sh`。

## 总体原则

1. 用户面向“能力”，不是面向 target 名。
2. 先路由到专项 skill，再判断构建方式。
3. 能 `mm` 就先 `mm`，不默认全量构建。
4. 只有确实依赖板型、驱动或产品配置时，才执行 `lunch <target>`。
5. 自动化或 agent 场景下，不依赖裸 `lunch` 的交互默认项。

## board 与 target

- 需要 target 时，先确定 board，再在该 board 对应的候选里显式选择 `lunch <target>`。
- board 来源优先级：用户或环境已明确给出 > 目标机可读 `/sys/firmware/devicetree/base/compatible`。
- 从 `compatible` 读取时，先去掉 NUL，再取最具体且能与 target JSON `board` 对齐的值，例如 `spacemit,k3-com260` -> `k3-com260`。
- 当前 SDK 不会自动从 board 推导 product；若同一 board 下有多个 product 候选且无额外信息，则停止并询问。
- 不跨平台猜 `k1-*`、`k3-*` target，也不只凭文件名前缀自造 target 名。

## build_hint

- `single_package_first`：先 `source build/envsetup.sh`，进入模块目录优先执行 `mm`；仅在暴露依赖或整机配置缺口时再升级到 target 路径。
- `target_preferred`：可先尝试 `mm`，但若模块明显依赖板型、驱动或 target 选项，则优先走 `lunch <target>`。
- `target_required`：先确定 board 和 target，再执行 `lunch <target>`，然后按 README 构建或运行。

默认推导：

- `components/model_zoo/*`：`single_package_first`
- `components/peripherals/*`：`target_preferred`
- `middleware/ros2/*`：`target_preferred`
- `application/native/*`：`target_required`
- `application/ros2/*`：`target_required`

若专项 skill 已显式声明 `metadata.sdk.build_hint`，以专项 skill 为准。

## 通用决策流

1. 先确认 SDK 根是否完整；不完整就走 bootstrap。
2. 再执行 `source build/envsetup.sh`。
3. 再路由到最匹配的专项 skill，并先按 skill 正文流程执行。
4. 再按专项 skill 的 `build_hint`，或 shared 默认规则，决定先 `mm` 还是先 `lunch <target>`。
5. 若需要 target，先确定 board；同一 board 下若有多个 product 候选，先询问用户。
6. 若命令细节、参数或接口语义仍不明确，再回读该 skill 的 `primary_docs`、组件 README 或头文件。
7. 再检查运行前置，如模型、设备、服务、环境变量、端口、权限与输出目录。
8. 对“帮我执行 / 帮我测一下 / 跑性能数据”这类请求，必须真正执行并返回结果、条件与失败点。

## 路由

- 首次拉 SDK 与环境：[`spacemit-robot-sdk-bootstrap`](../spacemit-robot-sdk-bootstrap/SKILL.md)
- 专项组件或应用（例 LLM）：[`spacemit-robot-llm`](../spacemit-robot-llm/SKILL.md)
