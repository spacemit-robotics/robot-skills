# LLM Troubleshooting

读取时机：构建、模型验证、服务启动、`llm_chat`、API 调用或 benchmark 失败时读取。

## 通用排查顺序

1. 确认 mode、SDK root 和执行位置。
2. 确认 `components/model_zoo/llm` 存在。
3. 检查 SDK 环境是否已准备，构建请求是否已走 `spacemit-robot-build`。
4. 检查工具是否可用：`llama-server`、`llama-cli`、`llama-bench`、`llm_chat`。
5. 检查模型路径和 `.gguf` 文件是否存在。
6. 检查 endpoint、端口、模型名、API Key 和服务日志。
7. 返回实际失败命令、退出码、关键日志和下一步最小修复建议。

## 常见问题

### `llm_chat` 不在 PATH

先确认组件已构建，再检查：

- SDK 环境是否已 source；
- `output/staging/bin` 是否有产物；
- 构建日志是否安装 `llm_chat`；
- `components/model_zoo/llm/README.md` 中的构建说明是否有变化。

### `llama-server`、`llama-cli` 或 `llama-bench` 不存在

读取 `package.xml` 和 README，确认 `llama.cpp-tools-spacemit` 是否应安装在当前板端环境。安装包或使用 `sudo` 前必须确认。

### 模型不存在

按 `references/setup.md` 的模型解析规则处理。不要凭记忆造模型名，不要从未确认的模型源下载。

### 端口冲突

先确认已有进程是否属于当前测试。不要默认 `killall`、`pkill` 或停止用户服务。需要停止服务时，说明进程、端口和影响范围并等待确认。

### OpenAI 兼容服务不可达

检查：

- endpoint 是否正确；
- `/v1/models` 是否可访问；
- 模型名是否与服务返回一致；
- API Key 是否在环境变量中；
- 代理、防火墙或远程访问限制。

### benchmark 失败或数据异常

检查：

- 模型文件是否完整；
- 参数是否与 README 口径一致；
- 内存是否不足；
- 是否有后台服务占用资源；
- 是否在正确机器上执行；
- 日志中是否有 unsupported model、missing tensor、OOM 或非法参数。

## 禁止事项

- 不要编造模型输出、服务返回、tokens/s、TTFT、latency 或 benchmark 数据。
- 不要默认删除模型缓存、覆盖已有模型或停止已有服务。
- 不要把 API Key 写入源码、日志或最终回复。
- 不要把模型、日志或临时大文件放进 SDK 源码目录。
