---
name: spacemit-robot-sdk-bootstrap
description: 首次获取 SpacemiT Robot SDK 的初始化入口；负责 `repo init/sync`、依赖安装与导出 `SPACEMIT_SDK_ROOT`，不承担日常模块构建。
metadata:
  requires:
    bins: ["bash", "repo"]
---

# SpacemiT SDK 初始化

先读 [`spacemit-robot-shared`](../spacemit-robot-shared/SKILL.md)。

## 何时使用

- 用户还没有完整 SDK，需要首次拉取或重新初始化工作区。
- 当前目录下找不到完整的 `build/`、`components/`、`application/`、`target/`。
- 任务还停留在“先把 SDK 拉下来并准备好环境”的阶段。

## 默认规则

- 本 skill 仅用于首次初始化，不负责日常模块构建、压测或联调。
- 完成初始化后，应回到对应专项 skill 继续执行，不要停留在 bootstrap。
- `lunch <target>` 仅在 target 已明确时使用；不要依赖裸 `lunch` 默认项。

## 固定流程

1. 安装初始化依赖，并创建工作目录：

```bash
sudo apt update
sudo apt install -y repo build-essential cmake pkg-config jq curl
mkdir <工作区目录> && cd <工作区目录>
```

2. 拉取 SDK，二选一：

GitHub 可稳定访问：

```bash
repo init -u https://github.com/spacemit-robotics/manifest.git -b main -m default.xml \
  --repo-url=https://gitee.com/spacemit-robotics/git-repo
repo sync -j4 && repo start robot-dev --all
```

GitHub 不稳定（国内镜像）：

```bash
repo init -u https://gitee.com/spacemit-robotics/manifest.git -b main -m default.xml \
  --repo-url=https://gitee.com/spacemit-robotics/git-repo
repo sync -j4 && repo start robot-dev --all
```

3. 在 SDK 根导出环境并验证：

```bash
export SPACEMIT_SDK_ROOT="$(pwd)"
source build/envsetup.sh
lunch <target> # 仅在已明确 target 时使用
```

4. 确认 `application/`、`build/`、`components/`、`target/` 存在，且 `envsetup` 无报错。
5. 初始化完成后，返回 [`spacemit-robot-shared`](../spacemit-robot-shared/SKILL.md) 路由到具体专项 skill。

## 禁止事项

- 不要把 bootstrap 当成日常模块构建或性能测试入口。
- 不要在 SDK 尚未完整拉取前直接执行组件命令、`mm` 或专项脚本。
- 不要在 target 未明确时使用裸 `lunch` 让 agent 依赖默认项。
