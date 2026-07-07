# 模块 Skill 编写模板

本文件是 `spacemit-robot-*` 组件 skill 的唯一编写规范。目标是让 agent 能帮助用户完成 Robot SDK 的真实开发闭环：搭环境、跑示例、调用 API 做应用、跑性能数据，同时避免把每个模块都写成厚重手册。

## 设计原则

- `SKILL.md` 是主入口，负责触发、产品能力、边界、路由和安全规则。
- 运行时 agent 只会看到安装后的 `SKILL.md`；必须遵守的规则只能写进 `skills/`。
- 不把 `product.md`、`overview.md` 作为标准文件；产品知识优先写在 `SKILL.md`。
- `references/` 只放按需读取的细节资料，文件名按任务命名，不做固定六件套。
- `scripts/` 是可选资源，只用于确定性、重复、容易写错或需要解析输出的动作。
- 组件 skill 保持薄入口，不复制 SDK README，不写长命令 runbook。
- 组件 skill 不写死 host、target、board、SSH 命令或用户私有目录。
- SDK root 环境变量只使用 `SROBOTIS_ROOT`。
- 执行命令时遵守基础 skill：`spacemit-robot-shared`、`spacemit-robot-build`、`spacemit-robot-remote`、`spacemit-robot-sync`。
- 日常开发不默认调用 `scripts/test/robot-test`；只有 CI、回归或用户明确要求时才使用。

## 仓库约定

- 目录名与 frontmatter `name` 统一使用 `spacemit-robot-` 前缀、小写和连字符。
- Frontmatter 必填：`name`、`description`。
- 组件建议声明 `metadata.sdk.module_paths`、`metadata.sdk.primary_docs`、`metadata.sdk.build_hint`。
- 在 `config/skill-map.yaml` 登记 `name`、`category`、`primary_docs`。
- `primary_docs` 是按需回源索引，不是每次请求的固定前置阅读列表；优先 SDK 模块内 `AGENTS.md`，再读 README、package、header 或 test 文件。
- 组件 skill 只声明模块路径、构建倾向、文档入口、产品能力、适用边界和专项注意事项。

## 基础能力分工

- `shared`: 三模式、配置优先级、SDK root、target、路由。
- `bootstrap`: 首次初始化、依赖、repo init/sync、SDK root 验证。
- `remote`: SSH 检查、远程 SDK root 检查、远程命令执行。
- `build`: `envsetup.sh`、`lunch`、`m`、`mm` 的构建决策。
- `sync`: hybrid 单向同步、dry-run、路径保护、repo preflight。
- 组件 skill: `Contract`、`User Goals`、`Workflow`、`References`、`Notes`。

## Build Hint

- `single_package_first`: 先按模块构建，遇到产品配置缺口再升级 target。
- `target_preferred`: 可先模块构建，但明显依赖板型、驱动或产品配置时优先 target。
- `target_required`: 先确定 board 和 target，再构建或运行。

## Mode Boundary

- `local`: agent 在板端，SDK 在板端。
- `remote`: agent 在 PC，SDK 在板端，所有执行通过远程规则在板端完成。
- `hybrid`: agent 在 PC，本地 SDK 负责编辑，板端 SDK 负责构建运行，同步只做 PC 到板端单向同步。

Hybrid 不交叉编译，不在 PC 侧构建目标产物。Hybrid 的 PC 本地 SDK 默认路径是 `~/workspace/spacemit-robot`。

## 推荐目录

```text
skills/spacemit-robot-<module>/
├── SKILL.md
├── references/        # 可选：按任务拆分的细节资料
└── scripts/           # 可选：确定性 helper
```

只创建真实需要的目录。简单模块可以只有 `SKILL.md`。

## SKILL.md 模板

