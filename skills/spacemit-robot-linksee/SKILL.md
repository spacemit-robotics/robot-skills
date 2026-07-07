---
name: spacemit-robot-linksee
description: >-
  application/ros2/linksee 的整机构建、ROS2 底盘/雷达/SLAM/Nav2/巡航/语音控制、
  linksee_app、端到端推理、感知抓取与 RTSP 示例入口。
metadata:
  requires:
    bins: ["bash", "ros2"]
  sdk:
    module_paths:
      - application/ros2/linksee
    primary_docs:
      - application/ros2/linksee/README.md
      - application/ros2/linksee/package.xml
      - application/ros2/linksee/linksee_app/README.md
      - application/ros2/linksee/linksee_app/package.xml
      - application/ros2/linksee/perceptive_grasp/README.md
      - application/ros2/linksee/perceptive_grasp/package.xml
      - application/ros2/linksee/rtsp_detection/README.md
      - application/ros2/linksee/rtsp_tracking/README.md
    build_hint: target_required
---

# SpacemiT Robot Linksee

先按 [`spacemit-robot-shared`](../spacemit-robot-shared/SKILL.md) 确认 SDK 根路径、执行模式和 target；无完整 SDK 时转 [`spacemit-robot-sdk-bootstrap`](../spacemit-robot-sdk-bootstrap/SKILL.md)。

## 何时使用

- 用户要构建、运行、测试或调试 `application/ros2/linksee`。
- 用户要启动 Linksee 底盘、雷达、里程计、SLAM 建图、RGB-D SLAM、Nav2 导航、自动巡航或语音控制。
- 用户要处理 `linksee_app`、`linksee_native`、`linksee_device`、`LinkseeHost/LinkseeClient`、MCP/Hermes 自然语言控制、`perceptive_grasp`、`rtsp_detection` 或 `rtsp_tracking`。

## 默认规则

- `build_hint`: `target_required`。先按 shared 规则确认 board 和 target；只有用户或 target 匹配明确时才使用 `k3-com260-linksee`，不要默认写死。
- SDK 内模块路径：`$SROBOTIS_ROOT/application/ros2/linksee`。
- 运行端默认是 K3 板端；PC 端只做 RViz 可视化、遥操作、训练或远程客户端。
- ROS2 运行终端都要先执行 `source "$SROBOTIS_ROOT/output/staging/setup.bash"`；构建终端先执行 `source build/envsetup.sh`。
- 参考文档中的复现小节是原子流程：同一小节内的命令必须按原顺序作为一个整体处理，不要拆开、重排或只执行中间一步，除非用户明确要求单步调试。
- 只有命令细节、参数语义或失败点不清时，才回读 `primary_docs` 或 `docs-ros/zh/k3/03-参考方案/3.2-轮式机器人Linksee.md`。

## 固定流程

1. 确认 `$SROBOTIS_ROOT` 指向完整 SDK，至少包含 `build/`、`application/`、`components/`、`middleware/`、`target/`。
2. 在 SDK 根目录执行 `source build/envsetup.sh`，按 shared 规则确认并 `lunch <target>`。
3. 整机方案构建优先执行 `m`；只改 `linksee` 应用时，可在 target 环境下进入模块目录执行 `mm`。
4. 运行前确认底盘、雷达、IMU、相机、机械臂、音频设备和 `/dev/ttyACM*`、`/dev/video*`、`/dev/rpmsg*` 权限。
5. 涉及机器人运动时，先确认现场安全、急停手段和人工监看；不要在无人确认时启动巡航、导航、抓取或端到端推理。
6. 执行型请求必须真实执行命令，并返回命令、关键日志、话题或设备检查结果，以及失败点。

## 构建

```bash
cd "$SROBOTIS_ROOT"
source build/envsetup.sh
lunch <target>
m
```

只构建主应用包：

```bash
cd "$SROBOTIS_ROOT"
source build/envsetup.sh
lunch <target>
cd application/ros2/linksee
mm
```

构建 `linksee_app` 前先构建 `mlink device` 依赖：

```bash
cd "$SROBOTIS_ROOT"
source build/envsetup.sh
lunch <target>
cd components/agent_tools/mlink_device
mm
cd "$SROBOTIS_ROOT/application/ros2/linksee/linksee_app"
mm
```

## 测试入口

当前源码树没有 `application/ros2/linksee/test.yaml` 时，不要伪造 robot-test 结果；先说明缺少测试定义，再按用户目标执行构建或对应流程冒烟验证。

