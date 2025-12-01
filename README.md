## 小那 · 情感陪伴助手（LangChain + 通义千问）

一个基于 **LangChain** 和 **通义千问（Qwen）** 的情感陪伴聊天助手，支持：

- **命令行聊天**：在终端中与“小那”对话  
- **网页聊天界面**：使用 **Streamlit** 提供对话 UI  
- **记忆功能**：本地保存最近多轮对话  
- **语音回复**：调用 Edge TTS 合成语音并用 pygame 播放

---

### 1. 环境准备

建议使用虚拟环境（可选）：

```bash
python -m venv .venv
.\.venv\Scripts\activate  # Windows
```

安装依赖（核心）：

```bash
pip install -r requirement.txt
```

如果没有 requirement.txt，也可以手动安装主要包：

```bash
pip install streamlit langchain langchain-openai colorama pygame edge-tts
```

---

### 2. 通义千问（Qwen）配置

项目使用 **DashScope 的 OpenAI 兼容接口** 调用通义千问。

在系统环境变量中设置：

- **DASHSCOPE_API_KEY**：你的通义千问 DashScope 密钥

示例（PowerShell）：

```powershell
setx DASHSCOPE_API_KEY "你的DashScope_API_Key"
```

代码中相关配置在 `main.py`：

- `API_KEY = os.getenv("DASHSCOPE_API_KEY", "")`
- `BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"`
- `MODEL_NAME = "qwen-plus"`（可改为 `qwen-turbo` 等）

---

### 3. 运行命令行版本

在项目目录 `emotion.agent` 下：

```bash
python main.py
```

命令行中输入内容，即可与“小那”对话：

- 输入 `quit` / `exit` 退出
- 输入 `clear` 清除历史记忆

---

### 4. 运行网页前端（Streamlit）

同样在 `emotion.agent` 目录下，执行：

```bash
streamlit run frontend.py
```

浏览器会自动打开一个页面，展示聊天界面：

- 左侧为聊天记录
- 底部输入框发送消息

---

### 5. 主要文件说明

- `main.py`  
  - 定义核心类 `EmotionalAgent`  
  - 使用 LangChain 的 `ChatOpenAI` 调用通义千问  
  - 使用 `MemoryManager` 读写对话历史  
  - 使用 Edge TTS + pygame 播放语音回复

- `frontend.py`  
  - 使用 Streamlit 创建 Web 聊天前端  
  - 通过 `EmotionalAgent` 与后端交互

- `memory.py`  
  - `MemoryManager`：负责将对话历史读写到本地 `chat_history.json`

- `reply.mp3`  
  - 最近一次 TTS 合成的语音文件

---

### 6. 常见问题

- **Streamlit 提示 `Error: No such command 'frontend.py'`**  
  使用命令时需要加 `run`：  
  ```bash
  streamlit run frontend.py
