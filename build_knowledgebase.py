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
    EMBEDDING_TYPE_KEY,
    EmbeddingType,
    APIKeyType,
)
from utils.llm import validate_api_token

logger = logging.getLogger(__name__)

# load the .env
load_dotenv(dotenv_path=os.path.join(os.getcwd(), ENV_FILE))


if __name__ == "__main__":
    # initialize the knowledgebase
    logger.info("⚡ Initializing the URLs...")

    # determine assistant type
    assistant_type = os.getenv(ASSISTANT_TYPE_KEY, AssistantType.HUGGINGFACE.value)
    embedding_type = os.getenv(EMBEDDING_TYPE_KEY, EmbeddingType.HUGGINGFACE.value)

    if assistant_type == AssistantType.OPENAI.value:
        assistant_type = AssistantType.OPENAI
        knowledgebase_name = os.environ.get(OPENAI_KNOWLEDGEBASE_KEY, None)

        if embedding_type == EmbeddingType.OPENAI.value:
            embedding_type = EmbeddingType.OPENAI
            embedding_api_key = os.getenv(OPENAI_API_TOKEN_KEY, None)
            embedding_api_key_type = APIKeyType.OPENAI
        else:
            embedding_type = EmbeddingType.HUGGINGFACE
            embedding_api_key = os.getenv(HUGGINGFACEHUB_API_TOKEN_KEY, None)
            embedding_api_key_type = APIKeyType.HUGGINGFACE

    else:
        assistant_type = AssistantType.HUGGINGFACE
        knowledgebase_name = os.environ.get(HF_KNOWLEDGEBASE_KEY, None)
        embedding_type = EmbeddingType.HUGGINGFACE
        embedding_api_key = os.getenv(HUGGINGFACEHUB_API_TOKEN_KEY, None)
        embedding_api_key_type = APIKeyType.HUGGINGFACE

    if embedding_type == EmbeddingType.OPENAI:
        urls = [
            "https://www.shoutout.ai/pricing",
            "https://www.shoutout.ai/company",
            "https://www.shoutout.ai/omnichannel-inbox",
        ]

    else:
        urls = [
            "https://www.shoutout.ai/",
            "https://www.shoutout.ai/pricing",
            "https://www.shoutout.ai/company",
            "https://www.shoutout.ai/conversational-banking",
            "https://www.shoutout.ai/conversational-ai-for-travel-and-hospitality",
            "https://www.shoutout.ai/conversational-ai-for-healthcare",
            "https://www.shoutout.ai/conversational-ai-in-education",
            "https://www.shoutout.ai/omnichannel-customer-service",
            "https://www.shoutout.ai/website-conversion-rate-optimization-services",
            "https://www.shoutout.ai/conversational-ai",
            "https://www.shoutout.ai/omnichannel-inbox",
            "https://www.shoutout.ai/knowledge-base-help-center",
            "https://www.shoutout.ai/whatsapp-chatbot",
            "https://www.shoutout.ai/facebook-messenger",
            "https://www.shoutout.ai/website-chatbots",
            "https://www.shoutout.ai/telegram-chatbots",
            "https://www.shoutout.ai/shared-inbox",
        ]

    logger.info("🗝️ Validating the embedding API token...")
    embedding_valid, embedding_err = validate_api_token(
        api_key_type=embedding_api_key_type, api_key=embedding_api_key
    )
    if not embedding_valid:
        logger.error(embedding_err)
        sys.exit(1)

    create_knowledgebase(
        urls=urls,
        assistant_type=assistant_type,
        embedding_type=embedding_type,
        embedding_api_key=embedding_api_key,
        knowledgebase_name=knowledgebase_name,
    )

    logger.info("✅ Knowledgebase created")
