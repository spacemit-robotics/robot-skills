---
name: spacemit-robot-key
description: >-
  components/peripherals/key 与 middleware/ros2/peripherals/key 的构建、PR
  测试、GPIO 按键硬件 smoke 与 ROS 2 事件话题验证入口。
metadata:
  requires:
    bins: ["bash"]
  sdk:
    module_paths:
      - components/peripherals/key
      - middleware/ros2/peripherals/key
    primary_docs:
      - components/peripherals/key/README.md
      - components/peripherals/key/test.yaml
      - components/peripherals/key/package.xml
      - middleware/ros2/peripherals/key/README.md
      - middleware/ros2/peripherals/key/test.yaml
      - middleware/ros2/peripherals/key/package.xml
    build_hint: target_preferred
---

# SpacemiT Robot Key

先按 [`spacemit-robot-shared`](../spacemit-robot-shared/SKILL.md) 确认 SDK 根路径与通用构建规则；无 SDK 就转 [`spacemit-robot-sdk-bootstrap`](../spacemit-robot-sdk-bootstrap/SKILL.md)。

## 何时使用

- 用户要构建、测试或调试 `components/peripherals/key`。
- 用户要构建、测试或运行 `middleware/ros2/peripherals/key` 的按键事件节点。
- 用户要验证 GPIO 按键的按下、释放、单击、双击、长按或长按连发事件。

## 默认规则

- `build_hint`: `target_preferred`
- SDK 内模块路径：`$SPACEMIT_SDK_ROOT/components/peripherals/key` 与 `$SPACEMIT_SDK_ROOT/middleware/ros2/peripherals/key`。
- ROS 2 节点依赖底层 key 组件，构建或调试 ROS 2 前先确认组件层已构建。
- PR 测试使用 fake gpiod；真实 `/dev/gpiochip*`、GPIO 编号、按键操作只走 `manual` scope。
- 多按键 ROS 2 参数数组必须等长；数组不等长、GPIO 无效或权限不足应作为失败点返回。

## 固定流程

1. 确认 `$SPACEMIT_SDK_ROOT` 指向完整 SDK。
2. 在 `$SPACEMIT_SDK_ROOT` 下执行 `source build/envsetup.sh`。
3. 组件构建执行 `./build/build.sh package components/peripherals/key`。
4. ROS 2 构建先确保组件构建完成，再执行 `./build/build.sh package middleware/ros2/peripherals/key`。
5. 测试前分别执行 `./scripts/test/robot-test list components/peripherals/key` 和 `./scripts/test/robot-test list middleware/ros2/peripherals/key`。
6. PR 验证分别执行 `./scripts/test/robot-test run components/peripherals/key --scope pr` 与 `./scripts/test/robot-test run middleware/ros2/peripherals/key --scope pr`。
7. 对“帮我跑一下”“帮我测一下”类请求，必须真实执行命令，并返回命令、结果、日志路径和失败点。

## 专项任务

### 构建与 PR 测试

优先先跑组件层，再跑 ROS 2 层。组件层覆盖 key service、add/remove、事件回调和错误路径；ROS 2 层覆盖底层回调到 `KeyEvent` 的转换与参数校验。

### 硬件 smoke

真实硬件测试需要确认 GPIO 编号、有效电平、`/dev/gpiochip*` 权限和人工按键操作。没有权限或无人操作时，不要伪造硬件结果。

## 禁止事项

- 不要默认写死 target；需要 target 时按 shared 规则确认 board 和 product。
- 不要把 GPIO 编号从物理引脚号直接猜成 Linux GPIO 号。
- 不要在无硬件或无人操作时运行 manual smoke。
- 不要只给命令不执行；执行型请求必须真实运行并回传结果。

## 常见任务与命令

| 意图 | 命令 |
| ---- | ---- |
| 构建组件 | `cd "$SPACEMIT_SDK_ROOT" && source build/envsetup.sh && ./build/build.sh package components/peripherals/key` |
| 构建 ROS 2 节点 | `cd "$SPACEMIT_SDK_ROOT" && source build/envsetup.sh && ./build/build.sh package components/peripherals/key && ./build/build.sh package middleware/ros2/peripherals/key` |
| 列出组件测试 | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test list components/peripherals/key` |
| 跑组件 PR 测试 | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test run components/peripherals/key --scope pr` |
| 列出 ROS 2 测试 | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test list middleware/ros2/peripherals/key` |
| 跑 ROS 2 PR 测试 | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test run middleware/ros2/peripherals/key --scope pr` |
| 跑硬件 smoke | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test run components/peripherals/key --scope manual` |
