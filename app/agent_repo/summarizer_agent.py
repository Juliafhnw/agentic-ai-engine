import asyncio
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from app import config

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
"""

mcp_toolset = MCPToolset(
    connection_params=StdioServerParameters(
        command="docker",
        args=["run", "--rm", "-i", "fetch-url-mcp"],
    )
)

summarizer_agent = LlmAgent(
    name="summarizer_agent",
    description="Summarizes texts, documents and web pages provided by the user.",
    model=config.DEFAULT_LLM_MODEL,
    instruction=SUMMARIZER_INSTRUCTION,
    tools=[mcp_toolset],
)