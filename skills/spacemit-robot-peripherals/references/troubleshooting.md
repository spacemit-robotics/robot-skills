# Peripheral Troubleshooting

Read this reference after a failure or when data/state is missing. Diagnose from the lowest layer that can independently prove behavior.

```text
hardware/system -> native driver -> public C API -> staging/install
-> ROS 2 node -> topic/service -> user application
```

| Symptom | Inspect | Conclusion or next action |
| --- | --- | --- |
| UART/I2C/SPI open fails | Device node, permissions, occupancy, address/baud/mode, wiring | Correct the observed transport mismatch; do not assume hardware failure from permission errors |
| GPIO has no event or wrong level | gpiochip/line mapping, board generation, direction, active level, debounce | Correct mapping/configuration before changing callback code |
| Driver not found | Enabled-driver CMake variable, compiled objects, runtime shared library identity | Rebuild the selected driver and prove the loaded library is current |
| Native example fails | README arguments, public error/status code, driver logs | Fix or isolate the native layer before ROS 2 investigation |
| ROS CMake cannot find header/library | Native install/staging, prefix, `CMAKE_PREFIX_PATH` | Build/install native first; avoid hard-coded library paths |
| Node runs but publishes no data | Effective parameters, native example, publisher/topic type, source callback/timer | Locate whether acquisition or publication is absent |
| Topic/service appears missing | Node/namespace, resolved names, interface type, QoS, ROS domain | Correct the observed discovery or naming mismatch |
| Lidar dependency fetch/configure fails | Network and `~/.cache/thirdparty` provenance/age | Confirm before deleting cache, then reconfigure from a clean build directory |
| WiFi action loses visibility | NetworkManager interface state, SSH route, ROS DDS interface/domain | Treat interface loss as expected risk; recover locally or through another link |
| 5G does not reach data state | AT port, SIM readiness, registration, PDP, NCM interface, DHCP | Report the first failed stage; do not collapse modem and IP failures |

## Data Quality

- IMU: confirm sensor model, sample rate, units, mounting transform, and stationary calibration conditions.
- Lidar: confirm model, baud, scan range, received frame count, and ROS `LaserScan` conversion separately.
- Light sensor/PM: compare native reads with the configured I2C or sysfs source before inspecting ROS messages.
- Key/misc IO/LED: verify physical logic and configured line/device before changing event or command mapping.
- NFC: separate tag detection, authentication/device capability, read, and write failures.

Only call a cause verified when command output or source behavior supports it. Preserve the first failing command and its logs.
