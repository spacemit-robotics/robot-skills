# LLM Benchmarking

读取时机：用户明确要求性能、benchmark、延迟、吞吐、tokens/s、模型对比或优化前后对比时读取。

## 性能采集规则

- 性能采集使用 SDK README 中的 `llama-bench` 口径。
- 模型路径先按 `references/setup.md` 的模型解析规则得到。
- `remote` 和 `hybrid` 模式下，benchmark 在板端执行。
- 长时间 benchmark、占用大量内存或下载大模型前必须确认。
- 不要编造性能数据；没有执行就明确说明未执行。

默认命令形态如下，模型路径替换为解析出的本地 `.gguf` 路径：

```bash
llama-bench \
  -m ~/.cache/models/llm/<model>.gguf \
  -t 8 \
  -p 128 \
  -n 128 \
  -mmp 0 \
  -fa 1
```

线程数、prompt token 数、generation token 数可按用户要求或 README 口径调整。调整时在结果里说明。

## 执行前记录

执行前记录：

- mode；
- board 或执行机器；
- SDK root；
- 模型路径；
- 线程数；
- prompt token 数；
- generation token 数；
- 完整命令；
- 是否有后台服务或端口占用。

## 输出要求

返回结果时至少包含：

- 模型路径；
- 完整命令；
- 线程数；
- prompt token 数；
- generation token 数；
- 主要吞吐或延迟指标；
- 日志路径；
- 失败点。

如果用户要求对比多个模型或多组参数，逐项返回相同字段，不要只给结论。
