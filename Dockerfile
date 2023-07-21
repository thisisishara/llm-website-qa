FROM python:3.10.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# building the knowledgebase
# when the app is being deployed
RUN python3 ./build_knowledgebase.py

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port", "8501"]
