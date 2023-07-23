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
)
from utils.llm import validate_api_token

# load the .env
load_dotenv(dotenv_path=os.path.join(os.getcwd(), ENV_FILE))

logger = logging.getLogger(__name__)


if __name__ == "__main__":
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

    logger.info(f"The API key for the current session: {api_key}")
    logger.info(f"The knowledgebase for the current session: {knowledgebase_name}")

    logger.info("🗝️ Validating the API token...")
    valid, err = validate_api_token(assistant_type=assistant_type, api_key=str(api_key))
    if not valid:
        logger.error(err)
        sys.exit(1)

    parser = argparse.ArgumentParser(description="LLM Website QA - CLI")
    parser.add_argument(
        QUERY_TAG, type=str, help="Question to be asked from the assistant"
    )
    args = parser.parse_args()
    query = args.query

    knowledgebase = Knowledgebase(
        assistant_type=assistant_type,
        api_key=str(api_key),
        knowledgebase_name=knowledgebase_name,
    )
    result = knowledgebase.query_knowledgebase(query=query)

    print(f"\nAnswer: \n{str(result.get(ANSWER_TAG, '').strip())}")
    print(f"\nSources: \n{str(result.get(SOURCES_TAG, '').strip())}")
