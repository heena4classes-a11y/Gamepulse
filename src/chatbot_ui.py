# src/chatbot_ui.py
import streamlit as st
from rag_bot import ask_bot

st.set_page_config(page_title="GamePulse Chatbot", page_icon="🎮")
st.title("🎮 Assassin's Creed Shadows - Review Chatbot")

# Initialize chat history in session state
if "history" not in st.session_state:
    st.session_state.history = []

# User input
user_input = st.text_input("Ask a question about the game:")

if user_input:
    # Call RAG bot
    answer = ask_bot(user_input)
    
    # Append to chat history
    st.session_state.history.append({"user": user_input, "bot": answer})

# Display chat history
for chat in st.session_state.history:
    with st.chat_message("user"):
        st.markdown(chat['user'])
    with st.chat_message("assistant"):
        st.markdown(chat['bot'])

