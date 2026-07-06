---
name: spacemit-robot-remote
description: SpacemiT Robot SDK 远程开发基础 skill；用于 SSH 连通性检查、远程 SDK root 检查、板端命令执行，以及 remote/hybrid 模式下的只读诊断。
---

# SpacemiT Robot Remote

先按 `spacemit-robot-shared` 确认 mode、`SROBOTIS_REMOTE` 和 `SROBOTIS_REMOTE_ROOT`。

## Rules

- `remote` 和 `hybrid` 的构建、运行、测试都在板端执行。
- 不写死 host、用户名、端口、target 或 SDK root。
- 不依赖 Python、bash helper 或仓库内脚本；agent 直接使用系统 SSH 客户端执行用户确认后的命令。
- 只读环境检查可以直接执行；会修改板端文件、安装依赖、启动服务、占用设备或移动硬件的命令需要先说明影响并确认。
- 远程 SDK root 必须至少包含 `build/`、`components/`、`application/`、`target/`。

## Command Guidance

远程执行前必须先进入 `SROBOTIS_REMOTE_ROOT`，并确认 `build/`、`components/`、`application/`、`target/` 都存在；确认通过后再执行用户请求的构建、运行或诊断命令。下面只是结构示例，实际 host、root 和命令来自 shared 的配置解析结果：

```bash
ssh "<user@host>" '
  cd "<remote-sdk-root>" || exit 1
  test -d build || exit 1
  test -d components || exit 1
  test -d application || exit 1
  test -d target || exit 1
  # run the requested command here
'
```

需要 SDK 环境时，在远端 SDK root 内先执行 `source build/envsetup.sh`，再执行具体任务。Windows PC 场景优先使用系统 OpenSSH、Git Bash、WSL 或 agent 自带的远程执行能力；不要要求用户额外安装 Python。

## Flow

1. 解析配置来源，确认 `SROBOTIS_REMOTE` 和 `SROBOTIS_REMOTE_ROOT`。
2. 检查 SSH 是否可用。
3. 检查远端 SDK root 是否完整。
4. 需要 SDK 环境时，进入远端 root 后执行 `source build/envsetup.sh`。
5. 执行用户要求的命令，并返回命令、退出码、关键输出和失败点。

日常开发验证不默认调用 `scripts/test/robot-test`；只有 CI、回归验证或用户明确要求时才使用。
