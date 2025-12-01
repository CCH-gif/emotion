# emotion
## 小那 · 情感陪伴 Agent

一个基于大语言模型 + 本地记忆系统 + TTS 语音播放的终端情感陪伴机器人，并提供简单的 Web 前端界面（Streamlit）。

---

### 功能特性

- **情感陪伴对话**：以“小那”的人设和你进行多轮聊天，语气轻松温暖。
- **记忆管理**：自动保存最近多轮对话到本地 `chat_history.json`，支持清空记忆。
- **语音播放**：使用 `edge-tts` 合成语音，`pygame` 在本地播放回复音频。
- **Web 前端**：通过 Streamlit 提供简易聊天网页界面。

---

### 项目结构

- `main.py`：核心 Agent 逻辑（终端版 + 语音播放）
- `memory.py`：对话记忆管理（加载 / 保存 / 清空）
- `frontend.py`：Streamlit 前端界面
- `chat_history.json`：本地对话历史（自动生成）

---

### 环境准备

#### 1. 创建虚拟环境（可选）

cd d:\实验\emotion.agent
python -m venv .venv
.\.venv\Scripts\activate#### 2. 安装依赖

pip install openai streamlit edge-tts pygame colorama> 如果报错缺少 `pyaudio` 或声卡相关库，可根据系统提示额外安装。

---

### API 配置

在 `main.py` 顶部有两项配置，需要你自己填：

API_KEY = ""      # 你的 OpenAI / DashScope 兼容 key
BASE_URL = ""     # 兼容 OpenAI 协议的接口地址
MODEL_NAME = "qwen-plus"示例（如果你用 DashScope 兼容模式）：

API_KEY = "sk-xxxxxx"
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"> **注意**：不要把真实的 API Key 提交到任何公共仓库。

---

### 运行命令行版（终端聊天）

cd d:\实验\emotion.agent
python main.py- 输入内容后按回车即可聊天
- 输入 `clear`：清空记忆，从零开始
- 输入 `quit` / `exit`：退出程序

程序会：
- 在终端打印“小那”的文字回复
- 在本地生成并播放 `reply.mp3` 语音

---

### 运行 Web 前端

cd d:\实验\emotion.agent
streamlit run frontend.py浏览器会自动打开一个页面，你可以在网页里：

- 输入消息和“小那”聊天
- 查看历史消息（当前语音在本机播放，不走浏览器）

---

### 常见问题

- **没有声音 / 播放失败**
  - 检查是否安装 `edge-tts` 和 `pygame`
  - 确认本机有可用音频输出设备
  - 终端里是否有 `[Audio Error]` 或 `TTS Error` 提示

- **一直报 API 相关错误**
  - 检查 `API_KEY` 和 `BASE_URL` 是否填写正确
  - 检查是否可以正常访问对应的 API 服务

- **记忆不生效 / 不记得之前说的话**
  - 查看当前目录下是否生成 `chat_history.json`
  - 检查是否频繁用 `clear` 清空记忆

---

### 后续可以扩展的方向

- 在前端增加“开关语音”按钮
- 增加多角色 / 多人设切换
- 增加日志与对话分析能力（例如情绪分析）
