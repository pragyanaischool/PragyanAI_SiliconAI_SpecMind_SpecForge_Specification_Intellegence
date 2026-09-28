import streamlit as st


def init_session_state():
    """Initializes persistent session state variables for Streamlit."""
    if "contract" not in st.session_state:
        st.session_state.contract = None
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "requirements" not in st.session_state:
        st.session_state.requirements = []
    if "groq_api_key" not in st.session_state:
        st.session_state.groq_api_key = ""
