# Device Routing

Use this table to select the module before reading device-specific files. Defaults in examples and YAML files are examples, not portable board configuration.

| Device | Native path | Transport or system | Native example | ROS 2 package / executable | Main risk |
| --- | --- | --- | --- | --- | --- |
| 5G | `components/peripherals/5g` | UART, USB ECM/NCM, `udhcpc` | `test_5g_mr880a` | `peripherals_5g_node` / `modem_5g_node` | Network state and raw AT |
| IMU | `components/peripherals/imu` | I2C, SPI, UART | `test_imu_i2c`, `test_imu_spi`, `test_imu_uart` | `peripherals_imu_node` / `imu_uart_node` | Calibration requires a stationary sensor |
| Key | `components/peripherals/key` | libgpiod | `test_key` | `peripherals_key_node` / `key_node` | GPIO numbering and active level |
| LED | `components/peripherals/led` | sysfs, SPI | `test_led_generic`, `test_led_ws2812` | `peripherals_led_node` / `led_node` | Physical output |
| Lidar | `components/peripherals/lidar` | UART, third-party SDK | `test_lidar_uart` | `peripherals_lidar_node` / `lidar_2d_node` | Powered hardware and cache downloads |
| Light sensor | `components/peripherals/light_sensor` | I2C, W1160 | `test_light_sensor_i2c` | `peripherals_light_sensor_node` / `light_sensor_node` | I2C address and binary dependency |
| Misc IO | `components/peripherals/misc_io` | libgpiod | `test_misc_io` | `peripherals_misc_io_node` / `misc_io_node` | Attached output loads |
| NFC | `components/peripherals/nfc` | I2C, SI512 | `test_nfc_i2c` | `peripherals_nfc_node` / `nfc_node` | Block writes modify a card |
| PM | `components/peripherals/pm` | power_supply, ADC, I2C | `test_pm_generic`, `test_pm_adc` | `peripherals_pm_node` / `pm_node` | Power-switch side effects |
| WiFi | `components/peripherals/wifi` | NetworkManager, `nmcli` | `test_wifi_demo` | `peripherals_wifi_node` / `wifi_node` | SSH and DDS disconnect |

## Select Sources

- Native setup or example: read `components/peripherals/<name>/README.md`, `CMakeLists.txt`, and the matching example source.
- Native application: read the public header before generating code; use the example only to confirm lifecycle and argument semantics.
- ROS 2 task: read `middleware/ros2/peripherals/<name>/README.md`, then only the matching `params/`, `msg/`, `srv/`, `launch/`, or node source.
- Test request: inspect the native and ROS 2 `test.yaml` files separately before choosing scopes.
- Source change: locate the smallest owning layer before editing; do not patch a ROS 2 symptom when the native example already fails.

Never infer command-line arguments, driver names, topic names, service types, or defaults from an executable name. Read the current source.
