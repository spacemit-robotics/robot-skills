---
name: spacemit-robot-llm
description: model_zoo/llm 的构建、运行与性能测试入口；默认先 `mm`，模型走 `~/.cache/models/llm`，压测直接用 `bench_llm.sh`。
metadata:
  requires:
    bins: ["bash", "curl"]
  sdk:
    module_paths:
      - components/model_zoo/llm
    primary_docs:
      - components/model_zoo/llm/README.md
      - components/model_zoo/llm/include/llm_service.h
    build_hint: single_package_first
---

# SpacemiT model_zoo LLM

先 [`spacemit-robot-shared`](../spacemit-robot-shared/SKILL.md)；无 SDK 则 [`spacemit-robot-sdk-bootstrap`](../spacemit-robot-sdk-bootstrap/SKILL.md)。

## 何时使用

- 用户要构建、运行、调试或压测 `components/model_zoo/llm`。
- 用户要跑 `llm_chat`、接 OpenAI 兼容服务、查看 `LLMService` API，或采集 LLM 性能数据。

## 默认规则

- `build_hint`: `single_package_first`
- 默认模型目录：`~/.cache/models/llm`
- 不默认先读总览文档或组件 README；只有命令不清、参数不清或实际执行失败时，才回读 `README.md`、`llm_service.h` 或脚本本身。
- 不要把模型下载到仓库内 `models/`、当前目录临时路径或其他自造目录。

## 固定流程

1. 先确认 SDK 根可用；无 SDK 就转 bootstrap。
2. 在 `$SPACEMIT_SDK_ROOT` 下执行 `source build/envsetup.sh`。
3. 若 `llm_chat` 不可用，再执行 `cd "$SPACEMIT_SDK_ROOT/components/model_zoo/llm" && mm`。
4. 若 `mm` 报缺依赖，按报错补装；不要先做脱离上下文的大段依赖排查。
5. 本地运行或压测前先检查 `~/.cache/models/llm/*.gguf`；已有模型就直接复用，没有再下载到该目录。
6. 若 shared 规则或组件文档明确要求 target，再显式执行 `lunch <target>`；不要裸 `lunch`。
7. 对“帮我执行 / 帮我测一下 / 跑性能数据”这类请求，必须真正执行并返回结果，而不只是给命令。

## 性能测试

当用户说“测试性能数据”“跑一下 LLM 性能”时，直接按下面顺序执行：

1. `source build/envsetup.sh`
2. 若 `llm_chat` 不可用，再 `mm`
3. `ls ~/.cache/models/llm/*.gguf`
4. 只有在 `~/.cache/models/llm` 下没有可用 `.gguf` 时，才下载模型到该目录
5. `cd "$SPACEMIT_SDK_ROOT/components/model_zoo/llm" && LLM_THREADS=8 scripts/bench_llm.sh ~/.cache/models/llm/<model>.gguf`
6. 返回 first token latency、tokens/s、E2E latency、测试命令、模型路径和失败点

## 禁止事项

- 不要在压测前先单独跑一次 `llm_chat` 探路；`bench_llm.sh` 自己会拉起 `llama-server` 并完成预热
- 不要先执行与压测无关的 Python 探测或长时间搜索
- 不要默认 `killall` / `pkill` 现有 `llama-server`；只有确认端口冲突或残留进程影响本次测试时才处理

## 常见任务与命令

| 意图 | 动作 |
| ---- | ---- |
| 构建 | `cd "$SPACEMIT_SDK_ROOT" && source build/envsetup.sh && cd components/model_zoo/llm && mm` |
| 查模型 | `ls ~/.cache/models/llm/*.gguf` |
| 验模型 | `llama-cli -m ~/.cache/models/llm/<model>.gguf ...` / `llama-bench -m ~/.cache/models/llm/<model>.gguf ...` |
| 起本地服务 | `llama-server -m <gguf> ...`（见 README） |
| 示例对话 | `llm_chat "<text>" <api_base> <model> [prompt] [max_tokens]` |
| 采集性能数据 | `$SPACEMIT_SDK_ROOT/components/model_zoo/llm/scripts/bench_llm.sh ~/.cache/models/llm/<model>.gguf` |
