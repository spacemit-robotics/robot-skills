---
name: spacemit-robot-llm
description: components/model_zoo/llm 的构建、模型准备、llama-server 验证、llm_chat 示例、llama-bench 性能采集与 C++ API 接入入口。
metadata:
  requires:
    bins: ["bash", "curl"]
  sdk:
    module_paths:
      - components/model_zoo/llm
    primary_docs:
      - components/model_zoo/llm/README.md
      - components/model_zoo/llm/include/llm_service.h
      - components/model_zoo/llm/package.xml
    build_hint: single_package_first
---

# SpacemiT Robot LLM

先按 [`spacemit-robot-shared`](../spacemit-robot-shared/SKILL.md) 确认 SDK 根路径与通用构建规则；没有完整 SDK 时走 [`spacemit-robot-sdk-bootstrap`](../spacemit-robot-sdk-bootstrap/SKILL.md)。

## 何时使用

- 用户要构建、运行、调试或集成 `components/model_zoo/llm`。
- 用户要验证 GGUF 模型、启动 `llama-server`、运行 `llm_chat` 示例或采集 `llama-bench` 性能数据。
- 用户要查看 `LLMService` C++ API、OpenAI 兼容服务接入、Tool Calling、流式输出或多轮对话能力。

## 默认规则

- 构建倾向：`single_package_first`，优先在模块目录执行 `mm`，只有确实需要产品配置时再按 shared 规则选择 target。
- SDK 内模块路径：`$SPACEMIT_SDK_ROOT/components/model_zoo/llm`。
- 默认模型目录：`~/.cache/models/llm`；不要把大模型文件放进 SDK 仓库。
- 默认模型源：`https://archive.spacemit.com/spacemit-ai/model_zoo/llm/`。
- 性能采集直接使用 `llama-bench`；线程数默认按 README 使用 `-t 8`，同时保留 `-p 128 -n 128 -mmp 0 -fa 1`。
- 只有命令细节、参数语义或 API 行为不清时，再回读 `README.md`、`include/llm_service.h`、`package.xml`。

## 固定流程

1. 确认 `$SPACEMIT_SDK_ROOT` 指向完整 SDK，至少包含 `build/`、`components/`、`target/`。
2. 在 SDK 根目录执行 `source build/envsetup.sh`。
3. 需要构建时执行 `cd "$SPACEMIT_SDK_ROOT/components/model_zoo/llm" && mm`。
4. 运行前检查 `llama-server`、`llama-cli`、`llama-bench`、`llm_chat` 是否可用；缺系统包时按 `package.xml` 和 README 补装。
5. 运行前检查模型文件：优先复用 `~/.cache/models/llm/*.gguf` 或用户指定路径；缺模型时按下方“模型解析与下载”处理。
6. 执行型请求必须真实运行命令，并返回模型路径、命令、关键输出、耗时或失败点。

## 专项任务

### 构建组件

```bash
cd "$SPACEMIT_SDK_ROOT"
source build/envsetup.sh
cd components/model_zoo/llm
mm
```

构建后 `llm_chat` 应通过 SDK 环境出现在 `PATH` 中；如果不可用，先检查 `output/staging/bin` 和构建日志。

### 验证模型

```bash
llama-cli -m ~/.cache/models/llm/<model>.gguf \
  -t 4 \
  -p "Hello, please introduce yourself."
```

### 启动服务并跑示例

```bash
llama-server -m ~/.cache/models/llm/<model>.gguf -t 8 --port 8080 &
curl -fsS http://localhost:8080/v1/models
llm_chat "你好" "http://localhost:8080/v1" "<model-name>" "You are a helpful assistant." 256
```

端口冲突时先确认已有进程是否属于当前测试；不要默认清理用户正在使用的 `llama-server`。

### 采集性能

当用户说“帮我测一下 xxx 模型的性能数据”时，按“模型解析与下载”先得到本地 `.gguf` 路径，再在 SDK 根目录执行性能采集。默认命令形态如下；模型路径替换为解析出的本地路径。

```bash
llama-bench \
  -m ~/.cache/models/llm/<model>.gguf \
  -t 8 \
  -p 128 \
  -n 128 \
  -mmp 0 \
  -fa 1
```

返回结果时至少包含：模型路径、完整命令、线程数、prompt token 数、generation token 数、主要吞吐或延迟指标，以及失败点。

### 模型解析与下载

对用户点名的模型，例如“测一下 Qwen3-4B 的性能”，不要凭记忆造模型名，按下面顺序解析：

1. 如果用户给的是本地 `.gguf` 路径，先确认文件存在，存在则直接使用。
2. 在 `~/.cache/models/llm` 查找 `.gguf`，优先精确文件名匹配，其次大小写不敏感包含匹配。
3. 本地没有匹配时，读取模型源索引，只接受其中列出的 `.gguf` 文件：

   ```bash
   curl -fsSL https://archive.spacemit.com/spacemit-ai/model_zoo/llm/ |
     sed -n 's/.*href="\([^"]*\.gguf\)".*/\1/p'
   ```

4. 远端模型匹配规则与本地一致；如果匹配到唯一模型，下载到 `~/.cache/models/llm`：

   ```bash
   mkdir -p ~/.cache/models/llm
   curl -fL --retry 3 --continue-at - \
     -o ~/.cache/models/llm/<model>.gguf \
     https://archive.spacemit.com/spacemit-ai/model_zoo/llm/<model>.gguf
   ```

5. 如果远端没有匹配模型，明确告诉用户：`当前不支持该模型`。
6. 如果匹配到多个候选，不要自行猜测；列出候选模型名，让用户确认要测哪一个。

### 接入 C++ API

- 头文件入口：`components/model_zoo/llm/include/llm_service.h`。
- 默认后端是 OpenAI 兼容 HTTP API，可连接本地 `llama-server`、vLLM、SGLang 或云端 OpenAI 兼容服务。
- 修改 API 行为前先读 `llm_service.h` 和 `src/backends/openai_backend.*`，避免绕过已有 `LLMService` 抽象。

## 禁止事项

- 不要假设已经选择 target；需要 target 时按 shared 规则显式选择。
- 不要把模型、日志或临时大文件提交到 SDK。
- 不要默认 `killall`、`pkill` 或删除已有模型缓存。
- 不要用自造脚本替代 README 中已经定义的 `llama-server`、`llama-cli`、`llama-bench` 入口。
- 不要从非默认模型源下载用户点名的性能测试模型；默认模型源没有时回复当前不支持。

## 常见任务与命令

| 意图 | 命令 |
| ---- | ---- |
| 构建 LLM 组件 | `cd "$SPACEMIT_SDK_ROOT" && source build/envsetup.sh && cd components/model_zoo/llm && mm` |
| 查找模型 | `ls ~/.cache/models/llm/*.gguf` |
| 验证模型输出 | `llama-cli -m ~/.cache/models/llm/<model>.gguf -t 4 -p "<prompt>"` |
| 启动 OpenAI 兼容服务 | `llama-server -m ~/.cache/models/llm/<model>.gguf -t 8 --port 8080` |
| 检查服务 | `curl -fsS http://localhost:8080/v1/models` |
| 运行示例 | `llm_chat "<text>" "http://localhost:8080/v1" "<model-name>" "You are a helpful assistant." 256` |
| 采集性能 | `llama-bench -m <model.gguf> -t 8 -p 128 -n 128 -mmp 0 -fa 1` |
| 查看支持模型 | `curl -fsSL https://archive.spacemit.com/spacemit-ai/model_zoo/llm/ \| sed -n 's/.*href="\\([^"]*\\.gguf\\)".*/\\1/p'` |
