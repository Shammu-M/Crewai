"""Streamlit view for the banking assistant."""

import streamlit as st

from controllers.chat_controller import handle_chat_prompt
from models.database import initialize_database


def render() -> None:
    st.set_page_config(page_title="Banking Assistant", page_icon="🏦")
    initialize_database()
    st.title("Banking Assistant")
    st.caption("Demo data only | User: DEMO-USER-001 | Model: openai/gpt-oss-120b via Groq")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if prompt := st.chat_input("Ask about balances, transactions, or service requests"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Checking the relevant banking specialist..."):
                answer = handle_chat_prompt(prompt)
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
