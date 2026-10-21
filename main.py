import os

import streamlit as st
import requests

API_URL = "https://api.timeweb.ai/v1/chat/completions"
API_KEY = os.getenv("TIMEWEB_API_KEY", "")
if not API_KEY:
    try:
        API_KEY = st.secrets["TIMEWEB_API_KEY"]
    except Exception:
        API_KEY = ""
MODEL = "dashscope/qwen3.6-flash"

st.title("🤖 Чат-бот на Streamlit + Timeweb")

if not API_KEY:
    st.error("Добавьте ключ API в настройки приложения.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Напишите сообщение...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": st.session_state.messages,
                "temperature": 0.7
            }
        )

        data = response.json()

        try:
            answer = data["choices"][0]["message"]["content"]
        except Exception:
            answer = f"Ошибка API: {data}"

        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})