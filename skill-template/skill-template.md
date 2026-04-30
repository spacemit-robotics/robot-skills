---
name: spacemit-{{skill_name}}
description: "{{description}}"
metadata:
  requires:
    bins: ["bash"]
  sdk:
    module_paths:
      - {{module_path}}
    primary_docs:
      - {{primary_doc}}
    build_hint: {{build_hint}}
---

# {{title}}

先 [`../spacemit-robot-shared/SKILL.md`](../spacemit-robot-shared/SKILL.md)；无 SDK 则 [`../spacemit-robot-sdk-bootstrap/SKILL.md`](../spacemit-robot-sdk-bootstrap/SKILL.md)。

## 何时使用

{{when_to_use}}

## 默认规则

- `build_hint`: `{{build_hint}}`
- 写本模块的默认路径、环境变量或缓存目录。
- 不默认先读总览文档或组件 README；只有命令不清、参数不清或实际执行失败时，才回读 `primary_docs`、头文件或脚本本身。
- 写本模块最容易跑偏的 1-2 条固定约束。

## 固定流程

1. 先确认 SDK 根可用；无 SDK 就转 bootstrap。
2. 在 `$SPACEMIT_SDK_ROOT` 下执行 `source build/envsetup.sh`。
3. 再按 `metadata.sdk.build_hint` 决定是优先 `mm`，还是先解析 board 并显式执行 `lunch <target>`。
4. 若构建或运行暴露缺依赖，按报错补装；不要先做脱离上下文的大段依赖排查。
5. 只有当命令细节、参数语义或脚本用法不清，或实际执行失败时，再回读 `primary_docs`。
6. 对“帮我执行 / 帮我测一下 / 跑数据”这类请求，必须真正执行并回传结果，而不只是给命令。

## {{task_section_title}}

{{task_section_content}}

## 禁止事项

- 不要写与本模块无关的通用背景介绍。
- 不要把组件 README、总览文档或长篇 API 说明设为固定前置。
- 不要把运行时必须遵守的关键规则只写在模板、`docs/` 或仓库说明里。

## 常见任务与命令

| 意图 | 动作 |
| ---- | ---- |
| 构建 | `{{build_command}}` |
| 运行 | `{{run_command}}` |
| 测试 | `{{test_command}}` |