```bash
cd "$SROBOTIS_ROOT"
if test -f application/ros2/linksee/test.yaml; then
  ./scripts/test/robot-test list application/ros2/linksee
  ./scripts/test/robot-test run application/ros2/linksee --scope pr
else
  echo "missing application/ros2/linksee/test.yaml"
fi
```

## 整机流程

下面每个小节都是不可拆分流程。每条 launch 通常在独立终端运行；每个板端终端都先加载 staging 环境。

### SLAM 建图

```bash
source "$SROBOTIS_ROOT/output/staging/setup.bash"
ros2 launch linksee base_control_esos.launch.py

source "$SROBOTIS_ROOT/output/staging/setup.bash"
ros2 launch linksee start_ydlidar.launch.py

source "$SROBOTIS_ROOT/output/staging/setup.bash"
ros2 launch cartographer_run cartographer_2d.launch.py

source "$SROBOTIS_ROOT/output/staging/setup.bash"
ros2 run teleop_twist_keyboard teleop_twist_keyboard

source ~/visual_ws/install/setup.bash
ros2 launch visualization display_slam.launch.py

source /opt/ros/humble/setup.bash
ros2 run nav2_map_server map_saver_cli -f my_map
```

### RGB-D 视觉 SLAM

```bash
sudo apt install 'ros-humble-rtabmap*' ros-humble-aruco-markers-msgs

source "$SROBOTIS_ROOT/output/staging/setup.bash"
ros2 launch linksee base_control_esos.launch.py

source "$SROBOTIS_ROOT/output/staging/setup.bash"
ros2 launch linksee start_ydlidar.launch.py

source "$SROBOTIS_ROOT/output/staging/setup.bash"
ros2 launch linksee start_odom.launch.py

source "$SROBOTIS_ROOT/output/staging/setup.bash"
ros2 launch realsense2_camera rs_launch.py camera_namespace:=/

source "$SROBOTIS_ROOT/output/staging/setup.bash"
ros2 launch rtabmap_run rgbd_slam.launch.py

source ~/visual_ws/install/setup.bash
ros2 launch visualization display_rgbd.launch.py

source "$SROBOTIS_ROOT/output/staging/setup.bash"
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

### Nav2 导航

导航前先把 `my_map` 地图放到 `$SROBOTIS_ROOT/middleware/ros2/planning/nav2/map`，重新 `lunch` 并全量 `m`，且让小车回到建图起点。

```bash
source "$SROBOTIS_ROOT/output/staging/setup.bash"
ros2 launch linksee base_control_esos.launch.py

source "$SROBOTIS_ROOT/output/staging/setup.bash"
ros2 launch linksee start_ydlidar.launch.py

source "$SROBOTIS_ROOT/output/staging/setup.bash"
ros2 launch linksee start_odom.launch.py

source "$SROBOTIS_ROOT/output/staging/setup.bash"
ros2 launch nav2 nav2.launch.py

source ~/visual_ws/install/setup.bash
ros2 launch visualization display_navigation.launch.py
```

### 自动巡航

巡航复用 Nav2 前置条件，并需要至少 `2*2m` 安全空间。

```bash
source "$SROBOTIS_ROOT/output/staging/setup.bash"
ros2 launch linksee base_control_esos.launch.py

source "$SROBOTIS_ROOT/output/staging/setup.bash"
ros2 launch linksee start_ydlidar.launch.py

source "$SROBOTIS_ROOT/output/staging/setup.bash"
ros2 launch linksee start_odom.launch.py

source "$SROBOTIS_ROOT/output/staging/setup.bash"
ros2 launch nav2 nav2.launch.py

source "$SROBOTIS_ROOT/output/staging/setup.bash"
ros2 run nav2 autonomous_patrol

source "$SROBOTIS_ROOT/output/staging/setup.bash"
ros2 topic pub --once /square_waypoints_enable std_msgs/msg/Bool "{data: true}"

source ~/visual_ws/install/setup.bash
ros2 launch visualization display_navigation.launch.py
```

### 语音控制小车

```bash
source "$SROBOTIS_ROOT/output/staging/setup.bash"
ros2 launch linksee base_control_esos.launch.py

source "$SROBOTIS_ROOT/output/staging/setup.bash"
ros2 launch linksee start_ydlidar.launch.py

source "$SROBOTIS_ROOT/output/staging/setup.bash"
ros2 launch linksee start_odom.launch.py

source "$SROBOTIS_ROOT/output/staging/setup.bash"
ros2 launch linksee voice_cmd.launch.py

source "$SROBOTIS_ROOT/output/staging/setup.bash"
ros2 run linksee voice_dispatcher_node.py

