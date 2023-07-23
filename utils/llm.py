import openai
import streamlit as st
from huggingface_hub import InferenceClient
from streamlit.logger import get_logger

from utils.constants import AssistantType, OPENAI_CHAT_COMPLETION_MODEL

logger = get_logger(__name__)


@st.cache_data(show_spinner=False)
def validate_api_token(assistant_type: AssistantType, api_key: str) -> tuple[bool, str]:
    if not assistant_type:
        return (
            False,
            "Assistant type is not mentioned",
        )

    if not api_key:
        return (
            False,
            "Invalid API key detected",
        )

    try:
        if assistant_type == AssistantType.OPENAI.value:
            logger.info(
                f"OpenAI token validation attempt for\n{assistant_type}\n{api_key}\n"
            )
            openai.ChatCompletion.create(
                model=OPENAI_CHAT_COMPLETION_MODEL,
                messages=[{"role": "user", "content": "test"}],
                api_key=api_key,
            )
            logger.info("OpenAI token validated")
        else:
            client = InferenceClient(token=api_key)
            client.text_generation(prompt="hi", max_new_tokens=1)
            logger.info("HuggingFace token validated")

    except Exception as e:
        logger.error(f"{e.__class__.__name__}: {e}")
        return False, f"{e.__class__.__name__}: {e}"
    return True, ""
