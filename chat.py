import argparse
import logging
import os
import sys

from dotenv import load_dotenv

from knowledgebase import Knowledgebase
from utils.constants import (
    ENV_FILE,
    ASSISTANT_TYPE_KEY,
    AssistantType,
    OPENAI_API_TOKEN_KEY,
    OPENAI_KNOWLEDGEBASE_KEY,
    HUGGINGFACEHUB_API_TOKEN_KEY,
    HF_KNOWLEDGEBASE_KEY,
    QUERY_TAG,
    ANSWER_TAG,
    SOURCES_TAG,
    EMBEDDING_TYPE_KEY,
    APIKeyType,
    EmbeddingType,
)
from utils.llm import validate_api_token

# load the .env
load_dotenv(dotenv_path=os.path.join(os.getcwd(), ENV_FILE))

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    assistant_type = os.getenv(ASSISTANT_TYPE_KEY, AssistantType.HUGGINGFACE.value)
    embedding_type = os.getenv(EMBEDDING_TYPE_KEY, EmbeddingType.HUGGINGFACE.value)

    if assistant_type == AssistantType.OPENAI.value:
        assistant_type = AssistantType.OPENAI
        assistant_api_key = os.environ.get(OPENAI_API_TOKEN_KEY, None)
        assistant_api_key_type = APIKeyType.OPENAI
        knowledgebase_name = os.environ.get(OPENAI_KNOWLEDGEBASE_KEY, None)

        if embedding_type == EmbeddingType.OPENAI.value:
            embedding_type = EmbeddingType.OPENAI
            embedding_api_key = assistant_api_key
            embedding_api_key_type = APIKeyType.OPENAI
        else:
            embedding_type = EmbeddingType.HUGGINGFACE
            embedding_api_key = os.getenv(HUGGINGFACEHUB_API_TOKEN_KEY, None)
            embedding_api_key_type = APIKeyType.HUGGINGFACE
    else:
        assistant_type = AssistantType.HUGGINGFACE
        assistant_api_key = os.environ.get(HUGGINGFACEHUB_API_TOKEN_KEY, None)
        assistant_api_key_type = APIKeyType.HUGGINGFACE
        knowledgebase_name = os.environ.get(HF_KNOWLEDGEBASE_KEY, None)
        embedding_type = EmbeddingType.HUGGINGFACE
        embedding_api_key = assistant_api_key
        embedding_api_key_type = APIKeyType.HUGGINGFACE

    logger.info("🗝️ Validating the API tokens...")
    assistant_valid, assistant_err = validate_api_token(
        api_key_type=assistant_api_key_type, api_key=assistant_api_key
    )
    if not assistant_valid:
        logger.error(assistant_err)
        sys.exit(1)

    embedding_valid, embedding_err = validate_api_token(
        api_key_type=embedding_api_key_type, api_key=embedding_api_key
    )
    if not embedding_valid:
        logger.error(embedding_err)
        sys.exit(1)

    parser = argparse.ArgumentParser(description="LLM Website QA - CLI")
    parser.add_argument(
        QUERY_TAG, type=str, help="Question to be asked from the assistant"
    )
    args = parser.parse_args()
    query = args.query

    knowledgebase = Knowledgebase(
        assistant_type=assistant_type,
        embedding_type=embedding_type,
        assistant_api_key=assistant_api_key,
        embedding_api_key=embedding_api_key,
        knowledgebase_name=knowledgebase_name,
    )
    result, metadata = knowledgebase.query_knowledgebase(query=query)

    print(f"\nAnswer: \n{str(result.get(ANSWER_TAG, '').strip())}")
    print(f"\nSources: \n{str(result.get(SOURCES_TAG, '').strip())}")
    print(f"\nCost: \n{metadata}")
