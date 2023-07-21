import logging
import os

import streamlit as st

from knowledgebase import Knowledgebase
from utils.openai import validate_openai_token

# initialize a logger
logger = logging.getLogger(__name__)

# initialize knowledgebase
knowledgebase = Knowledgebase(
    knowledgebase_name=os.getenv("KNOWLEDGEBASE", "shoutoutai_kb")
)
logger.info(f"⚡ Knowledgebase initialized")


def retrieve_answer(query: str):
    try:
        answer = knowledgebase.query_knowledgebase(
            query=query, openai_api_key=st.session_state.validated_token
        )
        if answer.get("sources", None) not in [None, "None", ""]:
            return f"{answer['answer']}\n{answer['sources']}"
        else:
            return f"{answer['answer']}"
    except Exception as e:
        logger.exception(f"Invalid API key. {e}")
        return (
            f"Could not retrieve the answer. This could be due to "
            f"various reasons such as Invalid API Token or hitting "
            f"the Rate limit enforced by OpenAI."
        )


def show_chat_ui():
    if not st.session_state.get("message_history", None):
        st.subheader("Let's start chatting, shall we?")

    if st.session_state.get("in_progress", False):
        query = st.chat_input(
            "Ask me about ShoutOUT AI stuff", key="query_input", disabled=True
        )
    else:
        query = st.chat_input("Ask me about ShoutOUT AI stuff", key="query_input")

    if query:
        st.session_state.in_progress = True
        current_messages = st.session_state.get("message_history", [])
        current_messages.append({"text": query, "from": "user"})
        st.session_state.message_history = current_messages
        answer = retrieve_answer(query=query)
        current_messages.append({"text": answer, "from": "assistant"})
        st.session_state.message_history = current_messages
        st.session_state.in_progress = False

    if st.session_state.get("message_history", None):
        messages = st.session_state.message_history
        for message in messages:
            if message.get("from") == "user":
                with st.chat_message("user", avatar="https://i.imgur.com/Rf63hWt.png"):
                    st.write(message.get("text"))

            if message.get("from") == "assistant":
                with st.chat_message(
                    "assistant", avatar="https://i.imgur.com/Latap1Y.png"
                ):
                    st.write(message.get("text"))


def show_error_ui():
    st.error(st.session_state.token_err)


def verify_token():
    valid, err = validate_openai_token(openai_api_key=st.session_state.get('api_key', None))
    if valid:
        st.session_state.validated_token = st.session_state.api_key
    else:
        st.session_state.validated_token = "invalid"
        st.session_state.token_err = err


def app():
    # sidebar
    st.sidebar.image("https://i.imgur.com/CtQmI3J.png", width=150)
    st.sidebar.info(
        "🚀 To get started, enter your OpenAI API key. Once that's done, "
        "you can ask anything related to ShoutOUT AI related products. Oh! "
        "one more thing, we take security seriously and we are NOT storing "
        "the API keys in any manner, so you're safe. Just revoke it after "
        "usage to make sure nothing unexpected happens."
    )
    st.sidebar.text_input(
        "Enter the OpenAI API Key",
        key="api_key",
        label_visibility="hidden",
        placeholder="OpenAI API Key",
        type="password",
    )

    if st.sidebar.button("Get Started ✅", key="verify_button"):
        verify_token()

    # perform verification on startup
    verify_token()

    # main section
    st.header("ShoutOUT Website QA Demo powered by OpenAI LLMs")
    st.caption("⚡ Powered by :blue[LangChain] & :blue[OpenAI]")

    key_state = str(st.session_state.validated_token)
    if key_state == "invalid":
        st.sidebar.warning(f"⚠️ Invalid API Token")
        show_error_ui()
    elif key_state.startswith("sk-"):
        st.sidebar.success(f"🎉 Token Validated!")
        show_chat_ui()


if __name__ == "__main__":
    st.set_page_config(
        page_title="ShoutOUT AI Website QA powered by OpenAI LLMs",
        page_icon="https://i.imgur.com/xUd9ypU.png",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # run the app
    app()
