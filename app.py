import streamlit as st
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

# Azure App Service では「構成→アプリケーション設定」で OPENAI_API_KEY を追加
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

chat = ChatOpenAI(model="gpt-4o-mini")

system_template = (
    "あなたは優秀な翻訳アシスタントです。{source_lang}の文章を{target_lang}に翻訳してください。"
)
system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
human_message_prompt = HumanMessagePromptTemplate.from_template("{text}")
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

if "response" not in st.session_state:
    st.session_state["response"] = ""

def communicate():
    text = st.session_state["user_input"]
    if not text.strip():
        st.warning("翻訳する文章を入力してください。")
        return

    messages = chat_prompt.format_prompt(
        source_lang=source_lang, target_lang=target_lang, text=text
    ).to_messages()
    response = chat.invoke(messages)
    st.session_state["response"] = response.content

st.title("🌍 翻訳アプリ")

options = ["日本語", "英語", "スペイン語", "ドイツ語", "フランス語", "中国語"]
source_lang = st.selectbox("翻訳元の言語", options)
target_lang = st.selectbox("翻訳先の言語", options)

st.text_input("翻訳する文章を入力してください", key="user_input")
st.button("翻訳する", type="primary", on_click=communicate)

if st.session_state["response"]:
    st.subheader("翻訳結果")
    st.success(st.session_state["response"])
