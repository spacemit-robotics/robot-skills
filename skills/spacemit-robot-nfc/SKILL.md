---
name: spacemit-robot-nfc
description: >-
  components/peripherals/nfc 与 middleware/ros2/peripherals/nfc 的构建、PR
  测试、SI512 I2C 硬件 smoke 与 ROS 2 标签话题/读写服务验证入口。
metadata:
  requires:
    bins: ["bash"]
  sdk:
    module_paths:
      - components/peripherals/nfc
      - middleware/ros2/peripherals/nfc
    primary_docs:
      - components/peripherals/nfc/README.md
      - components/peripherals/nfc/test.yaml
      - middleware/ros2/peripherals/nfc/README.md
      - middleware/ros2/peripherals/nfc/test.yaml
      - middleware/ros2/peripherals/nfc/package.xml
    build_hint: target_preferred
---

# SpacemiT Robot NFC

先按 [`spacemit-robot-shared`](../spacemit-robot-shared/SKILL.md) 确认 SDK 根路径与通用构建规则；无 SDK 就转 [`spacemit-robot-sdk-bootstrap`](../spacemit-robot-sdk-bootstrap/SKILL.md)。

## 何时使用

- 用户要构建、测试或调试 `components/peripherals/nfc`。
- 用户要构建、测试或运行 `middleware/ros2/peripherals/nfc` 的 NFC 节点。
- 用户要验证 SI512 I2C、标签轮询、UID、块读写、ROS 2 tag topic 或 poll/read/write 服务。

## 默认规则

- `build_hint`: `target_preferred`
- SDK 内模块路径：`$SPACEMIT_SDK_ROOT/components/peripherals/nfc` 与 `$SPACEMIT_SDK_ROOT/middleware/ros2/peripherals/nfc`。
- ROS 2 节点依赖底层 NFC 组件，构建或调试 ROS 2 前先确认组件层已构建。
- PR 测试使用 mock NFC driver；真实 SI512、NFC tag、I2C 总线和读写块只走 `manual` scope。
- ROS 2 `write_block` 数据必须是 16 字节；同卡重复发布、poll 超时等行为以 README 和测试脚本为准。

## 固定流程

1. 确认 `$SPACEMIT_SDK_ROOT` 指向完整 SDK。
2. 在 `$SPACEMIT_SDK_ROOT` 下执行 `source build/envsetup.sh`。
3. 组件构建执行 `./build/build.sh package components/peripherals/nfc`。
4. ROS 2 构建先确保组件构建完成，再执行 `./build/build.sh package middleware/ros2/peripherals/nfc`。
5. 测试前分别执行 `./scripts/test/robot-test list components/peripherals/nfc` 和 `./scripts/test/robot-test list middleware/ros2/peripherals/nfc`。
6. PR 验证分别执行 `./scripts/test/robot-test run components/peripherals/nfc --scope pr` 与 `./scripts/test/robot-test run middleware/ros2/peripherals/nfc --scope pr`。
7. 对“帮我跑一下”“帮我测一下”类请求，必须真实执行命令，并返回命令、结果、日志路径和失败点。

## 专项任务

### 构建与 PR 测试

优先先跑组件层，再跑 ROS 2 层。组件层覆盖 allocation、init、callback、poll、read/write 和错误路径；ROS 2 层覆盖 poll/read/write 服务、标签消息转换和无卡/坏参数处理。

### 硬件 smoke

真实硬件测试需要确认 SI512、I2C 设备路径、地址、NFC tag 和权限。写块测试可能改变卡片数据，执行前必须确认用户允许。

## 禁止事项

- 不要默认写死 target；需要 target 时按 shared 规则确认 board 和 product。
- 不要在未确认用户允许时执行真实 NFC 写块操作。
- 不要在无硬件、无卡片或无 I2C 权限时运行 manual smoke。
- 不要只给命令不执行；执行型请求必须真实运行并回传结果。

## 常见任务与命令

| 意图 | 命令 |
| ---- | ---- |
| 构建组件 | `cd "$SPACEMIT_SDK_ROOT" && source build/envsetup.sh && ./build/build.sh package components/peripherals/nfc` |
| 构建 ROS 2 节点 | `cd "$SPACEMIT_SDK_ROOT" && source build/envsetup.sh && ./build/build.sh package components/peripherals/nfc && ./build/build.sh package middleware/ros2/peripherals/nfc` |
| 列出组件测试 | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test list components/peripherals/nfc` |
| 跑组件 PR 测试 | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test run components/peripherals/nfc --scope pr` |
| 列出 ROS 2 测试 | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test list middleware/ros2/peripherals/nfc` |
| 跑 ROS 2 PR 测试 | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test run middleware/ros2/peripherals/nfc --scope pr` |
| 跑硬件 smoke | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test run components/peripherals/nfc --scope manual` |
