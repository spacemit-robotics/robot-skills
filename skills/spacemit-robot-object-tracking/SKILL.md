---
name: spacemit-robot-object-tracking
description: "middleware/ros2/perception/object_tracking 的构建、运行、测试与调试入口"
metadata:
  requires:
    bins: ["bash", "ros2", "colcon"]
  sdk:
    module_paths:
      - middleware/ros2/perception/object_tracking
    primary_docs:
      - middleware/ros2/perception/object_tracking/README.md
      - middleware/ros2/perception/object_tracking/package.xml
    build_hint: single_package_first
---

# SpacemiT Object Tracking

先按 [`../spacemit-robot-shared/SKILL.md`](../spacemit-robot-shared/SKILL.md) 确认 SDK 根路径与通用构建规则；无 SDK 则 [`../spacemit-robot-sdk-bootstrap/SKILL.md`](../spacemit-robot-sdk-bootstrap/SKILL.md)。

## 何时使用

- 用户要构建、运行、测试或调试 `middleware/ros2/perception/object_tracking`。
- 用户需要进行多目标持续跟踪。
- 用户需要使用 ByteTrack 或 OC-SORT 追踪算法。
- 用户需要输出带 track_id 的目标追踪结果。

## 默认规则

- `build_hint`: `single_package_first`
- 模块路径：`$SPACEMIT_SDK_ROOT/middleware/ros2/perception/object_tracking`
- 依赖 `components/model_zoo/vision` 组件和 YOLOv8 模型文件
- 不默认先读总览文档或组件 README；只有命令不清、参数不清或实际执行失败时，才回读 `primary_docs`、头文件或脚本本身。
- 该模块支持 ByteTrack 和 OC-SORT 两种追踪算法，不支持跨摄像头追踪。

## 固定流程

1. 先确认 SDK 根可用；无 SDK 就转 bootstrap。
2. 在 `$SPACEMIT_SDK_ROOT` 下执行 `source build/envsetup.sh`。
3. 使用 `colcon build --packages-select object_tracking` 构建模块。
4. 需要测试时执行 `scripts/test/robot-test run middleware/ros2/perception/object_tracking --scope pr`。
5. 若构建或运行暴露缺依赖，按报错补装；不要先做脱离上下文的大段依赖排查。
6. 只有当命令细节、参数语义或脚本用法不清，或实际执行失败时，再回读 `primary_docs`。
7. 对"帮我执行 / 帮我测一下 / 跑数据"这类请求，必须真正执行并回传结果，而不只是给命令。

## 专项任务

### 构建组件

```bash
cd "$SPACEMIT_SDK_ROOT/middleware/ros2/perception"
source "$SPACEMIT_SDK_ROOT/build/envsetup.sh"
colcon build --packages-select object_tracking
source install/setup.bash
```

### 运行节点

```bash
# 使用默认配置（ByteTrack）
ros2 launch object_tracking object_tracking.launch.py

# ByteTrack
ros2 run object_tracking object_tracking_node --ros-args \
  -p config_path:="$(ros2 pkg prefix object_tracking)/share/object_tracking/config/bytetrack.yaml" \
  -p tracker_type:=bytetrack \
  -p score_threshold:=0.25 \
  -p use_camera:=false \
  -p lazy_load:=true

# OC-SORT
ros2 run object_tracking object_tracking_node --ros-args \
  -p config_path:="$(ros2 pkg prefix object_tracking)/share/object_tracking/config/ocsort.yaml" \
  -p tracker_type:=ocsort \
  -p score_threshold:=0.25 \
  -p use_camera:=false \
  -p lazy_load:=true
```

### 视频测试（无相机时）

```bash
# 终端 1：发布视频帧
ros2 run object_tracking publish_video /path/to/video.mp4

# 终端 2：启动追踪节点
ros2 launch object_tracking object_tracking.launch.py
```

### 运行测试

```bash
cd "$SPACEMIT_SDK_ROOT"
scripts/test/robot-test list middleware/ros2/perception/object_tracking
scripts/test/robot-test run middleware/ros2/perception/object_tracking --scope pr
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
| 构建 | `cd "$SPACEMIT_SDK_ROOT/middleware/ros2/perception" && colcon build --packages-select object_tracking` |
| 运行 ByteTrack | `ros2 run object_tracking object_tracking_node --ros-args -p tracker_type:="bytetrack"` |
| 运行 OC-SORT | `ros2 run object_tracking object_tracking_node --ros-args -p tracker_type:="ocsort"` |
| 测试 | `cd "$SPACEMIT_SDK_ROOT" && scripts/test/robot-test run middleware/ros2/perception/object_tracking --scope pr` |
| 查看话题 | `ros2 topic list \| grep tracking` |
| 查看参数 | `ros2 param list /object_tracking_node` |
| 视频测试 | `ros2 run object_tracking publish_video /path/to/video.mp4` |
| 查看追踪结果 | `ros2 run object_tracking simple_image_viewer /object_tracking/debug_image` |
