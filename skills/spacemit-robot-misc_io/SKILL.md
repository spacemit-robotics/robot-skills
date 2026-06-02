---
name: spacemit-robot-misc_io
description: >-
  components/peripherals/misc_io 与 middleware/ros2/peripherals/misc_io 的构建、PR
  测试、GPIO 输入输出硬件 smoke 与 ROS 2 命令/状态/事件话题验证入口。
metadata:
  requires:
    bins: ["bash"]
  sdk:
    module_paths:
      - components/peripherals/misc_io
      - middleware/ros2/peripherals/misc_io
    primary_docs:
      - components/peripherals/misc_io/README.md
      - components/peripherals/misc_io/test.yaml
      - components/peripherals/misc_io/package.xml
      - middleware/ros2/peripherals/misc_io/README.md
      - middleware/ros2/peripherals/misc_io/test.yaml
      - middleware/ros2/peripherals/misc_io/package.xml
    build_hint: target_preferred
---

# SpacemiT Robot Misc IO

先按 [`spacemit-robot-shared`](../spacemit-robot-shared/SKILL.md) 确认 SDK 根路径与通用构建规则；无 SDK 就转 [`spacemit-robot-sdk-bootstrap`](../spacemit-robot-sdk-bootstrap/SKILL.md)。

## 何时使用

- 用户要构建、测试或调试 `components/peripherals/misc_io`。
- 用户要构建、测试或运行 `middleware/ros2/peripherals/misc_io` 的通用 GPIO IO 节点。
- 用户要验证蜂鸣器、继电器、开关、传感器触点等输入/输出 IO。

## 默认规则

- `build_hint`: `target_preferred`
- SDK 内模块路径：`$SPACEMIT_SDK_ROOT/components/peripherals/misc_io` 与 `$SPACEMIT_SDK_ROOT/middleware/ros2/peripherals/misc_io`。
- ROS 2 节点依赖底层 misc_io 组件，构建或调试 ROS 2 前先确认组件层已构建。
- PR 测试使用 fake gpiod；真实 `/dev/gpiochip*`、chip/line offset 和外设动作只走 `manual` scope。
- ROS 2 参数数组必须等长，`io_ids` 必须唯一；输出命令只对输出 IO 生效。

## 固定流程

1. 确认 `$SPACEMIT_SDK_ROOT` 指向完整 SDK。
2. 在 `$SPACEMIT_SDK_ROOT` 下执行 `source build/envsetup.sh`。
3. 组件构建执行 `./build/build.sh package components/peripherals/misc_io`。
4. ROS 2 构建先确保组件构建完成，再执行 `./build/build.sh package middleware/ros2/peripherals/misc_io`。
5. 测试前分别执行 `./scripts/test/robot-test list components/peripherals/misc_io` 和 `./scripts/test/robot-test list middleware/ros2/peripherals/misc_io`。
6. PR 验证分别执行 `./scripts/test/robot-test run components/peripherals/misc_io --scope pr` 与 `./scripts/test/robot-test run middleware/ros2/peripherals/misc_io --scope pr`。
7. 对“帮我跑一下”“帮我测一下”类请求，必须真实执行命令，并返回命令、结果、日志路径和失败点。

## 专项任务

### 构建与 PR 测试

优先先跑组件层，再跑 ROS 2 层。组件层覆盖输入/输出 active logic、set/get 和错误路径；ROS 2 层覆盖命令驱动输出、输入回调发布事件、无效配置和命令拒绝。

### 硬件 smoke

真实硬件测试需要确认 GPIO chip、line offset、方向、有效电平和权限。不要把 K1/K3 的 GPIO 编号换算规则当成通用默认值，硬件映射不清时先回读 README 或询问。

## 禁止事项

- 不要默认写死 target；需要 target 时按 shared 规则确认 board 和 product。
- 不要把物理引脚号、全局 GPIO 号、chip/line offset 混用。
- 不要在无硬件或无人操作时运行 manual smoke。
- 不要只给命令不执行；执行型请求必须真实运行并回传结果。

## 常见任务与命令

| 意图 | 命令 |
| ---- | ---- |
| 构建组件 | `cd "$SPACEMIT_SDK_ROOT" && source build/envsetup.sh && ./build/build.sh package components/peripherals/misc_io` |
| 构建 ROS 2 节点 | `cd "$SPACEMIT_SDK_ROOT" && source build/envsetup.sh && ./build/build.sh package components/peripherals/misc_io && ./build/build.sh package middleware/ros2/peripherals/misc_io` |
| 列出组件测试 | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test list components/peripherals/misc_io` |
| 跑组件 PR 测试 | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test run components/peripherals/misc_io --scope pr` |
| 列出 ROS 2 测试 | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test list middleware/ros2/peripherals/misc_io` |
| 跑 ROS 2 PR 测试 | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test run middleware/ros2/peripherals/misc_io --scope pr` |
| 跑硬件 smoke | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test run components/peripherals/misc_io --scope manual` |
