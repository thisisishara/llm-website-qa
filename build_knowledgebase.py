import argparse
import logging
import os
import sys

from dotenv import load_dotenv

from knowledgebase import create_knowledgebase
from utils.openai import validate_openai_token

logger = logging.getLogger(__name__)

# load the .env
load_dotenv()


if __name__ == "__main__":
    # initialize the knowledgebase
    logger.info("⚡ Initializing the URLs...")
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

    parser = argparse.ArgumentParser(description="ShoutOUT AI Knowledgebase build CLI")
    parser.add_argument(
        "-t",
        "--token",
        type=str,
        help="Question to be asked about ShoutOUT AI",
        default=os.getenv("OPENAI_API_KEY", None),
        required=False,
    )
    args = parser.parse_args()
    openai_api_key = args.token

    logger.info(f"The API key set for current session: {openai_api_key}")

    logger.info("🗝️ Validating the API token...")
    valid, err = validate_openai_token(openai_api_key=openai_api_key)
    if not valid:
        logger.error(err)
        sys.exit(1)

    logger.info("Building the knowledgebase")
    create_knowledgebase(urls=urls, openai_api_key=openai_api_key)

    logger.info("✅ Knowledgebase created")
