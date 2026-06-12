from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from app import config
from app.agent_repo.summarizer_team.critique_tool import critique_tool
from app.agent_repo.summarizer_team.prompt import (
    SUMMARIZER_INSTRUCTION,
    FORMATTER_INSTRUCTION,
)

mcp_toolset = MCPToolset(
    connection_params=StdioServerParameters(
        command="docker",
        args=["run", "--rm", "-i", "fetch-url-mcp"],
    )
)

summarizer_agent = LlmAgent(
    name="summarizer_agent",
    description="Summarizes texts, documents and web pages.",
    model=config.DEFAULT_LLM_MODEL,
    instruction=SUMMARIZER_INSTRUCTION,
    tools=[mcp_toolset],
    output_key="raw_summary",
)

from app.context.artifacts.artifact_tools import save_artifact, load_artifact, list_artifacts

formatter_agent = LlmAgent(
    name="formatter_agent",
    description="Formats a summary into a beautiful Markdown document and saves it as artifact.",
    model=config.DEFAULT_LLM_MODEL,
    instruction=FORMATTER_INSTRUCTION + "\n\nAfter formatting, automatically save the result as 'summary.md' using the save_artifact tool.",
    tools=[save_artifact, load_artifact, list_artifacts],
)


critique_agent = LlmAgent(
    name="critique_agent",
    description="Evaluates the quality of the formatted summary.",
    model=config.DEFAULT_LLM_MODEL,
    instruction="""\
You are a quality evaluator. Use the critique_summary tool to evaluate the summary
you receive and present the feedback clearly to the user.
""",
    tools=[critique_tool],
)

orchestrator_agent = SequentialAgent(
    name="orchestrator_agent",
    description="Orchestrates the summarization pipeline.",
    sub_agents=[summarizer_agent, formatter_agent, critique_agent],
)