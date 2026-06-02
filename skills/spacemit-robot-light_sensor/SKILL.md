---
name: spacemit-robot-light_sensor
description: >-
  components/peripherals/light_sensor 与 middleware/ros2/peripherals/light_sensor
  的构建、PR 测试、W1160 硬件 smoke 与 ROS 2 Illuminance 话题验证入口。
metadata:
  requires:
    bins: ["bash"]
  sdk:
    module_paths:
      - components/peripherals/light_sensor
      - middleware/ros2/peripherals/light_sensor
    primary_docs:
      - components/peripherals/light_sensor/README.md
      - components/peripherals/light_sensor/test.yaml
      - middleware/ros2/peripherals/light_sensor/README.md
      - middleware/ros2/peripherals/light_sensor/test.yaml
      - middleware/ros2/peripherals/light_sensor/package.xml
    build_hint: target_preferred
---

# SpacemiT Robot Light Sensor

先按 [`spacemit-robot-shared`](../spacemit-robot-shared/SKILL.md) 确认 SDK 根路径与通用构建规则；无 SDK 就转 [`spacemit-robot-sdk-bootstrap`](../spacemit-robot-sdk-bootstrap/SKILL.md)。

## 何时使用

- 用户要构建、测试或调试 `components/peripherals/light_sensor`。
- 用户要构建、测试或运行 `middleware/ros2/peripherals/light_sensor` 的光照传感器节点。
- 用户要验证 W1160 I2C 光照读取、lux 发布频率、I2C 设备路径或地址配置。

## 默认规则

- `build_hint`: `target_preferred`
- SDK 内模块路径：`$SPACEMIT_SDK_ROOT/components/peripherals/light_sensor` 与 `$SPACEMIT_SDK_ROOT/middleware/ros2/peripherals/light_sensor`。
- ROS 2 节点依赖底层 light_sensor 组件，构建或调试 ROS 2 前先确认组件层已构建。
- PR 测试使用 mock I2C driver；真实 `/dev/i2c-*`、W1160 和权限验证只走 `manual` scope。
- W1160 默认 I2C 地址是 `0x48`；设备路径、地址或静态库路径不清时再回读 primary docs。

## 固定流程

1. 确认 `$SPACEMIT_SDK_ROOT` 指向完整 SDK。
2. 在 `$SPACEMIT_SDK_ROOT` 下执行 `source build/envsetup.sh`。
3. 组件构建执行 `./build/build.sh package components/peripherals/light_sensor`。
4. ROS 2 构建先确保组件构建完成，再执行 `./build/build.sh package middleware/ros2/peripherals/light_sensor`。
5. 测试前分别执行 `./scripts/test/robot-test list components/peripherals/light_sensor` 和 `./scripts/test/robot-test list middleware/ros2/peripherals/light_sensor`。
6. PR 验证分别执行 `./scripts/test/robot-test run components/peripherals/light_sensor --scope pr` 与 `./scripts/test/robot-test run middleware/ros2/peripherals/light_sensor --scope pr`。
7. 对“帮我跑一下”“帮我测一下”类请求，必须真实执行命令，并返回命令、结果、日志路径和失败点。

## 专项任务

### 构建与 PR 测试

优先先跑组件层，再跑 ROS 2 层。组件层覆盖初始化、重复 lux polling 和错误路径；ROS 2 层覆盖 `sensor_msgs/msg/Illuminance` 发布、frame、variance 与异常采样处理。

### 硬件 smoke

真实硬件测试需要 W1160、I2C 总线、地址和读写权限。没有设备或权限时，不要运行 `manual` scope，也不要伪造 lux 数据。

## 禁止事项

- 不要默认写死 target；需要 target 时按 shared 规则确认 board 和 product。
- 不要把 `/dev/i2c-*` 或 I2C 地址猜成固定板级值。
- 不要在无 W1160 或无 I2C 权限时运行 manual smoke。
- 不要只给命令不执行；执行型请求必须真实运行并回传结果。

## 常见任务与命令

| 意图 | 命令 |
| ---- | ---- |
| 构建组件 | `cd "$SPACEMIT_SDK_ROOT" && source build/envsetup.sh && ./build/build.sh package components/peripherals/light_sensor` |
| 构建 ROS 2 节点 | `cd "$SPACEMIT_SDK_ROOT" && source build/envsetup.sh && ./build/build.sh package components/peripherals/light_sensor && ./build/build.sh package middleware/ros2/peripherals/light_sensor` |
| 列出组件测试 | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test list components/peripherals/light_sensor` |
| 跑组件 PR 测试 | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test run components/peripherals/light_sensor --scope pr` |
| 列出 ROS 2 测试 | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test list middleware/ros2/peripherals/light_sensor` |
| 跑 ROS 2 PR 测试 | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test run middleware/ros2/peripherals/light_sensor --scope pr` |
| 跑硬件 smoke | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test run components/peripherals/light_sensor --scope manual` |
