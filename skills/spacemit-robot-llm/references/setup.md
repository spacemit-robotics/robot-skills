# LLM Setup

读取时机：准备 LLM 环境、安装依赖、检查模型目录、解析用户点名模型、下载模型或确认工具链前读取。

## 基础依赖

SDK README 和 `package.xml` 是依赖事实源。常见依赖包括：

- CMake >= 3.15
- C++17 编译器
- `libcurl4-openssl-dev`
- `nlohmann-json3-dev`
- riscv64/K3 平台上的 `llama.cpp-tools-spacemit`

安装依赖、执行 `sudo apt` 或修改系统环境前必须先说明目标机器、影响范围并确认。

## 模型目录和模型源

- 默认模型目录：`~/.cache/models/llm`
- 默认模型源：`https://archive.spacemit.com/spacemit-ai/model_zoo/llm/`
- 用户给出本地 `.gguf` 路径时，优先使用用户路径。
- 不要把模型、下载缓存、日志或 benchmark 输出写入 SDK 源码目录。

## 模型解析规则

用户点名模型时，例如“测一下 Qwen3-4B 的性能”，不要凭记忆造模型名，按下面顺序解析：

1. 如果用户给的是本地 `.gguf` 路径，先确认文件存在；存在则直接使用。
2. 在默认模型目录查找 `.gguf`，优先精确文件名匹配，其次大小写不敏感包含匹配。
3. 本地没有匹配时，读取默认模型源索引，只接受索引中列出的 `.gguf` 文件。
4. 远端模型匹配规则与本地一致。
5. 如果远端没有匹配模型，明确告诉用户当前未找到支持模型，或请用户提供模型路径。
6. 如果匹配到多个候选，不要自行猜测；列出候选模型名，让用户确认。

查看默认模型源索引的命令形态：

```bash
curl -fsSL https://archive.spacemit.com/spacemit-ai/model_zoo/llm/ |
  sed -n 's/.*href="\([^"]*\.gguf\)".*/\1/p'
```

下载模型前必须确认目标文件、目标目录和大文件下载影响。确认后下载到默认模型目录或用户指定目录，命令形态：

```bash
mkdir -p ~/.cache/models/llm
curl -fL --retry 3 --continue-at - \
  -o ~/.cache/models/llm/<model>.gguf \
  https://archive.spacemit.com/spacemit-ai/model_zoo/llm/<model>.gguf
```

## 环境检查输出

环境检查后至少返回：

- mode 和执行位置；
- SDK root；
- LLM 模块路径是否存在；
- 关键工具是否可用：`llama-server`、`llama-cli`、`llama-bench`、`llm_chat`；
- 模型目录和候选模型；
- 缺失项；
- 需要用户确认的安装、下载或服务动作。
