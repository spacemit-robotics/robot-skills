# Peripheral Testing

Read this reference when the user explicitly asks to test, validate CI/PR behavior, run regression, or perform a hardware smoke check.

## Choose Evidence

| Path | Purpose | Hardware |
| --- | --- | --- |
| Native example or ROS 2 node | Normal user workflow and integration | Often required |
| Native API contract | Public API, functional behavior, error paths with fakes | Usually not required |
| ROS 2 contract | Parameters, messages/services, mapping, error paths with fakes | Usually not required |
| Hardware smoke | Real transport and device behavior | Required and supervised |

Contract success does not prove physical wiring or hardware behavior. A successful example on one device does not replace the other layer's contract.

## Use test.yaml and robot-test

1. Inspect both `components/peripherals/<name>/test.yaml` and `middleware/ros2/peripherals/<name>/test.yaml`.
2. For explicit test/CI/regression requests, list the module tests before running them.
3. Start with `--scope pr` unless the user requests scheduled or manual coverage.
4. Run native and ROS 2 modules separately so the failing layer is visible.
5. Use `scripts/test/robot-test` only for these explicit test workflows, not ordinary example/node execution.

Do not run a `manual` test merely because it is present in `test.yaml`.

## Hardware Smoke Gate

Before a hardware smoke test, confirm:

- the required model and transport match the test manifest;
- the user can supervise interactive actions;
- state-changing and network-disrupting effects are accepted;
- required environment variables are set from observed device configuration;
- a timeout and cleanup path are available.

Missing hardware or supervision means hardware verification is skipped, not PASS.

## Report Results

Record each layer independently using:

```text
layer, module, test or command, execution location, exit status,
key output, logs/artifacts, skipped prerequisites, first failure
```

Return the actual command and output evidence. Do not summarize a nonzero exit as success because some subchecks passed.
