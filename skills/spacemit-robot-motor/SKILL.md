---
name: spacemit-robot-motor
description: components/peripherals/motor 的构建、运行、测试、调试与 API 接入入口。
metadata:
  requires:
    bins: ["bash"]
  sdk:
    module_paths:
      - components/peripherals/motor
    primary_docs:
      - components/peripherals/motor/README.md
      - components/peripherals/motor/package.xml
    build_hint: single_package_first
---

# SpacemiT Robot Motor

先按 [`spacemit-robot-shared`](../spacemit-robot-shared/SKILL.md) 确认 SDK 根路径与通用构建规则。

## 何时使用

- 用户要构建、运行、测试或调试 `components/peripherals/motor`。

## 默认规则

- 构建倾向：`single_package_first`。
- SDK 内模块路径：`$SPACEMIT_SDK_ROOT/components/peripherals/motor`。

## 固定流程

1. 确认 `$SPACEMIT_SDK_ROOT` 指向完整 SDK。
2. 在 SDK 根目录执行 `source build/envsetup.sh`。
3. 需要构建时进入模块目录执行 `mm`。
4. 需要测试时执行 `scripts/test/robot-test run components/peripherals/motor`。
5. 执行型请求必须真实运行命令，并返回结果和失败点。

## 专项任务

### 构建组件


### 运行测试
1. **非法参数注入测试**：

   ```bash
   cd "$SPACEMIT_SDK_ROOT" && scripts/test/robot-test run components/peripherals/motor --scope pr
   ```

2. **生产环境兼容性测试**：
需人工观察验证电机的运动情况，确保参数配置正确
   ```bash
   cd "$SPACEMIT_SDK_ROOT" && scripts/test/robot-test run components/peripherals/motor --scope manual
   ```

## 禁止事项

- 不要假设已经选择 target。
- 不要把临时文件或大文件写入 SDK 仓库。

## 常见任务与命令

| 意图 | 命令 |
| ---- | ---- |
| 构建 | `cd "$SPACEMIT_SDK_ROOT" && source build/envsetup.sh && cd components/peripherals/motor && mm` |
| 非法参数注入测试 | `cd "$SPACEMIT_SDK_ROOT" && scripts/test/robot-test run components/peripherals/motor --scope pr` |
| 生产环境兼容性测试 | `cd "$SPACEMIT_SDK_ROOT" && scripts/test/robot-test run components/peripherals/motor --scope manual` |

