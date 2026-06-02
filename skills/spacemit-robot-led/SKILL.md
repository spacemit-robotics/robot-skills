---
name: spacemit-robot-led
description: >-
  components/peripherals/led 与 middleware/ros2/peripherals/led 的构建、PR
  测试、sysfs/SPI LED 硬件 smoke 与 ROS 2 命令/状态话题验证入口。
metadata:
  requires:
    bins: ["bash"]
  sdk:
    module_paths:
      - components/peripherals/led
      - middleware/ros2/peripherals/led
    primary_docs:
      - components/peripherals/led/README.md
      - components/peripherals/led/test.yaml
      - middleware/ros2/peripherals/led/README.md
      - middleware/ros2/peripherals/led/test.yaml
      - middleware/ros2/peripherals/led/package.xml
    build_hint: target_preferred
---

# SpacemiT Robot LED

先按 [`spacemit-robot-shared`](../spacemit-robot-shared/SKILL.md) 确认 SDK 根路径与通用构建规则；无 SDK 就转 [`spacemit-robot-sdk-bootstrap`](../spacemit-robot-sdk-bootstrap/SKILL.md)。

## 何时使用

- 用户要构建、测试或调试 `components/peripherals/led`。
- 用户要构建、测试或运行 `middleware/ros2/peripherals/led` 的 LED 命令/状态节点。
- 用户要验证 sysfs LED、SPI WS2812/SK6812、静态点亮、闪烁或呼吸效果。

## 默认规则

- `build_hint`: `target_preferred`
- SDK 内模块路径：`$SPACEMIT_SDK_ROOT/components/peripherals/led` 与 `$SPACEMIT_SDK_ROOT/middleware/ros2/peripherals/led`。
- ROS 2 节点依赖底层 LED 组件，构建或调试 ROS 2 前先确认组件层已构建。
- PR 测试使用 mock driver；真实 `/sys/class/leds/*` 或 `/dev/spidev*` 只走 `manual` scope。
- LED 效果依赖周期 `led_tick()`；ROS 2 问题优先检查 `tick_period_ms`、LED ID 唯一性和驱动配置。

## 固定流程

1. 确认 `$SPACEMIT_SDK_ROOT` 指向完整 SDK。
2. 在 `$SPACEMIT_SDK_ROOT` 下执行 `source build/envsetup.sh`。
3. 组件构建执行 `./build/build.sh package components/peripherals/led`。
4. ROS 2 构建先确保组件构建完成，再执行 `./build/build.sh package middleware/ros2/peripherals/led`。
5. 测试前分别执行 `./scripts/test/robot-test list components/peripherals/led` 和 `./scripts/test/robot-test list middleware/ros2/peripherals/led`。
6. PR 验证分别执行 `./scripts/test/robot-test run components/peripherals/led --scope pr` 与 `./scripts/test/robot-test run middleware/ros2/peripherals/led --scope pr`。
7. 对“帮我跑一下”“帮我测一下”类请求，必须真实执行命令，并返回命令、结果、日志路径和失败点。

## 专项任务

### 构建与 PR 测试

优先先跑组件层，再跑 ROS 2 层。组件层覆盖 LED 状态、亮度、颜色、闪烁、呼吸和错误路径；ROS 2 层覆盖命令映射、状态发布、重复 LED ID 和后端分配失败。

### 硬件 smoke

真实硬件测试需要确认 sysfs LED 名称、spidev 路径、权限、颜色顺序和人工看护。不要在未确认设备的情况下连续闪烁或高亮输出。

## 禁止事项

- 不要默认写死 target；需要 target 时按 shared 规则确认 board 和 product。
- 不要把 LED 名称、SPI 设备号或颜色顺序硬编码成未经确认的板级默认值。
- 不要在无硬件或无人看护时运行 manual smoke。
- 不要只给命令不执行；执行型请求必须真实运行并回传结果。

## 常见任务与命令

| 意图 | 命令 |
| ---- | ---- |
| 构建组件 | `cd "$SPACEMIT_SDK_ROOT" && source build/envsetup.sh && ./build/build.sh package components/peripherals/led` |
| 构建 ROS 2 节点 | `cd "$SPACEMIT_SDK_ROOT" && source build/envsetup.sh && ./build/build.sh package components/peripherals/led && ./build/build.sh package middleware/ros2/peripherals/led` |
| 列出组件测试 | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test list components/peripherals/led` |
| 跑组件 PR 测试 | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test run components/peripherals/led --scope pr` |
| 列出 ROS 2 测试 | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test list middleware/ros2/peripherals/led` |
| 跑 ROS 2 PR 测试 | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test run middleware/ros2/peripherals/led --scope pr` |
| 跑硬件 smoke | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test run components/peripherals/led --scope manual` |
