import argparse
import logging
import os
import sys

from dotenv import load_dotenv

from knowledgebase import Knowledgebase
from utils.openai import validate_openai_token

# load the .env
load_dotenv()

logger = logging.getLogger(__name__)

logger.info(f"⚡ Knowledgebase initialized")

if __name__ == "__main__":
    openai_api_key = os.getenv("OPENAI_API_KEY")
    logger.info(f"The API key for the current session: {openai_api_key}")

    logger.info("🗝️ Validating the API token...")
    valid, err = validate_openai_token(openai_api_key=openai_api_key)
    if not valid:
        logger.error(err)
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description="ShoutOUT AI Website QA with LLMs - CLI"
    )
    parser.add_argument(
        "query", type=str, help="Question to be asked about ShoutOUT AI"
    )
    args = parser.parse_args()
    query = args.query

    knowledgebase = Knowledgebase(knowledgebase_name="shoutoutai_kb")
    result = knowledgebase.query_knowledgebase(
        query=query, openai_api_key=openai_api_key
    )

    print(f"\nAnswer: \n{str(result.get('answer', '').strip())}")
    print(f"\nSources: \n{str(result.get('sources', '').strip())}")
