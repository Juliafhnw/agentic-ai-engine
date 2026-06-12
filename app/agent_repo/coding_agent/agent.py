"""Coding agent – investigates and explains source code."""

from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from app import config
from app.agent_repo.coding_agent.prompt import CODING_AGENT_INSTRUCTION
import os


def read_file(filepath: str) -> dict:
    """Read the contents of a source file.

    Args:
        filepath: Absolute or relative path to the file.

    Returns:
        A dict with the file contents or an error message.
    """
    try:
        with open(filepath, "r") as f:
            content = f.read()
        return {"status": "ok", "content": content, "lines": len(content.splitlines())}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def list_directory(dirpath: str) -> dict:
    """List files in a directory.

    Args:
        dirpath: Path to the directory.

    Returns:
        A dict with the list of files.
    """
    try:
        files = os.listdir(dirpath)
        return {"status": "ok", "files": sorted(files)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


coding_agent = LlmAgent(
    name="coding_agent",
    description="Investigates and explains ADK source code and implementation details.",
    model=config.DEFAULT_LLM_MODEL,
    instruction=CODING_AGENT_INSTRUCTION,
    tools=[FunctionTool(func=read_file), FunctionTool(func=list_directory)],
)