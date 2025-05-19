import streamlit as st
import requests as rq
import json

with st.sidebar:
    openrouter_api_key = st.text_input("OpenrouterAI API Key", key="chatbot_api_key", type="password")
    openrouter_model = st.text_input("OpenrouterAI Model", key="model", type="default")

def AI(messages,api_key,model=openrouter_model):
    response = rq.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai. - If you are intereseted please update this.
        "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
    },
    data=json.dumps({
        "model": model, # Optional
        "messages": messages
    })
    )  
    return response.json()["choices"][0]["message"]["content"]

st.title("💬 Simple AI Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": "You are an assistant who are required to communicate with the user providing all necessary output required by them."}]
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openrouter_api_key:
        st.info("Please add your OpenrouterAI API key to continue.")
        st.stop()
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = AI(model="openai/gpt-4o-mini", messages=st.session_state.messages,api_key=openrouter_api_key)
    msg = response
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)