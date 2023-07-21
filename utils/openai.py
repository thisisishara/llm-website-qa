import re


def validate_openai_token(api_token: str) -> bool:
    return bool(re.match(r"^(?!.*[\s\n])sk-[a-zA-Z0-9]+$", api_token))
