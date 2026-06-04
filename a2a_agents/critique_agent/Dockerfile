FROM python:3.14-slim

WORKDIR /app

RUN pip install "a2a-sdk[http-server]>=0.3.4,<0.4.0" google-genai uvicorn

COPY agent.py .

CMD ["python", "agent.py"]