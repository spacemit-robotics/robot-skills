---
name: spacemit-robot-5g
description: >-
  components/peripherals/5g 与 middleware/ros2/peripherals/5g 的构建、PR
  测试、MR880A 硬件 smoke 与 ROS 2 接口验证入口。
metadata:
  requires:
    bins: ["bash"]
  sdk:
    module_paths:
      - components/peripherals/5g
      - middleware/ros2/peripherals/5g
    primary_docs:
      - components/peripherals/5g/README.md
      - components/peripherals/5g/test.yaml
      - middleware/ros2/peripherals/5g/README.md
      - middleware/ros2/peripherals/5g/test.yaml
      - middleware/ros2/peripherals/5g/package.xml
    build_hint: target_preferred
---

# SpacemiT Robot 5G

先按 [`spacemit-robot-shared`](../spacemit-robot-shared/SKILL.md) 确认 SDK 根路径与通用构建规则；无 SDK 就转 [`spacemit-robot-sdk-bootstrap`](../spacemit-robot-sdk-bootstrap/SKILL.md)。

## 何时使用

- 用户要构建、测试或调试 `components/peripherals/5g`。
- 用户要构建、测试或运行 `middleware/ros2/peripherals/5g` 的 MR880A ROS 2 节点。
- 用户要验证 AT 透传、PDP、拨号、飞行模式、信号/注册状态或硬件 smoke。

## 默认规则

- `build_hint`: `target_preferred`
- SDK 内模块路径：`$SPACEMIT_SDK_ROOT/components/peripherals/5g` 与 `$SPACEMIT_SDK_ROOT/middleware/ros2/peripherals/5g`。
- ROS 2 节点依赖底层 5G 组件，构建或调试 ROS 2 前先确认组件层已构建。
- PR 测试使用 mock UART modem；真实 MR880A、SIM、APN、DHCP 和网络拨号只走 `manual` scope。
- 只有命令细节、参数语义或执行失败时，才回读 `primary_docs`、`CMakeLists.txt` 或测试脚本。

## 固定流程

1. 确认 `$SPACEMIT_SDK_ROOT` 指向完整 SDK。
2. 在 `$SPACEMIT_SDK_ROOT` 下执行 `source build/envsetup.sh`。
3. 组件构建执行 `./build/build.sh package components/peripherals/5g`。
4. ROS 2 构建先确保组件构建完成，再执行 `./build/build.sh package middleware/ros2/peripherals/5g`。
5. 测试前分别执行 `./scripts/test/robot-test list components/peripherals/5g` 和 `./scripts/test/robot-test list middleware/ros2/peripherals/5g`。
6. PR 验证分别执行 `./scripts/test/robot-test run components/peripherals/5g --scope pr` 与 `./scripts/test/robot-test run middleware/ros2/peripherals/5g --scope pr`。
7. 对“帮我跑一下”“帮我测一下”类请求，必须真实执行命令，并返回命令、结果、日志路径和失败点。

## 专项任务

### 构建与 PR 测试

优先先跑组件层，再跑 ROS 2 层。组件层覆盖 modem API、错误路径和 mock 串口；ROS 2 层覆盖状态发布与 PDP、拨号、飞行模式、AT 服务。

### 硬件 smoke

真实硬件测试需要 MR880A、可用 AT 串口或自动识别、SIM/APN 和人工看护。未确认硬件与网络影响前，不要运行 `manual` scope，不要主动修改用户当前网络连接。

## 禁止事项

- 不要默认写死 target；需要 target 时按 shared 规则确认 board 和 product。
- 不要在无硬件或无人看护时运行 MR880A manual smoke。
- 不要默认清理网络接口、杀掉现有拨号进程或改写用户 APN 配置。
- 不要只给命令不执行；执行型请求必须真实运行并回传结果。

## 常见任务与命令

| 意图 | 命令 |
| ---- | ---- |
| 构建组件 | `cd "$SPACEMIT_SDK_ROOT" && source build/envsetup.sh && ./build/build.sh package components/peripherals/5g` |
| 构建 ROS 2 节点 | `cd "$SPACEMIT_SDK_ROOT" && source build/envsetup.sh && ./build/build.sh package components/peripherals/5g && ./build/build.sh package middleware/ros2/peripherals/5g` |
| 列出组件测试 | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test list components/peripherals/5g` |
| 跑组件 PR 测试 | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test run components/peripherals/5g --scope pr` |
| 列出 ROS 2 测试 | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test list middleware/ros2/peripherals/5g` |
| 跑 ROS 2 PR 测试 | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test run middleware/ros2/peripherals/5g --scope pr` |
| 跑硬件 smoke | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test run components/peripherals/5g --scope manual` |
