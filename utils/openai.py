import openai
import streamlit as st
from streamlit.logger import get_logger

logger = get_logger(__name__)


@st.cache_data(show_spinner=False)
def validate_openai_token(openai_api_key: str) -> tuple[bool, str]:
    if not openai_api_key:
        return (
            False,
            "Invalid API token detected. Enter a valid OpenAI API token to get started!",
        )
    try:
        openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "test"}],
            api_key=openai_api_key,
        )
    except Exception as e:
        logger.error(f"{e.__class__.__name__}: {e}")
        return False, f"{e.__class__.__name__}: {e}"
    return True, ""
