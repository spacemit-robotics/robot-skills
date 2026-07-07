# LLM Examples

读取时机：用户要构建 LLM 组件、验证模型、启动 `llama-server`、检查 OpenAI 兼容服务或运行 `llm_chat` 示例时读取。

所有构建和执行位置先由 `spacemit-robot-shared`、`spacemit-robot-build`、`spacemit-robot-remote` 决定。`remote` 和 `hybrid` 模式下，下面的运行类命令都在板端执行。

## 构建组件

构建请求交给 `spacemit-robot-build`。LLM 的构建倾向是 `single_package_first`，优先构建 `components/model_zoo/llm`。

构建完成后，`llm_chat` 应通过 SDK 环境出现在 `PATH` 中；如果不可用，先检查：

- `output/staging/bin`
- 构建日志
- `components/model_zoo/llm/package.xml`
- SDK README 中的构建说明

## 验证模型

模型验证前先按 `references/setup.md` 解析 `.gguf` 路径。命令形态：

```bash
llama-cli -m ~/.cache/models/llm/<model>.gguf \
  -t 4 \
  -p "Hello, please introduce yourself."
```

返回结果时说明模型路径、完整命令、关键输出和失败点。

## 启动服务并运行示例

启动 OpenAI 兼容服务的命令形态：

```bash
llama-server -m ~/.cache/models/llm/<model>.gguf -t 8 --port 8080
```

如果需要后台运行，先说明会启动长驻服务并确认。端口冲突时先确认已有进程是否属于当前测试，不要默认清理用户正在使用的 `llama-server`。

检查服务：

```bash
curl -fsS http://localhost:8080/v1/models
```

运行 `llm_chat` 示例：

```bash
llm_chat "你好" "http://localhost:8080/v1" "<model-name>" "You are a helpful assistant." 256
```

返回结果时至少包含：

- service endpoint；
- 模型名；
- 输入文本；
- 完整命令；
- 输出摘要；
- 日志或失败点。

## 云端或远端 OpenAI 兼容服务

若使用云端或远端 OpenAI 兼容服务，只替换 API base 和模型名。API Key 必须来自用户已配置的环境变量或安全凭据，不要写入源码或最终回复。

如果服务不可达，先排查 endpoint、端口、模型名和认证，再考虑修改示例代码。
