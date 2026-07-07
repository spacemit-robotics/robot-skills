# LLM API

读取时机：用户要调用 C++ API、修改 API 行为、接入 OpenAI 兼容服务、处理 Tool Calling、流式输出、多轮对话或 metrics 时读取。

## 对外 API 入口

对外提供的 C++ API 头文件只有：

- `components/model_zoo/llm/include/llm_service.h`

用户做应用接入时，只以 `llm_service.h` 为 API 事实源。不要把 `src/` 下的 backend、factory 或 service 实现头文件当成对外接口。

## 内部实现参考

只有在排查实现问题、修改内部行为或新增 backend 时，才按需读取这些文件：

- `components/model_zoo/llm/src/backends/openai_backend.cpp`: 排查或修改 OpenAI 兼容 HTTP 后端行为时读取。
- `components/model_zoo/llm/src/backends/openai_backend.h`: 理解 OpenAI backend 内部边界、构造参数或内部接口时读取。
- `components/model_zoo/llm/src/llm_service.cpp`: 排查 `LLMService` PIMPL 封装、metrics 或公共 API 实现时读取。
- `components/model_zoo/llm/src/llm_backend_factory.cpp`: 排查 backend 选择或新增 backend 时读取。
- `components/model_zoo/llm/src/llm_backend_factory.h`: 理解 backend factory 内部接口或新增 backend 时读取。
- `components/model_zoo/llm/example/cpp/llm_chat.cpp`: 用户要运行、修改或参考 `llm_chat` 示例时读取。
- `components/model_zoo/llm/example/cpp/CMakeLists.txt`: 用户要在自己的 C++ 组件中链接 LLM 库时读取。

修改 API 行为前先读 `llm_service.h`；需要定位内部实现时再读对应 `src/` 文件。不要绕过已有 `LLMService` 抽象。

## 能力边界

`LLMService` 支持：

- OpenAI 兼容 HTTP API 后端；
- 自定义或本地 backend 构造路径；
- 单轮 `complete()`；
- 异步 `complete_async()`；
- 流式 `complete_stream()`；
- 多轮 `chat()`；
- 支持 Tool Calling 的 `chat_stream()`；
- prompt、model、API settings 和 reasoning budget 更新；
- `get_metrics()` 指标读取。

常见 OpenAI 兼容服务包括本地 `llama-server`、vLLM、SGLang 或云端 OpenAI 兼容服务。接入云端服务时，API Key 只从环境变量或用户明确配置读取。

## API 应用流程

1. 确认用户场景：单轮同步、单轮异步、单轮流式、多轮对话、Tool Calling、metrics，还是运行时切换 model/API/prompt。
2. 确认服务形态：本地 `llama-server`、远端 vLLM/SGLang、云端 OpenAI 兼容服务，记录 `api_base`、`model`、`api_key`、默认 prompt 和 `max_tokens`。
3. 确认服务已经可访问；本地服务通常先用 `curl -s http://127.0.0.1:<port>/v1/models` 验证。
4. 应用代码只包含 `llm_service.h`，使用 `spacemit_llm::LLMService` 或命名空间别名 `spacemit_llm::ChatMessage`、`spacemit_llm::ChatResult`。
5. 优先使用 OpenAI 兼容 HTTP 构造函数；普通应用不要优先使用自定义 backend 构造函数。
6. 按场景调用 `complete()`、`complete_async()`、`complete_stream()`、`chat()` 或 `chat_stream()`。
7. 流式调用后，应用需要等待 callback 收到 `is_finished=true` 或 `is_done=true`，再退出程序或读取 metrics；完整等待方式参考 `example/cpp/llm_chat.cpp`。
8. 如果使用 Tool Calling，应用层负责解析 `tool_calls_json`、执行真实工具、校验权限和回填工具结果；LLM 组件只负责传递 tools 定义并返回模型请求。
9. 构建交给 `spacemit-robot-build`；`remote` 或 `hybrid` 模式下，在板端运行验证。

## 初始化方式

普通应用优先使用 OpenAI 兼容 HTTP 后端：

```cpp
#include "llm_service.h"

spacemit_llm::LLMService llm(
    "qwen2.5-0.5b",
    "http://127.0.0.1:8080/v1",
    "",
    "You are a helpful assistant.",
    256);
```

参数含义：

