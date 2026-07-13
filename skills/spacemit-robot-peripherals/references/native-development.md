# Native Peripheral Development

Read this reference for native builds, examples, C API integration, driver selection, or component source changes.

## Prepare

1. Use the base skills to resolve mode, `SROBOTIS_ROOT`, board, and target.
2. Read the selected component README and `CMakeLists.txt` to identify dependencies and the exact enabled-driver variable.
3. Check the transport before building: device node, address or baud/mode, permissions, occupancy, system service, and real hardware model.
4. Hand the build decision to `spacemit-robot-build`. Peripheral modules are `target_preferred`; a standalone CMake path in a README does not override the active SDK mode.

Common driver choices include IMU I2C/SPI/UART drivers, LED generic/WS2812 drivers, lidar YDLIDAR/RPLIDAR drivers, NFC SI512, and PM generic/ADC backends. Read the current driver directory and CMake logic rather than memorizing option strings.

## Integrate the C API

Most device-handle APIs follow:

```text
select transport and driver -> allocate -> initialize/configure
-> read/write/start/callback -> stop/deinitialize/free
```

Key uses a global service plus key handles, and WiFi uses a global manager API. Always read the public header and error/status definitions before writing an application. Use the example to verify ownership, cleanup, callbacks, units, and default assumptions.

## Run an Example

1. Read the example source and its README instructions.
2. Confirm every hardware argument and side effect.
3. Build the selected driver and example.
4. Run on the board with a bounded duration when the example loops.
5. Report exit status, observed samples/state, cleanup, and logs. Do not treat “process started” as functional success.

## Change Native Source

| Concern | Source location |
| --- | --- |
| Public API and ABI | `components/peripherals/<name>/include/` |
| Core abstraction and registry | `components/peripherals/<name>/src/` |
| Hardware/backend implementation | `components/peripherals/<name>/src/drivers/` |
| User workflow | `example/` or `test/` |
| Functional/error contracts | `tests/` |
| Dependencies | `package.xml` |
| Driver enablement | `CMakeLists.txt` |

For a new driver, preserve the public API where possible, register it through the component's existing mechanism, add fake-backed contract coverage, and expose new ROS 2 configuration only when the adapter needs a user-visible choice.
