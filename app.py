import logging
import os

import streamlit as st

from knowledgebase import Knowledgebase
from utils.constants import (
    AssistantType,
    OPENAI_KNOWLEDGEBASE_KEY,
    HUGGINGFACEHUB_API_TOKEN_KEY,
    HF_KNOWLEDGEBASE_KEY,
    SOURCES_TAG,
    ANSWER_TAG,
    NONE_TAG,
    EMPTY_TAG,
    MESSAGE_HISTORY_TAG,
    TEXT_TAG,
    USER_TAG,
    ASSISTANT_TAG,
    FROM_TAG,
    IN_PROGRESS_TAG,
    QUERY_INPUT_TAG,
    VALID_TOKEN_TAG,
    StNotificationType,
    API_KEY_TAG,
    ASSISTANT_TYPE_TAG,
    ASSISTANT_AVATAR,
    USER_AVATAR,
    EmbeddingType,
    APIKeyType,
)
from utils.llm import validate_api_token

# initialize a logger
logger = logging.getLogger(__name__)


def retrieve_answer(query: str):
    try:
        assistant_type = st.session_state.selected_assistant_type
        embedding_type = EmbeddingType.HUGGINGFACE
        assistant_api_key = st.session_state.verified_api_key
        embedding_api_key = st.session_state.embedding_api_key
        knowledgebase_name = st.session_state.knowledgebase_name

        knowledgebase = Knowledgebase(
            assistant_type=assistant_type,
            embedding_type=embedding_type,
            assistant_api_key=assistant_api_key,
            embedding_api_key=embedding_api_key,
            knowledgebase_name=knowledgebase_name,
        )
        answer = knowledgebase.query_knowledgebase(query=query)

        if answer.get(SOURCES_TAG, None) not in [None, NONE_TAG, EMPTY_TAG]:
            return f"{answer[ANSWER_TAG]}\n{answer[SOURCES_TAG]}"
        else:
            return f"{answer[ANSWER_TAG]}"
    except Exception as e:
        logger.exception(f"Invalid API key. {e}")
        return (
            f"Could not retrieve the answer. This could be due to "
            f"various reasons such as Invalid API Tokens or hitting "
            f"the Rate limit enforced by LLM vendors."
        )


def show_chat_ui():
    if (
        st.session_state.selected_assistant_type == AssistantType.HUGGINGFACE
        and not st.session_state.get(MESSAGE_HISTORY_TAG, None)
    ):
        show_notification_banner_ui(
            notification_type=StNotificationType.WARNING,
            notification="🤗🤏🏽 HuggingFace assistant is not always guaranteed "
            "to return a valid response and often exceeds the "
            "maximum token limit. Use the OpenAI assistant for "
            "more reliable responses.",
        )

    if not st.session_state.get(MESSAGE_HISTORY_TAG, None):
        st.subheader("Let's start chatting, shall we?")

    if st.session_state.get(IN_PROGRESS_TAG, False):
        query = st.chat_input(
            "Ask me about ShoutOUT AI stuff", key=QUERY_INPUT_TAG, disabled=True
        )
    else:
        query = st.chat_input("Ask me about ShoutOUT AI stuff", key=QUERY_INPUT_TAG)

    if query:
        st.session_state.in_progress = True
        current_messages = st.session_state.get(MESSAGE_HISTORY_TAG, [])
        current_messages.append({TEXT_TAG: query, FROM_TAG: USER_TAG})
        st.session_state.message_history = current_messages
        answer = retrieve_answer(query=query)
        current_messages.append({TEXT_TAG: answer, FROM_TAG: ASSISTANT_TAG})
        st.session_state.message_history = current_messages
        st.session_state.in_progress = False

    if st.session_state.get(MESSAGE_HISTORY_TAG, None):
        messages = st.session_state.message_history
        for message in messages:
            if message.get(FROM_TAG) == USER_TAG:
                with st.chat_message(USER_TAG, avatar=USER_AVATAR):
                    st.write(message.get(TEXT_TAG))

            if message.get(FROM_TAG) == ASSISTANT_TAG:
                with st.chat_message(ASSISTANT_TAG, avatar=ASSISTANT_AVATAR):
                    st.write(message.get(TEXT_TAG))


def show_hf_chat_ui():
    st.sidebar.info(
        "🤗 You are using the Hugging Face Hub models for the QA task and "
        "performance might not be as good as proprietary LLMs."
    )

    verify_token()
    validated_token = st.session_state.get(VALID_TOKEN_TAG, None)
    if validated_token is None:
        st.stop()
    if not validated_token:
        st.sidebar.error("❌ Failed to get connected to the HuggingFace Hub")
        show_notification_banner_ui(
            notification_type=StNotificationType.INFO,
            notification="Failed to get connected to the HuggingFace Hub",
        )
        st.stop()

    st.sidebar.success(f"✅ Connected to the HF Hub")
    show_chat_ui()


