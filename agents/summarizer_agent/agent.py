"""Summarizer agent for ADK Web UI – standalone version."""
import os
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
import httpx

async def fetch_url(url: str) -> dict:
    """Fetch the content of a web page."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; AgenticAI/1.0)"}
        async with httpx.AsyncClient(follow_redirects=True, timeout=15) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return {"status": "ok", "content": response.text}
    except Exception as e:
        return {"status": "error", "message": str(e)}

root_agent = LlmAgent(
    name="summarizer_agent",
    description="Summarizes texts, documents and web pages provided by the user.",
    model=os.getenv("DEFAULT_LLM_MODEL", "gemini-2.5-flash"),
    instruction="""
You are an expert summarizer agent. Your job is to create clear, concise and
well-structured summaries of any text or document the user provides.

When summarizing:
- Start with a 1-2 sentence overview of the main topic
- Extract the key points as a structured list
- End with a brief conclusion or takeaway

If the user provides a URL, use the fetch_url tool to fetch the page and summarize it.
""",
    tools=[FunctionTool(func=fetch_url)],
)
