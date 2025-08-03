# streamlit_app.py

import streamlit as st
from main import agent
from streamlit_chat import message  # pip install streamlit-chat

st.set_page_config(page_title=" AI Agent", layout="centered")
st.markdown("<h1 style='text-align: center;'>AI Agent</h1>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: right;'>-powered by gemini</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Perform calculations, unit conversions, solve equations, generate code and get news — all in one place!</p>", unsafe_allow_html=True)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar with info
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=100)
    st.markdown("### 📌 Tools Available")
    st.markdown("- 🧮 Calculator")
    st.markdown("- 📏 Unit Converter")
    st.markdown("- 📐 Math Solver")
    st.markdown("- 📰 News Fetcher")
    st.markdown("- 💻 Code generator")
    st.markdown("- 🔎 General Facts")
    st.markdown("---")
    st.info("Example prompt:\n- `10 + 45`\n- `Convert 5 kg to pounds`\n- `Solve x^2 - 4 = 0`\n- `Latest news about AI` \n- `Python program for fibanocci`")

# Chat interface
for i, (sender, message_text) in enumerate(st.session_state.chat_history):
    is_user = sender == "You"
    message(message_text, is_user=is_user, key=str(i))

# User input
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message:", placeholder="refer example")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    st.session_state.chat_history.append(("You", user_input))

    with st.spinner("Thinking..."):
        assistant_response = agent(user_input)

    st.session_state.chat_history.append(("Assistant", assistant_response))
    st.rerun()
