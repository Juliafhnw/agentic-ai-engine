FROM python:3.14-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# Start the application
CMD ["uv", "run", "uvicorn", "agentic_ai_main:app", "--host", "0.0.0.0", "--port", "8080"]
