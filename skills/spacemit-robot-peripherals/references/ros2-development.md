# ROS 2 Peripheral Development

Read this reference for ROS 2 adapter builds, node execution, parameters, topics, services, launch files, or application integration.

## Build Order

Use this dependency order:

```text
native component -> staging/install -> ROS interface generation -> ROS node
```

If configuration reports a missing native header or library, verify the native build/install and `CMAKE_PREFIX_PATH` before changing ROS 2 code. Do not hide a stale or wrong native library by adding hard-coded search paths.

## Discover the Interface

| Need | Read |
| --- | --- |
| Defaults and device selection | `params/*.yaml` and node parameter declarations |
| Published/subscribed data | `msg/*.msg`, standard message type, and node source |
| Actions with responses | `srv/*.srv` and node source |
| Launch overrides | `launch/*.launch.py` |
| Package/executable/dependencies | `package.xml`, `CMakeLists.txt`, README |

Some adapters use standard messages instead of local `msg/` files: verify the publisher type in the README or source. Do not copy a topic, QoS policy, parameter, or service type from another peripheral package.

## Run and Verify

1. Source the environment containing both the native library and ROS 2 package.
2. Load the selected params file or explicit overrides from the module README.
3. Start the documented executable or launch file on the board.
4. Verify the node and effective parameters.
5. Inspect topic type/publishers/subscribers before `echo` or `hz`.
6. Inspect a service type before calling it; confirm state-changing calls first.
7. Correlate ROS output with native evidence when data is absent or implausible.

Useful inspection primitives include `ros2 node list/info`, `ros2 param dump`, `ros2 topic info/echo/hz`, `ros2 service type/call`, and launch help/argument inspection. Derive complete commands from the selected ROS 2 README.

## Change the Adapter

- Parameters and defaults: `params/` plus declarations in `src/*node*`.
- Message/service schema: `msg/` or `srv/`, then regenerate interfaces and update contract fakes.
- Runtime mapping: `src/*node*`.
- Launch behavior: `launch/`.
- Adapter contracts: `tests/` and `test.yaml`.

Keep hardware policy in the native layer unless it is genuinely a ROS-facing configuration or interface concern.
