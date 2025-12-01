import streamlit as st
from main import EmotionalAgent, SYSTEM_PROMPT


def get_agent() -> EmotionalAgent:
    if "agent" not in st.session_state:
        st.session_state.agent = EmotionalAgent()
    return st.session_state.agent


def main():
    st.set_page_config(page_title="小那 · 情感陪伴助手", page_icon="💛")
    st.title("💛 小那 · 情感陪伴助手")
    st.caption("本应用仅用于情感陪伴与聊天，不提供任何专业医疗/法律/财务建议。")

    agent = get_agent()

    # 初始化对话历史（仅用于前端展示）
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # 展示历史消息
    for role, content in st.session_state.chat_history:
        with st.chat_message("user" if role == "user" else "assistant"):
            st.markdown(content)

    # 输入框
    prompt = st.chat_input("和小那聊点什么吧...")
    if prompt:
        # 显示用户消息
        st.session_state.chat_history.append(("user", prompt))
        with st.chat_message("user"):
            st.markdown(prompt)

        # 调用后端 Agent
        with st.chat_message("assistant"):
            with st.spinner("小那正在想怎么回复你..."):
                reply = agent.chat(prompt)  # 会自动触发本地语音播放
            st.markdown(reply)
            st.session_state.chat_history.append(("assistant", reply))


if __name__ == "__main__":
    main()

