# llm-website-qa
Enable QA on websites using LangChain

Python version: `3.10.9`

## How to run? ⚡
1. Update the `.env` with required assistant type. Currently, `hf` and `openai` are supported.
2. You should build the knowledgebase first by providing the necessary URLs in the `build_knowledgebase.py` script and then setting the required environment variables in the `.env` file to use the OpenAI models for embedding generation. (refer to the `.env.template`). URLs to scrape must be specified in the same script.  
3. After that, simply run `docker compose up -d` to spin up the container
4. Finally, open up the browser and go to `http://localhost:8501` to access the streamlit UI

## Running without containers 🚀
To run without containers, build the knowledgebase as explained above and simply run `streamlit run ./app.py` and access it through `http://localhost:8501`

```markdown
⚠️ You will either get charged or your API credits will decrease when you use the OpenAI API Key.  
Refer to their website to inquiry about the charges and rate limits associated with their API.
```

## Limitations 🤏🏽
- OpenAI API keys might sometimes not get validated properly. Issue is being investigated.
- HuggingFace Models often end up failing to handle context lengths even if `map_reduce` Document Retrieval is being used. Issue is being investigated.  
