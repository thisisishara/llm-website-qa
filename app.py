import logging

import streamlit as st
from dotenv import load_dotenv

from knowledgebase import Knowledgebase
from utils.openai import validate_openai_token

# load the .env
load_dotenv()

# initialize a logger
logger = logging.getLogger(__name__)

# initialize knowledgebase
knowledgebase = Knowledgebase()
logger.info(f"⚡ Knowledgebase initialized")


def show_chat_ui():
    st.header("ShoutOUT Website QA Demo powered by OpenAI LLMs")
    st.caption("⚡ Powered by :blue[LangChain] & :blue[OpenAI]")
    st.subheader("Let's start chatting, shall we?")
    st.success(f"New API Key: {st.session_state.api_key[-4:]}")

    prompt = st.chat_input("Say something")
    if prompt:
        st.write(f"User has sent the following prompt: {prompt}")

    with st.chat_message("user", avatar="https://i.imgur.com/Rf63hWt.png"):
        st.write("Hello Assistant")
    with st.chat_message("assistant", avatar="https://i.imgur.com/Latap1Y.png"):
        st.write("Hello User")


def show_intro_ui():
    st.header("ShoutOUT Website QA Demo powered by OpenAI LLMs")
    st.caption("⚡ Powered by :blue[LangChain] & :blue[OpenAI]")


def show_error_ui():
    st.header("ShoutOUT Website QA Demo powered by OpenAI LLMs")
    st.caption("⚡ Powered by :blue[LangChain] & :blue[OpenAI]")
    st.error(f"Invalid API Token detected. Please try again!")


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
        placeholder="API Key",
        type="password",
    )

    # # enable getting URLs
    # st.sidebar.info(
    #     "To get started, enter your OpenAI API key and the URL of the webpage to chat with"
    # )
    # st.sidebar.text_input(
    #     "Enter the OpenAI API Key",
    #     key="api_key",
    #     label_visibility="hidden",
    #     placeholder="API Key",
    #     type="password",
    # )
    # st.sidebar.text_input(
    #     "Enter the URL of the webpage to chat with",
    #     key="webpage_url",
    #     label_visibility="hidden",
    #     placeholder="URL",
    # )

    if st.sidebar.button("Get Started ✅"):
        if validate_openai_token(st.session_state.api_key):
            st.session_state["validated_token"] = st.session_state.api_key
        else:
            st.session_state["validated_token"] = "invalid"

    key_state = str(st.session_state["validated_token"])
    if key_state == "invalid":
        st.sidebar.warning(f"⚠️ Invalid API Token")
        show_error_ui()
    elif key_state.startswith("sk-"):
        st.sidebar.success(f"🎉 Token Validated!")
        show_chat_ui()
    else:
        show_intro_ui()


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
