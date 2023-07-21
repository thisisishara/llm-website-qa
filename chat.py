import argparse
import logging
import os
import sys

from dotenv import load_dotenv
from langchain import OpenAI
from langchain.chains import VectorDBQAWithSourcesChain

from knowledgebase import load_knowledgebase
from utils.openai import validate_openai_token

# load the .env
load_dotenv()

logger = logging.getLogger(__name__)

knowledgebase = load_knowledgebase()
logger.info(f"⚡ Knowledgebase initialized")


if __name__ == "__main__":
    logger.info("🗝️ Validating the API token...")
    if not validate_openai_token(api_token=os.getenv("OPENAI_API_KEY")):
        logger.error("Invalid OpenAI API token detected.")
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description="ShoutOUT AI Website QA with LLMs - CLI"
    )
    parser.add_argument(
        "question", type=str, help="Question to be asked about ShoutOUT AI"
    )
    args = parser.parse_args()

    chain = VectorDBQAWithSourcesChain.from_llm(
        llm=OpenAI(temperature=0, verbose=True), vectorstore=knowledgebase, verbose=True
    )
    result = chain({"question": args.question})

    print(f"\nAnswer: \n{str(result['answer']).strip()}")
    print(f"\nSources: \n{result['sources']}")
