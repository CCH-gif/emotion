import json
import os
from pathlib import Path

class MemoryManager:
    """
    负责管理聊天历史：
    - load: 从本地文件读取
    - save: 保存并裁剪对话
    - clear: 删除历史
    """

    def __init__(self, filepath="chat_history.json", max_rounds=20):
        self.filepath = Path(filepath)
        self.max_rounds = max_rounds

    def load_memory(self):
        """读取历史对话"""
        if not self.filepath.exists():
            return []
        try:
            with self.filepath.open("r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def save_memory(self, messages):
        """保存对话：保留 system prompt + 最近 max_rounds 轮对话"""
        system_prompt = [msg for msg in messages if msg.get("role") == "system"]
        history = [msg for msg in messages if msg.get("role") != "system"]

        trimmed_history = history[-(self.max_rounds * 2):]
        final_memory = system_prompt + trimmed_history

        with self.filepath.open("w", encoding="utf-8") as f:
            json.dump(final_memory, f, ensure_ascii=False, indent=2)

    def clear_memory(self):
        if self.filepath.exists():
            self.filepath.unlink()