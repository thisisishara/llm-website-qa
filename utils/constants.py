from enum import Enum

KNOWLEDGEBASE_DIR = "knowledgebases"
BS_HTML_PARSER = "html.parser"
OPENAI_CHAT_COMPLETION_MODEL = "gpt-3.5-turbo"
ENV_FILE = ".env"
HF_TEXT_GENERATION_REPO_ID = "google/flan-t5-xxl"
# "OpenAssistant/falcon-40b-sft-mix-1226"
# "OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5"

ASSISTANT_TYPE_KEY = "ASSISTANT_TYPE"
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

USER_AVATAR = "https://i.imgur.com/Rf63hWt.png"
ASSISTANT_AVATAR = "https://i.imgur.com/NQwsRn2.png"


class AssistantType(Enum):
    HUGGINGFACE = "hf"
    OPENAI = "openai"


class StNotificationType(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "err"
