from enum import Enum

KNOWLEDGEBASE_DIR = "knowledgebases"
BS_HTML_PARSER = "html.parser"
OPENAI_COMPLETIONS_MODEL = "gpt-3.5-turbo"
OPENAI_CHAT_COMPLETIONS_MODEL = "gpt-3.5-turbo"
OPENAI_TEST_MODEL = "text-ada-001"
ENV_FILE = ".env"
HF_TEXT_GENERATION_REPO_ID = "stabilityai/FreeWilly2"
# HF_TEXT_GENERATION_REPO_ID = "google/flan-t5-xxl"
# HF_TEXT_GENERATION_REPO_ID = "OpenAssistant/falcon-40b-sft-mix-1226"
# HF_TEXT_GENERATION_REPO_ID = "OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5"
TEST_PROMPT = "test"

ASSISTANT_TYPE_KEY = "ASSISTANT_TYPE"
EMBEDDING_TYPE_KEY = "EMBEDDING_TYPE"
OPENAI_API_TOKEN_KEY = "OPENAI_API_KEY"
HUGGINGFACEHUB_API_TOKEN_KEY = "HUGGINGFACEHUB_API_TOKEN"
OPENAI_KNOWLEDGEBASE_KEY = "OPENAI_KNOWLEDGEBASE"
HF_KNOWLEDGEBASE_KEY = "HF_KNOWLEDGEBASE"

TEXT_TAG = "text"
SOURCE_TAG = "source"
SOURCES_TAG = "sources"
ANSWER_TAG = "answer"
QUESTION_TAG = "question"
QUERY_TAG = "query"
NONE_TAG = "None"
EMPTY_TAG = ""
MESSAGE_HISTORY_TAG = "message_history"
USER_TAG = "user"
ASSISTANT_TAG = "assistant"
FROM_TAG = "from"
IN_PROGRESS_TAG = "in_progress"
QUERY_INPUT_TAG = "query_input"
VALID_TOKEN_TAG = "valid_token"
API_KEY_TAG = "api_key"
ASSISTANT_TYPE_TAG = "assistant_type"
TOTAL_TOKENS_TAG = "total_tokens"
PROMPT_TOKENS_TAG = "prompt_tokens"
COMPLETION_TOKENS_TAG = "completion_tokens"
TOTAL_COST_TAG = "total_cost"

USER_AVATAR = "https://i.imgur.com/Rf63hWt.png"
ASSISTANT_AVATAR = "https://i.imgur.com/NQwsRn2.png"


class AssistantType(Enum):
    HUGGINGFACE = "hf"
    OPENAI = "openai"


class APIKeyType(Enum):
    HUGGINGFACE = "hf"
    OPENAI = "openai"


class EmbeddingType(Enum):
    HUGGINGFACE = "hf"
    OPENAI = "openai"


class StNotificationType(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "err"
