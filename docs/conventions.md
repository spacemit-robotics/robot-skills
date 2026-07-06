# Skill 约定

## Naming

- 目录名与 frontmatter `name` 统一使用 `spacemit-robot-` 前缀、小写和连字符。

## Content

- 运行时只以 `skills/` 下安装后的 `SKILL.md` 为准。
- SDK root 环境变量只使用 `SROBOTIS_ROOT`。
- 组件 skill 保持薄入口，不复制 SDK README，不写长命令 runbook。
- 组件 skill 必须链接到基础规则：`spacemit-robot-shared`、`spacemit-robot-build`、`spacemit-robot-remote`、`spacemit-robot-sync`。
- 组件 skill 不写死 host、SSH 命令、board、target、用户目录。
- 组件 skill 不默认调用 `robot-test`；它只属于 CI、回归验证或用户明确要求。
- `primary_docs` 用于按需回源，优先 SDK 模块内 `AGENTS.md`，再读 README、package 或 test 文件。
- 产品知识写在 `SKILL.md`：模块能力、典型场景、输入输出、支持/不支持行为，以及能力如何对应到 demo、API 和 benchmark。
- 复杂组件可用 `references/` 拆出按需细节，但文件名按任务命名，不固定六件套，也不标准化 `product.md` 或 `overview.md`。
- `scripts/` 是可选资源，只用于确定性、重复、容易写错或需要结构化输出的动作。
- 运行时 helper 避免 Python 依赖；remote/build/shared 保持规则型，确需脚本时优先 Node.js。

## Build Hint

- `single_package_first`: 先按模块构建，遇到产品配置缺口再升级 target。
- `target_preferred`: 可先模块构建，但明显依赖板型、驱动或产品配置时优先 target。
- `target_required`: 先确定 board 和 target，再构建或运行。

## Mode Boundary

- `local`: agent 在板端，SDK 在板端。
- `remote`: agent 在 PC，SDK 在板端，所有执行通过远程规则在板端完成。
- `hybrid`: agent 在 PC，本地 SDK 负责编辑，板端 SDK 负责构建运行，同步只做 PC 到板端单向同步。

Hybrid 不交叉编译，不在 PC 侧构建目标产物。Hybrid 的 PC 本地 SDK 默认路径是 `~/workspace/spacemit-robot`。
