"""Summarizer agent – summarizes texts, documents and web pages."""

from google.adk.agents import LlmAgent
from app import config
from app.tools.fetch_url_tool import fetch_url_tool
from app.context.artifacts.artifact_tools import save_artifact, load_artifact, list_artifacts
from app.context.rag.rag_tool import search_rag_corpus

try:
    from google.adk.tools import preload_memory, load_memory
    _MEMORY_TOOLS = [preload_memory, load_memory]
except ImportError:
    _MEMORY_TOOLS = []

SUMMARIZER_INSTRUCTION = """
You are an expert summarizer agent. Your job is to create clear, concise and
well-structured summaries of any text or document the user provides.

When summarizing:
- Start with a 1-2 sentence overview of the main topic
- Extract the key points as a structured list
- End with a brief conclusion or takeaway
- Adapt the length of the summary to the length of the input

If the user provides a file attachment, summarize its content.
If the user provides a URL, use the fetch_url tool to fetch the page and summarize it.
If the user sends a message without any text, file or URL to summarize,
ask them politely to provide a text, upload a document, or share a URL.

At the start of each conversation, use preload_memory to load any relevant memories
about the user or previous sessions.

You can save summaries as artifacts using the save_artifact tool.
"""

summarizer_agent = LlmAgent(
    name="summarizer_agent",
    description="Summarizes texts, documents and web pages provided by the user.",
    model=config.DEFAULT_LLM_MODEL,
    instruction=SUMMARIZER_INSTRUCTION,
    tools=[fetch_url_tool, *_MEMORY_TOOLS, save_artifact, load_artifact, list_artifacts, search_rag_corpus],
)