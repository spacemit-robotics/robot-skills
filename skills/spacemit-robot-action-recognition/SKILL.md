---
name: spacemit-robot-action-recognition
description: "middleware/ros2/perception/action_recognition 的构建、运行、测试与调试入口"
metadata:
  requires:
    bins: ["bash", "ros2", "colcon"]
  sdk:
    module_paths:
      - middleware/ros2/perception/action_recognition
    primary_docs:
      - middleware/ros2/perception/action_recognition/README.md
      - middleware/ros2/perception/action_recognition/package.xml
    build_hint: single_package_first
---

# SpacemiT Action Recognition

先按 [`../spacemit-robot-shared/SKILL.md`](../spacemit-robot-shared/SKILL.md) 确认 SDK 根路径与通用构建规则；无 SDK 则 [`../spacemit-robot-sdk-bootstrap/SKILL.md`](../spacemit-robot-sdk-bootstrap/SKILL.md)。

## 何时使用

- 用户要构建、运行、测试或调试 `middleware/ros2/perception/action_recognition`。
- 用户需要基于骨架序列进行动作识别（包括摔倒检测）。
- 用户需要实时处理人体姿态关键点数据进行 7 类动作分类。

## 默认规则

- `build_hint`: `single_package_first`
- 模块路径：`$SPACEMIT_SDK_ROOT/middleware/ros2/perception/action_recognition`
- 依赖 `components/model_zoo/vision` 组件、`body_pose` 包和 STGCN 模型文件
- 构建时必须同时编译 `body_pose`，因为需要其消息定义
- 不默认先读总览文档或组件 README；只有命令不清、参数不清或实际执行失败时，才回读 `primary_docs`、头文件或脚本本身。
- 该模块需要时序骨架数据，不支持单帧图像直接识别。

## 固定流程

1. 先确认 SDK 根可用；无 SDK 就转 bootstrap。
2. 在 `$SPACEMIT_SDK_ROOT` 下执行 `source build/envsetup.sh`。
3. 使用 `colcon build --packages-select action_recognition` 构建模块。
4. 需要测试时执行 `scripts/test/robot-test run middleware/ros2/perception/action_recognition --scope pr`。
5. 若构建或运行暴露缺依赖，按报错补装；不要先做脱离上下文的大段依赖排查。
6. 只有当命令细节、参数语义或脚本用法不清，或实际执行失败时，再回读 `primary_docs`。
7. 对"帮我执行 / 帮我测一下 / 跑数据"这类请求，必须真正执行并回传结果，而不只是给命令。

## 专项任务

### 构建组件

```bash
cd "$SPACEMIT_SDK_ROOT/middleware/ros2/perception"
source "$SPACEMIT_SDK_ROOT/build/envsetup.sh"
colcon build --packages-select body_pose action_recognition
source install/setup.bash
```

### 运行节点

```bash
# 订阅 /perception/body_poses，发布 /perception/actions
ros2 run action_recognition action_recognition_node --ros-args \
  -p config_path:="$(ros2 pkg prefix action_recognition)/share/action_recognition/config/stgcn.yaml" \
  -p score_threshold:=0.25 \
  -p sequence_length:=30 \
  -p lazy_load:=true
```

### 运行测试

```bash
cd "$SPACEMIT_SDK_ROOT"
scripts/test/robot-test list middleware/ros2/perception/action_recognition
scripts/test/robot-test run middleware/ros2/perception/action_recognition --scope pr
```

## 禁止事项

- 不要写与本模块无关的通用背景介绍。
- 不要把组件 README、总览文档或长篇 API 说明设为固定前置。
- 不要把运行时必须遵守的关键规则只写在模板、`docs/` 或仓库说明里。
- 不要假设已经选择 target。
- 不要把临时文件或大文件写入 SDK 仓库。

## 常见任务与命令

| 意图 | 动作 |
| ---- | ---- |
| 构建 | `cd "$SPACEMIT_SDK_ROOT/middleware/ros2/perception" && colcon build --packages-select body_pose action_recognition` |
| 运行 | `ros2 run action_recognition action_recognition_node --ros-args -p config_path:=.../config/stgcn.yaml` |
| 测试 | `cd "$SPACEMIT_SDK_ROOT" && scripts/test/robot-test run middleware/ros2/perception/action_recognition --scope pr` |
| 查看话题 | `ros2 topic list \| grep action` |
| 查看参数 | `ros2 param list /action_recognition_node` |