def show_openai_chat_ui():
    st.sidebar.info(
        "🚀 To get started, enter your OpenAI API key. Once that's done, "
        "you can ask start asking questions. Oh! one more thing, we take "
        "security seriously and we are NOT storing the API keys in any manner, "
        "so you're safe. Just revoke it after usage to make sure nothing "
        "unexpected happens."
    )
    if st.sidebar.text_input(
        "Enter the OpenAI API Key",
        key=API_KEY_TAG,
        label_visibility="hidden",
        placeholder="OpenAI API Key",
        type="password",
    ):
        verify_token()

    validated_token = st.session_state.get(VALID_TOKEN_TAG, None)
    if validated_token is None:
        st.sidebar.info(f"🗝️ Provide the API Key")
        st.stop()
    if not validated_token:
        st.sidebar.error("❌ API Key you provided is invalid")
        show_notification_banner_ui(
            notification_type=StNotificationType.INFO,
            notification="Please provide a valid OpenAI API Key",
        )
        st.stop()

    st.sidebar.success(f"✅ Token Validated!")
    show_chat_ui()


def show_notification_banner_ui(
    notification_type: StNotificationType, notification: str
):
    if notification_type == StNotificationType.INFO:
        st.info(notification)
    elif notification_type == StNotificationType.WARNING:
        st.warning(notification)
    elif notification_type == StNotificationType.ERROR:
        st.error(notification)


def verify_token():
    from dotenv import load_dotenv

    load_dotenv()

    embedding_api_key = os.getenv(HUGGINGFACEHUB_API_TOKEN_KEY, None)
    st_assistant_type = st.session_state.selected_assistant_type
    if st_assistant_type == AssistantType.OPENAI:
        assistant_api_key = st.session_state.get(API_KEY_TAG, None)
        assistant_api_key_type = APIKeyType.OPENAI
        knowledgebase_name = os.environ.get(OPENAI_KNOWLEDGEBASE_KEY, None)
    else:
        assistant_api_key = os.getenv(HUGGINGFACEHUB_API_TOKEN_KEY, None)
        assistant_api_key_type = APIKeyType.HUGGINGFACE
        knowledgebase_name = os.environ.get(HF_KNOWLEDGEBASE_KEY, None)

    logger.info(
        f"The API key for the current st session: {assistant_api_key}\n"
        f"The Knowledgebase for the current st session: {knowledgebase_name}"
    )

    assistant_valid, assistant_err = validate_api_token(
        api_key_type=assistant_api_key_type,
        api_key=assistant_api_key,
    )
    embedding_valid, embedding_err = validate_api_token(
        api_key_type=APIKeyType.HUGGINGFACE,
        api_key=embedding_api_key,
    )

    if assistant_valid and embedding_valid:
        st.session_state.valid_token = True
        st.session_state.verified_api_key = assistant_api_key
        st.session_state.embedding_api_key = embedding_api_key
        st.session_state.knowledgebase_name = knowledgebase_name
    elif not assistant_valid and not embedding_valid:
        st.session_state.valid_token = False
        st.session_state.token_err = f"{assistant_err}\n{embedding_err}"
    elif not assistant_valid:
        st.session_state.valid_token = False
        st.session_state.token_err = assistant_err
    elif not embedding_valid:
        st.session_state.valid_token = False
        st.session_state.token_err = embedding_err
    else:
        st.session_state.valid_token = False
        st.session_state.token_err = (
            "An unknown error occurred while validating the API keys"
        )


def app():
    # sidebar
    st.sidebar.image(
        "https://thisisishara.com/res/images/favicon/android-chrome-192x192.png",
        width=80,
    )
    if st.sidebar.selectbox(
        "Assistant Type",
        ["OpenAI", "Hugging Face"],
        key=ASSISTANT_TYPE_TAG,
        placeholder="Select Assistant Type",
    ):
        if str(st.session_state.assistant_type).lower() == AssistantType.OPENAI.value:
            st.session_state.selected_assistant_type = AssistantType.OPENAI
        else:
            st.session_state.selected_assistant_type = AssistantType.HUGGINGFACE
        st.session_state.valid_token = None
        st.session_state.verified_api_key = None
        st.session_state.knowledgebase_name = None

    st.write(st.session_state.selected_assistant_type)

    # main section
    st.header("LLM Website QA Demo")
    st.caption("⚡ Powered by :blue[LangChain], :green[OpenAI] & :green[Hugging Face]")

    assistant_type = st.session_state.selected_assistant_type
    if assistant_type == AssistantType.OPENAI:
        show_openai_chat_ui()
    elif assistant_type == AssistantType.HUGGINGFACE:
        show_hf_chat_ui()
    else:
        show_notification_banner_ui(
            notification_type=StNotificationType.INFO,
            notification="Please select an assistant type to get started!",
        )


if __name__ == "__main__":
    st.set_page_config(
        page_title="Website QA powered by LangChain & LLMs",
        page_icon="https://thisisishara.com/res/images/favicon/android-chrome-192x192.png",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    hide_streamlit_style = """
                <style>
                # #MainMenu {visibility: hidden;}
                # footer {visibility: hidden;}
                [data-testid="stDecoration"] {background: linear-gradient(to right, #9EE51A, #208BBC) !important;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # run the app
    app()
