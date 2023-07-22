# llm-website-qa
Enable QA on websites using LangChain

Python version: `3.10.9`

## How to run?
1. You should build the knowledgebase first by providing the necessary URLs in the `build_knowledgebase.py` script and then setting the required environment variables in the `.env` file to use the OpenAI models for embedding generation. (refer to the `.env.template`)
2. After that, simply run `docker compose up -d` to spin up the container
3. Finally, open up the browser and go to `http://localhost:8501` to access the streamlit UI

## Running without containers
To run without containers, build the knowledgebase as explained above and simply run `streamlit run ./app.py` and access it through `http://localhost:8501`

```markdown
⚠️ You will either get charged or your API credits will decrease when you use the OpenAI API Key.  
Refer to their website to inquiry about the charges and rate limits associated with their API.
```
