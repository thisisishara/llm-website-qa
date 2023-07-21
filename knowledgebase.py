import os
import pickle

import requests
from bs4 import BeautifulSoup
from langchain import VectorDBQAWithSourcesChain, OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from streamlit.logger import get_logger

logger = get_logger(__name__)


def load_knowledgebase(
    knowledgebase_name: str = os.getenv("KNOWLEDGEBASE", "shoutoutai_kb")
):
    with open(f"knowledgebases/{knowledgebase_name}.pkl", "rb") as f:
        knowledgebase = pickle.load(f)
    return knowledgebase


def create_knowledgebase(urls: list, openai_api_key: str):
    pages: list[dict] = []
    for url in urls:
        pages.append({"text": extract_text_from(url_=url), "source": url})

    text_splitter = CharacterTextSplitter(chunk_size=1500, separator="\n")

    docs, metadata = [], []
    for page in pages:
        splits = text_splitter.split_text(page["text"])
        docs.extend(splits)
        metadata.extend([{"source": page["source"]}] * len(splits))
        print(f"Split {page['source']} into {len(splits)} chunks")

    store = FAISS.from_texts(
        docs, OpenAIEmbeddings(openai_api_key=openai_api_key), metadatas=metadata
    )

    with open("knowledgebases/shoutoutai_kb.pkl", "wb") as f:
        pickle.dump(store, f)
        logger.info("Knowledgebase created successfully")


def extract_text_from(url_: str):
    html = requests.get(url_).text
    soup = BeautifulSoup(html, features="html.parser")
    text = soup.get_text()

    lines = (line.strip() for line in text.splitlines())
    return "\n".join(line for line in lines if line)


def construct_query_response(result: dict) -> dict:
    return {"answer": result}


class Knowledgebase:
    def __init__(
        self, knowledgebase_name: str = os.getenv("KNOWLEDGEBASE", "shoutoutai_kb")
    ):
        self.knowledgebase = load_knowledgebase(knowledgebase_name=knowledgebase_name)

    def query_knowledgebase(self, query: str, openai_api_key: str = None):
        try:
            logger.info(f"The API key for the session was set to: sk-***{openai_api_key[-4:]}")

            query = query.strip()
            if not query:
                return {
                    "answer": "Oh snap! did you hit send accidentally, "
                    "because I can't see any questions 🤔"
                }

            chain = VectorDBQAWithSourcesChain.from_llm(
                llm=OpenAI(temperature=0, verbose=True, openai_api_key=openai_api_key),
                vectorstore=self.knowledgebase,
                verbose=True,
            )
            result = chain({"question": query})
            return result
        except Exception as e:
            logger.error(f"{e.__class__.__name__}: {e}")
            return {"answer": f"{e.__class__.__name__}: {e}"}
