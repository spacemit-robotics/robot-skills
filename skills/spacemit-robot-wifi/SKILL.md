---
name: spacemit-robot-wifi
description: >-
  components/peripherals/wifi 与 middleware/ros2/peripherals/wifi 的构建、PR
  测试、NetworkManager 硬件 smoke 与 ROS 2 WiFi 状态/扫描/连接服务验证入口。
metadata:
  requires:
    bins: ["bash"]
  sdk:
    module_paths:
      - components/peripherals/wifi
      - middleware/ros2/peripherals/wifi
    primary_docs:
      - components/peripherals/wifi/README.md
      - components/peripherals/wifi/test.yaml
      - components/peripherals/wifi/package.xml
      - middleware/ros2/peripherals/wifi/README.md
      - middleware/ros2/peripherals/wifi/test.yaml
      - middleware/ros2/peripherals/wifi/package.xml
    build_hint: target_preferred
---

# SpacemiT Robot WiFi

先按 [`spacemit-robot-shared`](../spacemit-robot-shared/SKILL.md) 确认 SDK 根路径与通用构建规则；无 SDK 就转 [`spacemit-robot-sdk-bootstrap`](../spacemit-robot-sdk-bootstrap/SKILL.md)。

## 何时使用

- 用户要构建、测试或调试 `components/peripherals/wifi`。
- 用户要构建、测试或运行 `middleware/ros2/peripherals/wifi` 的 WiFi 节点。
- 用户要验证 NetworkManager/nmcli、扫描、连接、断开、状态发布、保存网络或 MAC 设置。

## 默认规则

- `build_hint`: `target_preferred`
- SDK 内模块路径：`$SPACEMIT_SDK_ROOT/components/peripherals/wifi` 与 `$SPACEMIT_SDK_ROOT/middleware/ros2/peripherals/wifi`。
- ROS 2 节点依赖底层 wifi 组件，构建或调试 ROS 2 前先确认组件层已构建。
- PR 测试使用 fake nmcli/backend；真实 NetworkManager、无线网卡、扫描和连接只走 `manual` scope。
- 连接/断开会改变当前网络；执行真实连接前必须确认 SSID、密码和是否会影响当前会话。

## 固定流程

1. 确认 `$SPACEMIT_SDK_ROOT` 指向完整 SDK。
2. 在 `$SPACEMIT_SDK_ROOT` 下执行 `source build/envsetup.sh`。
3. 组件构建执行 `./build/build.sh package components/peripherals/wifi`。
4. ROS 2 构建先确保组件构建完成，再执行 `./build/build.sh package middleware/ros2/peripherals/wifi`。
5. 测试前分别执行 `./scripts/test/robot-test list components/peripherals/wifi` 和 `./scripts/test/robot-test list middleware/ros2/peripherals/wifi`。
6. PR 验证分别执行 `./scripts/test/robot-test run components/peripherals/wifi --scope pr` 与 `./scripts/test/robot-test run middleware/ros2/peripherals/wifi --scope pr`。
7. 对“帮我跑一下”“帮我测一下”类请求，必须真实执行命令，并返回命令、结果、日志路径和失败点。

## 专项任务

### 构建与 PR 测试

优先先跑组件层，再跑 ROS 2 层。组件层覆盖 init、on/off、scan 解析、station info、saved networks、AP config、MAC API 和错误路径；ROS 2 层覆盖状态发布、scan/connect/disconnect 服务、断开后状态和异常处理。

### 硬件 smoke

真实硬件测试需要确认 `nmcli`、NetworkManager、无线网卡和用户允许的网络操作。若节点管理当前 ROS 2 使用的网卡，断开 WiFi 可能影响 DDS 发现；按 README 判断是否需要本机回环限制。

## 禁止事项

- 不要默认写死 target；需要 target 时按 shared 规则确认 board 和 product。
- 不要未经确认连接、断开、删除保存网络、改 MAC 或启停 AP。
- 不要把真实 WiFi 扫描/连接放进 PR scope。
- 不要只给命令不执行；执行型请求必须真实运行并回传结果。

## 常见任务与命令

| 意图 | 命令 |
| ---- | ---- |
| 构建组件 | `cd "$SPACEMIT_SDK_ROOT" && source build/envsetup.sh && ./build/build.sh package components/peripherals/wifi` |
| 构建 ROS 2 节点 | `cd "$SPACEMIT_SDK_ROOT" && source build/envsetup.sh && ./build/build.sh package components/peripherals/wifi && ./build/build.sh package middleware/ros2/peripherals/wifi` |
| 列出组件测试 | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test list components/peripherals/wifi` |
| 跑组件 PR 测试 | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test run components/peripherals/wifi --scope pr` |
| 列出 ROS 2 测试 | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test list middleware/ros2/peripherals/wifi` |
| 跑 ROS 2 PR 测试 | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test run middleware/ros2/peripherals/wifi --scope pr` |
| 跑硬件 smoke | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test run components/peripherals/wifi --scope manual` |
