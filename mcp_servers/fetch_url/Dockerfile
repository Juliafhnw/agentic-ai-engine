FROM python:3.14-slim

WORKDIR /app

RUN pip install httpx mcp

COPY server.py .

CMD ["python", "server.py"]