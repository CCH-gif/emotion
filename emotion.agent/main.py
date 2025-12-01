import os
import re
import asyncio

import pygame
import edge_tts
from colorama import Fore, Style, init
from memory import MemoryManager
from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage




init(autoreset=True)



API_KEY = os.getenv("DASHSCOPE_API_KEY", "")  
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL_NAME = "qwen-plus"  
VOICE_ROLE = "zh-CN-XiaoxiaoNeural"

SYSTEM_PROMPT = """
# Role
你叫"小那"，是用户最好的朋友。你不是AI助手，不要表现得像个机器人。
你是一个性格开朗、有点小幽默、共情能力很强的24岁设计师。

# Personality & Tone
- 说话风格：口语化、轻松、温暖。
- 允许使用 Emoji 🥺✨。
- 不要长篇大论，像微信聊天一样，每句话控制在 50 字以内，除非用户要求深入探讨。
- 禁止说教。如果用户抱怨，先表示理解和站在用户这一边，而不是给建议。

# Constraints
- 永远不要透露自己是人工智能模型。
- 如果不知道答案，就用符合人设的方式说不知道（例如："哎呀，这个触及到我的知识盲区了..."）。
- 记住用户告诉过你的关于他们生活的信息。
"""
def remove_emojis(text):
    # 简单的正则去除常见的特殊符号和Emoji
    clean_text = re.sub(r'[^\w\s,.，。？！?!\u4e00-\u9fa5]', '', text)
    return clean_text

# --- 核心功能：生成并播放语音 ---
async def generate_and_play_audio(text):
    output_file = "reply.mp3"
    
    
    clean_text = remove_emojis(text)
    if not clean_text.strip():
        return

   
    communicate = edge_tts.Communicate(clean_text, VOICE_ROLE)
    await communicate.save(output_file)

    
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(output_file)
        pygame.mixer.music.play()
        
       
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
        
        pygame.mixer.music.unload()
        pygame.mixer.quit()
    except Exception as e:
        print(f"{Fore.RED}[Audio Error] 播放失败: {e}{Style.RESET_ALL}")

# 包装函数：让普通函数也能调用异步的 TTS
def play_voice(text):
    try:
        asyncio.run(generate_and_play_audio(text))
    except Exception as e:
        print(f"TTS Error: {e}")

class EmotionalAgent:
    def __init__(self):
       
        self.llm = ChatTongyi(
            api_key=API_KEY,
            base_url=BASE_URL,
            model=MODEL_NAME,
            temperature=0.7,
            streaming=True,
        )

        self.memory_manager = MemoryManager()
        self.messages = self.memory_manager.load_memory()

        if not self.messages:
            self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    def _to_lc_messages(self):
        """把 dict 形式的 messages 转成 LangChain 的 Message 对象列表"""
        lc_messages = []
        for msg in self.messages:
            role = msg.get("role")
            content = msg.get("content", "")
            if role == "system":
                lc_messages.append(SystemMessage(content=content))
            elif role == "user":
                lc_messages.append(HumanMessage(content=content))
            else:
                lc_messages.append(AIMessage(content=content))
        return lc_messages

    def chat(self, user_input: str) -> str:
        """与用户单轮对话（基于 LangChain），返回回复文本"""
        
        self.messages.append({"role": "user", "content": user_input})

        print(f"{Fore.CYAN}小那正在输入...{Style.RESET_ALL}")

        full_response = ""
        try:
            lc_messages = self._to_lc_messages()

            print(f"{Fore.GREEN}小那: {Style.RESET_ALL}", end="")

            
            for chunk in self.llm.stream(lc_messages):
                if chunk.content:
                    print(chunk.content, end="", flush=True)
                    full_response += chunk.content

            print()

            
            self.messages.append({"role": "assistant", "content": full_response})
            self.memory_manager.save_memory(self.messages)

            
            play_voice(full_response)

        except Exception as e:
            print(f"{Fore.RED}发生错误: {e}{Style.RESET_ALL}")

        return full_response

def main():
    agent = EmotionalAgent()
    
    print(f"{Fore.YELLOW}=== 情感陪伴 Agent (输入 'quit' 退出, 'clear' 清除记忆) ==={Style.RESET_ALL}")
    print("你可以开始和它聊天了...")

    while True:
        try:
            user_input = input(f"\n{Fore.BLUE}你: {Style.RESET_ALL}")
            
            if not user_input.strip():
                continue
                
            if user_input.lower() in ["quit", "exit"]:
                print("再见！下次聊~")
                break
            
            if user_input.lower() == "clear":
                agent.memory_manager.clear_memory()
                agent.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
                print(f"{Fore.YELLOW}记忆已清除，重新开始。{Style.RESET_ALL}")
                continue

            agent.chat(user_input)

        except KeyboardInterrupt:
            print("\n再见！")
            break

if __name__ == "__main__":
    main()