---
name: spacemit-robot-{{skill_name}}
description: "{{description}}"
metadata:
  sdk:
    module_paths:
      - {{module_path}}
    primary_docs:
      - {{primary_doc}}
    build_hint: {{build_hint}}
---

# {{title}}

## Contract

- 模块路径：`{{module_path}}`
- 构建倾向：`{{build_hint}}`
- 文档入口：`{{primary_doc}}`
- 基础规则：先用 `spacemit-robot-shared` 解析 mode、SDK root 和 target；构建走 `spacemit-robot-build`；remote/hybrid 执行走 `spacemit-robot-remote`；hybrid 同步走 `spacemit-robot-sync`。

## Workflow

1. 先确认用户是在做代码修改、构建、运行 smoke、API 接入还是测试。
2. 优先读取 SDK 模块内 `AGENTS.md`；不存在时按需读取 primary docs。
3. 构建请求交给 `spacemit-robot-build`，不要在组件 skill 写死命令或 target。
4. `remote` 和 `hybrid` 场景下，所有执行都在板端完成。
5. `robot-test` 只在 CI/回归/用户明确要求时使用；日常开发默认按最小构建或 smoke 验证。

## Notes

- 写本模块最容易跑偏的 1-3 条约束。
- 涉及真实设备、长时间 benchmark、模型下载或修改板端状态时，先说明影响并确认。
