import streamlit as st
import ollama

st.title("🤖 Chatbot local avec Ollama")

if "history" not in st.session_state:
    st.session_state.history = []

prompt = st.chat_input("Pose ta question...")

if prompt:
    st.session_state.history.append(("user", prompt))

    response = ollama.chat(
        model="gemma3:1b",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response["message"]["content"]
    st.session_state.history.append(("bot", answer))

# Affichage
for role, msg in st.session_state.history:
    with st.chat_message(role):
        st.write(msg)
