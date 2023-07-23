import logging
import os
import sys

from dotenv import load_dotenv

from knowledgebase import create_knowledgebase
from utils.constants import (
    ASSISTANT_TYPE_KEY,
    AssistantType,
    OPENAI_API_TOKEN_KEY,
    HUGGINGFACEHUB_API_TOKEN_KEY,
    OPENAI_KNOWLEDGEBASE_KEY,
    HF_KNOWLEDGEBASE_KEY,
    ENV_FILE,
)
from utils.llm import validate_api_token

logger = logging.getLogger(__name__)

# load the .env
load_dotenv(dotenv_path=os.path.join(os.getcwd(), ENV_FILE))


if __name__ == "__main__":
    # initialize the knowledgebase
    logger.info("⚡ Initializing the URLs...")
    urls = [
        "https://www.shoutout.ai/company",
    ]

    # determine assistant type
    assistant_type = os.getenv(ASSISTANT_TYPE_KEY, AssistantType.HUGGINGFACE.value)
    if assistant_type == AssistantType.OPENAI.value:
        assistant_type = AssistantType.OPENAI
        api_key = os.getenv(OPENAI_API_TOKEN_KEY, None)
        knowledgebase_name = os.environ.get(OPENAI_KNOWLEDGEBASE_KEY, None)
    else:
        assistant_type = AssistantType.HUGGINGFACE
        api_key = os.getenv(HUGGINGFACEHUB_API_TOKEN_KEY, None)
        knowledgebase_name = os.environ.get(HF_KNOWLEDGEBASE_KEY, None)

    logger.info("🗝️ Validating the API token...")
    valid, err = validate_api_token(assistant_type=assistant_type, api_key=api_key)
    if not valid:
        logger.error(err)
        sys.exit(1)

    logger.info("Building the knowledgebase")
    create_knowledgebase(
        urls=urls,
        assistant_type=assistant_type,
        api_key=api_key,
        knowledgebase_name=knowledgebase_name,
    )

    logger.info("✅ Knowledgebase created")