source "$SROBOTIS_ROOT/output/staging/setup.bash"
ros2 run linksee asr_node.py -r 48000
```

## linksee_app 与自然语言控制

- 先准备模型、数据集、相机和机械臂设备索引，再启动 host 或推理。
- 直接验证工具时，按 `tool-start-host` → `tool-start-inference` → `tool-stop-inference` → `tool-stop-host` 顺序执行。
- 接入 MCP/Hermes 时，先启动 `mlink gateway`，再启动 `linksee_device unix linksee`，最后用 `mlink gateway tools` 确认 `linksee.start_host`、`linksee.start_inference`、`linksee.stop_host`、`linksee.stop_inference` 已注册。

```bash
cd "$SROBOTIS_ROOT"
source build/envsetup.sh
m_env_build application/ros2/linksee/linksee_app

linksee_native tool-start-host
linksee_native tool-start-inference
linksee_native tool-stop-inference
linksee_native tool-stop-host

m_env_build components/agent_tools/mlink_gateway
source output/envs/mlink-gateway/bin/activate
mlink gateway restart
linksee_device unix linksee
mlink gateway tools
```

## 感知抓取

按 `perceptive_grasp/README.md` 和参考文档 10.3 的顺序执行：准备 Python 虚拟环境、构建 vision/grasp/manipulator 依赖、准备模型、运行环境检查、必要时手眼标定，最后再运行抓取或语音模式。前一步失败时不要继续后续步骤。

```bash
cd "$SROBOTIS_ROOT/application/ros2/linksee/perceptive_grasp"
source "$SROBOTIS_ROOT/build/envsetup.sh"
source ~/.venv-grasp/bin/activate
python3 scripts/check_runtime_env.py --config config/grasp_pipeline.yaml

cd "$SROBOTIS_ROOT/application/ros2/linksee/perceptive_grasp/build"
source "$SROBOTIS_ROOT/build/envsetup.sh"
./perceptive_grasp --config ../config/grasp_pipeline.yaml --target banana
```

语音模式：

```bash
cd "$SROBOTIS_ROOT/application/ros2/linksee/perceptive_grasp"
source "$SROBOTIS_ROOT/build/envsetup.sh"
source ~/.venv-grasp/bin/activate
python3 scripts/local_voice_bridge.py \
  --config config/grasp_pipeline.yaml \
  --binary build/perceptive_grasp
```

## RTSP 示例

`rtsp_detection` 和 `rtsp_tracking` 都先构建 MPP 与 Vision，下载 YOLOv8 模型，再按各自 README 运行。设备号必须按实际 `v4l2-ctl --list-devices` 修改，不要默认相信 `/dev/video1`。

```bash
cd "$SROBOTIS_ROOT"
source build/envsetup.sh
mm components/multimedia/mpp
mm components/model_zoo/vision
cd components/model_zoo/vision/examples/yolov8
bash scripts/download_models.sh
```

## 禁止事项

- 不要把参考文档同一复现小节里的命令拆开作为独立方案推荐。
- 不要默认写死 target、串口、相机索引、`ROS_DOMAIN_ID` 或 Host IP。
- 不要在没有硬件和人工监看的情况下启动导航、巡航、抓取或端到端推理。
- 不要在缺少 `test.yaml`、缺少硬件或缺少模型时伪造测试通过。
- 不要把模型、数据集、地图、日志或临时大文件提交到 SDK。

## 常见任务与命令

| 意图 | 动作 |
| ---- | ---- |
| 整机构建 | `cd "$SROBOTIS_ROOT" && source build/envsetup.sh && lunch <target> && m` |
| 单包构建 | `cd "$SROBOTIS_ROOT" && source build/envsetup.sh && lunch <target> && cd application/ros2/linksee && mm` |
| 检查测试定义 | `test -f "$SROBOTIS_ROOT/application/ros2/linksee/test.yaml"` |
| 底盘启动 | `source "$SROBOTIS_ROOT/output/staging/setup.bash" && ros2 launch linksee base_control_esos.launch.py` |
| 雷达启动 | `source "$SROBOTIS_ROOT/output/staging/setup.bash" && ros2 launch linksee start_ydlidar.launch.py` |
| 里程计启动 | `source "$SROBOTIS_ROOT/output/staging/setup.bash" && ros2 launch linksee start_odom.launch.py` |
| 导航启动 | `source "$SROBOTIS_ROOT/output/staging/setup.bash" && ros2 launch nav2 nav2.launch.py` |
| linksee_app 构建 | `cd "$SROBOTIS_ROOT/application/ros2/linksee/linksee_app" && mm` |
| 感知抓取检查 | `python3 scripts/check_runtime_env.py --config config/grasp_pipeline.yaml` |
| RTSP 设备检查 | `v4l2-ctl --list-devices` |