```markdown
---
name: spacemit-robot-<module>
description: <一句话说明这个 skill 解决什么问题，以及何时触发>
metadata:
  sdk:
    module_paths:
      - <SDK-relative module path>
    primary_docs:
      - <SDK-relative README/AGENTS/package/test path>
    build_hint: <single_package_first|target_preferred|target_required>
---

# <模块名>

## Purpose

- 本模块用于：<产品能力、典型用户场景、输入输出>。
- 适合处理：<搭环境/跑示例/API 接入/benchmark/排障中的哪些任务>。
- 不适合处理：<不支持能力、需要转交的模块、需要用户确认的边界>。

## Contract

- 模块路径：`<SDK-relative module path>`
- 构建倾向：`<build_hint>`
- 文档入口：`<primary_docs>`
- 基础规则：先用 `spacemit-robot-shared` 解析 mode、SDK root 和 target；构建走 `spacemit-robot-build`；remote/hybrid 执行走 `spacemit-robot-remote`；hybrid 同步走 `spacemit-robot-sync`。

## User Goals

| 用户目标 | 本模块支持情况 | 资料入口 |
| --- | --- | --- |
| 搭建环境 | 是/否/部分 | `<SKILL.md 或 references/...>` |
| 跑通示例 | 是/否/部分 | `<SKILL.md 或 references/...>` |
| 调用 API 做应用 | 是/否/部分 | `<SKILL.md 或 references/...>` |
| 跑性能数据 | 是/否/部分 | `<SKILL.md 或 references/...>` |

## Workflow

1. 判断用户是在搭环境、跑示例、写 API 应用、跑性能、排障，还是做代码修改。
2. 优先读取 SDK 模块内 `AGENTS.md`；不存在时按需读取 primary docs。
3. 只读取与当前任务匹配的 reference 文件；不要为了“完整”预读所有资料。
4. 构建请求交给 `spacemit-robot-build`，不要在组件 skill 写死命令或 target。
5. `remote` 和 `hybrid` 场景下，所有执行都在板端完成。
6. 涉及真实设备、运动控制、模型下载、长时间 benchmark、覆盖远端文件或 `sudo` 时，先说明影响并确认。

## References

只列实际存在的 reference 文件。每个条目都写清楚什么时候读取。

- `references/setup.md`: 准备依赖、模型、硬件、权限、配置或模块特殊构建步骤前读取。
- `references/examples.md`: 用户要运行 demo、sample、launch、服务或 smoke 时读取。
- `references/api.md`: 用户要调用 C/C++、Python 或 ROS2 API 做应用时读取。
- `references/benchmarking.md`: 用户明确要性能数据、延迟、吞吐、精度或资源占用时读取。
- `references/troubleshooting.md`: 命令失败或用户提供错误信息时读取。

## Scripts

没有脚本时删除本节。只列实际存在的脚本。

| Script | 作用 | 何时使用 |
| --- | --- | --- |
| `scripts/<name>` | <确定性动作> | <用户任务或验证场景> |

脚本规则：

- 脚本必须能通过 `--help` 或等价方式说明用途。
- 脚本默认 dry-run 或只读，除非用户明确要求修改。
- 运行时 helper 不应要求 PC 用户额外安装 Python；能写成规则就写成规则，确需脚本时优先使用 Node.js，因为安装流程已经依赖 `npx`/npm。
- 如果脚本必须在板端或 SDK 环境执行，要写清执行位置和依赖。
- 脚本不能绕过 shared/build/remote/sync 的模式和执行位置规则。

## Notes

- 写本模块最容易跑偏的 1-3 条约束。
- 明确哪些请求应转给其他 skill 或 SDK 文档。
```

## References 设计

不要追求固定文件名。按用户任务命名，让 agent 一眼知道什么时候读。

常用命名：

| 文件名 | 适合内容 |
| --- | --- |
| `setup.md` | 依赖、环境变量、权限、模型、硬件、配置、模块特殊构建步骤 |
| `examples.md` | demo、sample、launch、服务启动、预期输出、日志、smoke |
| `api.md` | C/C++、Python、ROS2 API，最小应用代码，数据格式 |
| `benchmarking.md` | 性能命令、指标、环境记录、结果格式、解释方式 |
| `troubleshooting.md` | 常见错误、诊断命令、修复建议、安全确认门 |
| `<task>.md` | 模块特有任务，例如 `model-selection.md`、`calibration.md`、`pipeline-run.md` |

只有满足下面任一条件时才拆 reference：

- 内容超过 `SKILL.md` 中 1-2 个短段落。
- 有多条命令、多种模式、多种硬件/模型/配置分支。
- 用户任务经常需要回读完整表格、API 参数、日志特征或错误处理。
- 细节不是每次触发 skill 都需要读。

## Scripts 设计

优先把规则写清楚；只有下列情况才加脚本：

- 同一段命令或解析逻辑会被反复生成。
- 动作需要路径保护、dry-run、排除规则、结构化输出或跨平台处理。
- 输出需要稳定 JSON、表格或日志摘要，靠人工拼命令容易出错。
- 操作有风险，需要脚本内置保护。

不建议为简单 `source build/envsetup.sh && mm`、普通 `ssh`、普通 `grep/rg` 添加脚本。

## 编写检查清单

- `description` 能让 agent 在用户自然语言请求中正确触发。
- frontmatter、目录名和 `config/skill-map.yaml` 登记保持一致。
- `Purpose` 写清能力、典型场景、输入输出和不支持行为。
- 四个用户目标都有支持情况和资料入口。
- `primary_docs` 只作为按需回源索引，不作为固定预读列表。
- `References` 只列实际存在的文件，不列候选清单。
- `references/` 按任务命名，不创建标准 `product.md` 或 `overview.md`。
- `scripts/` 可选；有脚本时说明用途、参数、执行位置和风险。
- 命令只写 SDK-relative 任务逻辑，不写死 host、target、board 或用户私有目录。
- 执行位置、target、构建、remote/hybrid 同步交给基础 skill 决定。
- `robot-test` 只用于 CI、回归或用户明确要求。
