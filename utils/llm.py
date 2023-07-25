import openai
import streamlit as st
from huggingface_hub import InferenceClient
from streamlit.logger import get_logger

from utils.constants import APIKeyType, TEST_PROMPT, OPENAI_TEST_MODEL

logger = get_logger(__name__)


@st.cache_data(show_spinner=False)
def validate_api_token(api_key_type: APIKeyType, api_key: str) -> tuple[bool, str]:
    if not api_key_type:
        return (
            False,
            "API key type is not mentioned",
        )

    if not api_key:
        return (
            False,
            "Invalid API key detected",
        )

    try:
        if api_key_type == APIKeyType.OPENAI:
            openai.Completion.create(
                model=OPENAI_TEST_MODEL,
                prompt=TEST_PROMPT,
                api_key=api_key,
                max_tokens=1,
            )
            logger.info("OpenAI token validated")
        else:
            client = InferenceClient(token=api_key)
            client.text_generation(prompt=TEST_PROMPT, max_new_tokens=1)
            logger.info("HuggingFace token validated")

    except Exception as e:
        logger.error(f"{e.__class__.__name__}: {e}")
        return False, f"{e.__class__.__name__}: {e}"
    return True, ""
