---
name: spacemit-robot-sdk-bootstrap
description: SpacemiT Robot SDK 首次初始化入口；用于板端或 PC 本地准备 SDK、依赖、repo init/sync，并验证 SROBOTIS_ROOT，不承担日常构建或测试。
---

# SpacemiT Robot SDK Bootstrap

先按 `spacemit-robot-shared` 确认 mode 和 SDK root 需求。本 skill 只处理首次准备阶段，初始化完成后回到 shared、build、remote、sync 或具体组件 skill。

## Scope

适用场景：

- 用户还没有 SDK，需要首次下载。
- 板端没有 `/home/<user>/spacemit_robot` 或用户指定的 SDK root。
- PC 需要本地 SDK 作为 `hybrid` 编辑工作区。
- 现有目录不满足完整 SDK root 检查。

不适用场景：

- 日常模块构建。
- 日常测试或性能验证。
- 组件 API 接入说明。
- 自动选择 target 后继续构建。

## Initialization Types

板端 bootstrap：

- 用于 `local` 或 `remote` 的板端 SDK。
- 确认 SSH 或本地 shell 可用后，在板端创建 SDK 目录并执行 repo 初始化。

PC 本地 bootstrap：

- 用于 `hybrid` 的 PC 编辑工作区。
- 默认 SDK 目录为 `~/workspace/spacemit-robot`，除非用户明确指定其他路径。
- PC 本地 SDK 只负责读代码和改代码；目标产物仍在板端构建。

## Explicit Confirmation

以下动作属于显式初始化动作，执行前必须向用户确认目标机器、目录和影响范围：

- `sudo apt update`
- `sudo apt install ...`
- 创建或清空 SDK 工作目录
- `repo init ...`
- `repo sync ...`
- 大量下载、覆盖 manifest 或切换分支

不要在未确认的情况下修改用户已有 SDK、删除目录、重置分支或自动覆盖本地改动。

## Minimal Flow

1. 确认 mode：
   - `local`: 在板端初始化 `SROBOTIS_ROOT`。
   - `remote`: 通过 `spacemit-robot-remote` 在板端初始化 `SROBOTIS_REMOTE_ROOT`。
   - `hybrid`: PC 初始化 `SROBOTIS_ROOT`，板端初始化 `SROBOTIS_REMOTE_ROOT`。
2. 确认 SDK 目录不存在或用户允许复用。
3. 经用户确认后安装 repo 与构建基础依赖。
4. 经用户确认后执行 repo init 和 repo sync。
5. 初始化结束后验证完整 SDK root。
6. 在 SDK root 验证：

```bash
export SROBOTIS_ROOT="<sdk-root>"
cd "$SROBOTIS_ROOT"
test -d build
test -d components
test -d application
test -d target
source build/envsetup.sh
```

7. 只在 target 已由用户或 shared 规则明确时执行 `lunch <target>`。

## Repo Sources

根据网络环境选择 manifest 源。GitHub 可用时优先 GitHub，国内网络不稳定时可使用 Gitee 镜像。具体分支、manifest 文件和目录必须来自用户请求、项目配置或官方文档，不能凭空猜测。

## After Bootstrap

初始化完成后输出：

- mode
- `SROBOTIS_ROOT`
- `SROBOTIS_REMOTE`
- `SROBOTIS_REMOTE_ROOT`
- SDK root 检查结果
- `source build/envsetup.sh` 验证结果
- 是否已明确 target

然后转回相应 skill 继续工作，不在 bootstrap 内继续日常构建或测试。
