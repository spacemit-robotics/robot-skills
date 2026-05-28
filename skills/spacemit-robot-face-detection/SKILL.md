---
name: spacemit-robot-face-detection
description: "middleware/ros2/perception/face_detection 的构建、运行、测试与调试入口"
metadata:
  requires:
    bins: ["bash", "ros2", "colcon"]
  sdk:
    module_paths:
      - middleware/ros2/perception/face_detection
    primary_docs:
      - middleware/ros2/perception/face_detection/README.md
      - middleware/ros2/perception/face_detection/test.yaml
      - middleware/ros2/perception/face_detection/package.xml
    build_hint: single_package_first
---

# SpacemiT Face Detection

先按 [`spacemit-robot-shared`](../spacemit-robot-shared/SKILL.md) 确认 SDK 根路径与通用构建规则。无 SDK 则转 [`spacemit-robot-sdk-bootstrap`](../spacemit-robot-sdk-bootstrap/SKILL.md)。

## 何时使用

- 用户要构建、运行、测试或调试 `middleware/ros2/perception/face_detection`。
- 用户需要进行实时人脸检测。
- 用户需要输出标准 Detection2DArray 格式的人脸检测结果。

## 默认规则

- `build_hint`: `single_package_first`
- 模块路径：`$SPACEMIT_SDK_ROOT/middleware/ros2/perception/face_detection`
- 依赖 `vision` 包（对应组件路径 `components/model_zoo/vision`）和对应的人脸检测模型文件
- 不默认先读总览文档或组件 README；只有命令不清、参数不清或实际执行失败时，才回读 `primary_docs`、头文件或脚本本身。
- 该模块仅支持人脸检测，不支持人脸识别或人脸特征提取。

## 固定流程

1. 先确认 SDK 根可用；无 SDK 就转 bootstrap。
2. 在 `$SPACEMIT_SDK_ROOT` 下执行 `source build/envsetup.sh`。
3. 在 `middleware/ros2/perception` 下 `colcon build --packages-select face_detection`（与 CI 测试一致）。
4. 需要测试时执行 `scripts/test/robot-test run middleware/ros2/perception/face_detection --scope pr`。
5. 若构建或运行暴露缺依赖，按报错补装；不要先做脱离上下文的大段依赖排查。
6. 只有当命令细节、参数语义或脚本用法不清，或实际执行失败时，再回读 `primary_docs`。
7. 对"帮我执行 / 帮我测一下 / 跑数据"这类请求，必须真正执行并回传结果，而不只是给命令。

## 专项任务

### 构建组件

```bash
cd "$SPACEMIT_SDK_ROOT/middleware/ros2/perception"
source "$SPACEMIT_SDK_ROOT/build/envsetup.sh"
colcon build --packages-select face_detection
source install/setup.bash
```

### 运行节点

```bash
# 订阅图像话题（模型路径在 config yaml 内）
ros2 run face_detection face_detection_node --ros-args \
  -p config_path:="$(ros2 pkg prefix face_detection)/share/face_detection/config/yolov5-face.yaml" \
  -p score_threshold:=0.3 \
  -p use_camera:=false \
  -p lazy_load:=true
```

### 运行测试

```bash
cd "$SPACEMIT_SDK_ROOT"
scripts/test/robot-test list middleware/ros2/perception/face_detection
scripts/test/robot-test run middleware/ros2/perception/face_detection --scope pr
```


### 手跑测试脚本（调试用）

在 `middleware/ros2/perception` 下执行本模块 `tests/` 中的脚本：

```bash
cd "$SPACEMIT_SDK_ROOT/middleware/ros2/perception"
bash face_detection/tests/test_functional.sh
bash face_detection/tests/test_invalid_input.sh
bash face_detection/tests/test_performance.sh
```

scheduled 性能（SDK 根目录）：

```bash
cd "$SPACEMIT_SDK_ROOT"
scripts/test/robot-test run middleware/ros2/perception/face_detection --scope scheduled --category performance
```

说明：
- scheduled performance 默认测 `init_ms` 与 `first_output_ms`（阈值 5s / 8s）。
- 启动前若模型不存在会直接失败（不再 SKIP）。
- 输入优先使用 yaml 中 `test_image`；有 `--image` 时发布脚本启用 strict image 模式，图片不可读会直接失败。

## 禁止事项

- 不要写与本模块无关的通用背景介绍。
- 不要把组件 README、总览文档或长篇 API 说明设为固定前置。
- 不要把运行时必须遵守的关键规则只写在模板、`docs/` 或仓库说明里。
- 不要假设已经选择 target。
- 不要把临时文件或大文件写入 SDK 仓库。

## 常见任务与命令

| 意图 | 动作 |
| ---- | ---- |
| 构建 | `cd "$SPACEMIT_SDK_ROOT/middleware/ros2/perception" && colcon build --packages-select face_detection` |
| 运行 | `ros2 run face_detection face_detection_node --ros-args -p config_path:=.../config/yolov5-face.yaml -p use_camera:=false` |
| 手跑 PR 测试 | `cd "$SPACEMIT_SDK_ROOT/middleware/ros2/perception" && bash face_detection/tests/test_functional.sh` |
| 测试 | `cd "$SPACEMIT_SDK_ROOT" && scripts/test/robot-test run middleware/ros2/perception/face_detection --scope pr` |
| 查看话题 | `ros2 topic list \| grep face` |
| 查看参数 | `ros2 param list /face_detection_node` |
