---
name: spacemit-robot-pm
description: >-
  components/peripherals/pm 与 middleware/ros2/peripherals/pm 的构建、PR
  测试、电源状态硬件 smoke 与 ROS 2 PowerStatus/SetPowerSwitch 验证入口。
metadata:
  requires:
    bins: ["bash"]
  sdk:
    module_paths:
      - components/peripherals/pm
      - middleware/ros2/peripherals/pm
    primary_docs:
      - components/peripherals/pm/README.md
      - components/peripherals/pm/test.yaml
      - components/peripherals/pm/package.xml
      - middleware/ros2/peripherals/pm/README.md
      - middleware/ros2/peripherals/pm/test.yaml
      - middleware/ros2/peripherals/pm/package.xml
    build_hint: target_preferred
---

# SpacemiT Robot PM

先按 [`spacemit-robot-shared`](../spacemit-robot-shared/SKILL.md) 确认 SDK 根路径与通用构建规则；无 SDK 就转 [`spacemit-robot-sdk-bootstrap`](../spacemit-robot-sdk-bootstrap/SKILL.md)。

## 何时使用

- 用户要构建、测试或调试 `components/peripherals/pm`。
- 用户要构建、测试或运行 `middleware/ros2/peripherals/pm` 的电源管理节点。
- 用户要验证 power_supply 节点、电量/充电状态、ROS 2 状态话题或电源开关服务。

## 默认规则

- `build_hint`: `target_preferred`
- SDK 内模块路径：`$SPACEMIT_SDK_ROOT/components/peripherals/pm` 与 `$SPACEMIT_SDK_ROOT/middleware/ros2/peripherals/pm`。
- ROS 2 节点依赖底层 PM 组件，构建或调试 ROS 2 前先确认组件层已构建。
- PR 测试使用 fake PM backend；真实 `/sys/class/power_supply/*`、电源插拔和开关控制只走 `manual` scope。
- 当前通用驱动主要读取充电状态与容量；`pm_switch_set` 在 generic 下可能按预期返回不支持。

## 固定流程

1. 确认 `$SPACEMIT_SDK_ROOT` 指向完整 SDK。
2. 在 `$SPACEMIT_SDK_ROOT` 下执行 `source build/envsetup.sh`。
3. 组件构建执行 `./build/build.sh package components/peripherals/pm`。
4. ROS 2 构建先确保组件构建完成，再执行 `./build/build.sh package middleware/ros2/peripherals/pm`。
5. 测试前分别执行 `./scripts/test/robot-test list components/peripherals/pm` 和 `./scripts/test/robot-test list middleware/ros2/peripherals/pm`。
6. PR 验证分别执行 `./scripts/test/robot-test run components/peripherals/pm --scope pr` 与 `./scripts/test/robot-test run middleware/ros2/peripherals/pm --scope pr`。
7. 对“帮我跑一下”“帮我测一下”类请求，必须真实执行命令，并返回命令、结果、日志路径和失败点。

## 专项任务

### 构建与 PR 测试

优先先跑组件层，再跑 ROS 2 层。组件层覆盖 init、config、callback、state、switch 和错误路径；ROS 2 层覆盖状态发布、SetPowerSwitch、无效驱动、未配置通道和 backend read error。

### 硬件 smoke

真实硬件测试需要确认 charger/capacity power_supply 节点、读权限和人工插拔条件。电源开关服务可能影响设备供电，执行前必须确认通道含义和风险。

## 禁止事项

- 不要默认写死 target；需要 target 时按 shared 规则确认 board 和 product。
- 不要未经确认调用可能改变设备供电的 switch 服务。
- 不要把 generic 驱动下 `pm_switch_set` 不支持误判为 ROS 2 封装失败。
- 不要只给命令不执行；执行型请求必须真实运行并回传结果。

## 常见任务与命令

| 意图 | 命令 |
| ---- | ---- |
| 构建组件 | `cd "$SPACEMIT_SDK_ROOT" && source build/envsetup.sh && ./build/build.sh package components/peripherals/pm` |
| 构建 ROS 2 节点 | `cd "$SPACEMIT_SDK_ROOT" && source build/envsetup.sh && ./build/build.sh package components/peripherals/pm && ./build/build.sh package middleware/ros2/peripherals/pm` |
| 列出组件测试 | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test list components/peripherals/pm` |
| 跑组件 PR 测试 | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test run components/peripherals/pm --scope pr` |
| 列出 ROS 2 测试 | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test list middleware/ros2/peripherals/pm` |
| 跑 ROS 2 PR 测试 | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test run middleware/ros2/peripherals/pm --scope pr` |
| 跑硬件 smoke | `cd "$SPACEMIT_SDK_ROOT" && ./scripts/test/robot-test run components/peripherals/pm --scope manual` |
