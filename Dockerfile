FROM python:3.12.10-slim
WORKDIR /app
COPY requirements.txt .
COPY main.py .
COPY UI.py .
COPY .env .
EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
RUN pip install -r requirements.txt
ENTRYPOINT ["streamlit", "run", "UI.py", "--server.port=8501", "--server.address=0.0.0.0"]