- `model`: 服务端暴露的模型名，不一定等同于 `.gguf` 文件名。
- `api_base`: OpenAI 兼容 API 地址，通常形如 `http://127.0.0.1:8080/v1`。
- `api_key`: 本地 `llama-server` 可为空；云端服务从环境变量或安全配置读取。
- `prompt`: 默认 system prompt。
- `max_tokens`: 最大输出 token 数。

自定义或本地 backend 构造函数属于高级场景。普通应用不要用它替代 OpenAI 兼容 HTTP 后端：

```cpp
spacemit_llm::LLMService llm(config_dir, prompt, max_tokens);
```

## 常用调用模式

### 单轮同步

适合一次性问答、命令解析或不需要逐字显示的场景。

```cpp
std::string reply = llm.complete("你好，请用一句话介绍 K3。");
```

### 单轮异步

适合不希望阻塞当前线程的简单问答。结果通过 callback 返回。

```cpp
llm.complete_async(
    "生成一句机器人欢迎语。",
    [](const std::string& result, const std::string& error) {
        if (!error.empty()) {
            return;
        }
        // 使用 result。
    });
```

### 单轮流式

适合聊天窗口逐字显示、TTS 边生成边播报或支持用户打断。callback 返回 `false` 表示取消。

```cpp
llm.complete_stream(
    "写一段机器人助手的欢迎语。",
    [](const std::string& chunk, bool is_finished, const std::string& error) {
        if (!error.empty()) {
            return false;
        }
        if (!chunk.empty()) {
            std::cout << chunk << std::flush;
        }
        return !is_finished;
    });
```

`complete_stream()` 在 OpenAI HTTP 后端会启动后台线程；应用不能在发起调用后立即退出。

### 多轮对话

适合需要上下文的连续问答、机器人任务确认和多轮规划。应用层维护消息历史，并控制历史长度。

```cpp
using spacemit_llm::ChatMessage;

std::vector<ChatMessage> messages = {
    ChatMessage::System("You are a robot assistant."),
    ChatMessage::User("你能做什么？")
};

std::string answer = llm.chat(messages);
messages.push_back(ChatMessage::Assistant(answer));
```

### Tool Calling

适合 Agent、机器人控制、外部状态查询和业务工具调用。

调用闭环：

1. 准备 `messages`。
2. 准备合法的 OpenAI tools JSON 数组。
3. 调用 `chat_stream(messages, callback, tools_json)`。
4. 如果 `ChatResult::HasToolCalls()` 为 true，解析 `result.tool_calls_json`。
5. 应用层执行工具，并做参数校验、权限控制和真实设备安全确认。
6. 将模型回复和工具结果追加到 messages。
7. 再调用 `chat()` 或 `chat_stream()` 生成最终回复。

```cpp
auto result = llm.chat_stream(
    messages,
    [](const std::string& chunk, bool is_done, const std::string& error) {
        if (!error.empty()) {
            return false;
        }
        if (!chunk.empty()) {
            std::cout << chunk << std::flush;
        }
        return !is_done;
    },
    tools_json);

if (result.HasToolCalls()) {
    std::string tool_call_id = "<从 result.tool_calls_json 中解析出的 id>";
    std::string tool_result = R"({"battery": 86, "status": "normal"})";

    messages.push_back(ChatMessage::Assistant(result.content, result.tool_calls_json));
    messages.push_back(ChatMessage::Tool(tool_result, tool_call_id));

    std::string final_answer = llm.chat(messages);
}
```

## 运行时配置和指标

- `update_prompt(new_prompt, max_tokens)`: 更新默认 system prompt；`max_tokens > 0` 时同步更新最大输出 token 数。
- `update_model(new_model)`: 切换模型名。
- `update_api_settings(api_base, api_key)`: 切换 OpenAI 兼容服务地址和鉴权密钥。
- `update_reasoning_budget(reasoning_budget)`: 更新 reasoning budget。
- `get_metrics()`: 在一次调用完成后读取请求数、处理状态、端到端延迟、TTFT、输出 token 数和 tokens/s。
- `get_backend_type()`: 查看当前 backend 类型。

## 下游组件链接

如果用户要在 SDK 内自己的 C++ 组件中链接 LLM 组件，先参考 `components/model_zoo/llm/example/cpp/CMakeLists.txt`。常见方式是查找 `llm_service_cpp` 和 `llm_service.h`，并在当前组件的 `package.xml` 中声明对 `llm` 的依赖。

## 执行结果反馈

返回结果时说明：

- 使用的 API；
- 服务 endpoint 和模型名；
- 是否使用 API Key；
- 修改的文件；
- 构建命令和结果；
- 运行命令和结果。
