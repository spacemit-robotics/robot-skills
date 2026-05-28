---
name: spacemit-robot-yolo-general
description: "middleware/ros2/perception/yolo_general 的构建、运行、测试与调试入口"
metadata:
  requires:
    bins: ["bash", "ros2", "colcon"]
  sdk:
    module_paths:
      - middleware/ros2/perception/yolo_general
    primary_docs:
      - middleware/ros2/perception/yolo_general/README.md
      - middleware/ros2/perception/yolo_general/test.yaml
      - middleware/ros2/perception/yolo_general/package.xml
    build_hint: single_package_first
---

# SpacemiT YOLO General

先按 [`spacemit-robot-shared`](../spacemit-robot-shared/SKILL.md) 确认 SDK 根路径与通用构建规则。无 SDK 则转 [`spacemit-robot-sdk-bootstrap`](../spacemit-robot-sdk-bootstrap/SKILL.md)。

## 何时使用

- 用户要构建、运行、测试或调试 `middleware/ros2/perception/yolo_general`。
- 用户需要进行通用目标检测（COCO 80 类）。
- 用户需要输出标准 Detection2DArray 格式的检测结果。

## 默认规则

- `build_hint`: `single_package_first`
- 模块路径：`$SPACEMIT_SDK_ROOT/middleware/ros2/perception/yolo_general`
- 依赖 `vision` 包（对应组件路径 `components/model_zoo/vision`）和 YOLOv8 模型文件
- 不默认先读总览文档或组件 README；只有命令不清、参数不清或实际执行失败时，才回读 `primary_docs`、头文件或脚本本身。
- 该模块支持 COCO 80 类目标检测，不支持实例分割或关键点检测。

## 固定流程

1. 先确认 SDK 根可用；无 SDK 就转 bootstrap。
2. 在 `$SPACEMIT_SDK_ROOT` 下执行 `source build/envsetup.sh`。
3. 使用 `colcon build --packages-select yolo_general` 构建模块。
4. 需要测试时执行 `scripts/test/robot-test run middleware/ros2/perception/yolo_general --scope pr`。
5. 若构建或运行暴露缺依赖，按报错补装；不要先做脱离上下文的大段依赖排查。
6. 只有当命令细节、参数语义或脚本用法不清，或实际执行失败时，再回读 `primary_docs`。
7. 对"帮我执行 / 帮我测一下 / 跑数据"这类请求，必须真正执行并回传结果，而不只是给命令。

## 专项任务

### 构建组件

```bash
cd "$SPACEMIT_SDK_ROOT/middleware/ros2/perception"
source "$SPACEMIT_SDK_ROOT/build/envsetup.sh"
colcon build --packages-select yolo_general
source install/setup.bash
```

### 运行节点

```bash
ros2 run yolo_general yolo_general_node --ros-args \
  -p config_path:="$(ros2 pkg prefix yolo_general)/share/yolo_general/config/yolov8.yaml" \
  -p score_threshold:=0.25 \
  -p use_camera:=false \
  -p lazy_load:=true
```

### 运行测试

```bash
cd "$SPACEMIT_SDK_ROOT"
scripts/test/robot-test list middleware/ros2/perception/yolo_general
scripts/test/robot-test run middleware/ros2/perception/yolo_general --scope pr
```


### 手跑测试脚本（调试用）

在 `middleware/ros2/perception` 下执行本模块 `tests/` 中的脚本：

```bash
cd "$SPACEMIT_SDK_ROOT/middleware/ros2/perception"
bash yolo_general/tests/test_functional.sh
bash yolo_general/tests/test_invalid_input.sh
bash yolo_general/tests/test_performance.sh
```

scheduled 性能（SDK 根目录）：

```bash
cd "$SPACEMIT_SDK_ROOT"
scripts/test/robot-test run middleware/ros2/perception/yolo_general --scope scheduled --category performance
```

说明：
- scheduled performance 默认测 `init_ms` 与 `first_output_ms`（阈值 5s / 8s）。
- 输入优先使用安装包 `config/yolov8.yaml` 的 `test_image`；缺失时可自动下载同名资源，无法获取时回退 synthetic。
- 传 `--image` 时发布脚本启用 strict image 模式（图片不可读会直接失败，而不是静默回退）。
- 指标产物默认写到 `middleware/ros2/perception/perception_perf_yolo_general.txt`（`robot-test` 按 `test.yaml` 收集）。

## 禁止事项

- 不要写与本模块无关的通用背景介绍。
- 不要把组件 README、总览文档或长篇 API 说明设为固定前置。
- 不要把运行时必须遵守的关键规则只写在模板、`docs/` 或仓库说明里。
- 不要假设已经选择 target。
- 不要把临时文件或大文件写入 SDK 仓库。

## 常见任务与命令

| 意图 | 动作 |
| ---- | ---- |
| 构建 | `cd "$SPACEMIT_SDK_ROOT/middleware/ros2/perception" && colcon build --packages-select yolo_general` |
| 运行 | `ros2 run yolo_general yolo_general_node --ros-args -p config_path:=.../config/yolov8.yaml -p use_camera:=false` |
| 手跑 PR 测试 | `cd "$SPACEMIT_SDK_ROOT/middleware/ros2/perception" && bash yolo_general/tests/test_functional.sh` |
| 测试 | `cd "$SPACEMIT_SDK_ROOT" && scripts/test/robot-test run middleware/ros2/perception/yolo_general --scope pr` |
| 查看话题 | `ros2 topic list \| grep yolo` |
| 查看参数 | `ros2 param list /yolo_general_node` |
