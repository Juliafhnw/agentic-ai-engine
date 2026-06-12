"""Agent registry – maps agent_id to LlmAgent instances and display metadata.

To add a new agent:
  1. Create a new sub-package under agent_repo/
  2. Import the agent here
  3. Add an entry to AGENT_REGISTRY
"""

from google.adk.agents import LlmAgent
from google.adk.tools import AgentTool

from app.agent_repo.greeting_agent import greeting_agent

from app.agent_repo.summarizer_agent import summarizer_agent
from app.agent_repo.summarizer_team import orchestrator_agent


from app.context.artifacts.artifact_tools import save_artifact, load_artifact, list_artifacts

try:
    from google.adk.tools import preload_memory, load_memory
    _MEMORY_TOOLS = {preload_memory, load_memory}
except ImportError:
    _MEMORY_TOOLS = set()

_ARTIFACT_FUNCTIONS = {save_artifact, load_artifact, list_artifacts}


AGENT_REGISTRY: dict[str, dict] = {
    "greeting_agent": {
        "agent": greeting_agent,
        "label": "Welcome",
        "description": "Welcomes students and helps them get started.",
        "icon": "👋",
    },
    "summarizer_agent": {
        "agent": summarizer_agent,
        "label": "Summarizer",
        "description": "Summarizes texts and documents provided by the user.",
        "icon": "📝",
    },
    "summarizer_team": {
        "agent": orchestrator_agent,
        "label": "Summarizer Team",
        "description": "A team of agents that fetches, summarizes and formats content.",
        "icon": "🤖",
    }
}


def get_agent(agent_id: str) -> LlmAgent:
    """Look up an agent by ID. Raises KeyError if not found."""
    entry = AGENT_REGISTRY[agent_id]
    return entry["agent"]


def list_agents() -> list[dict]:
    """Return metadata for all registered agents (for the UI)."""
    return [
        {
            "id": agent_id,
            "label": meta["label"],
            "description": meta["description"],
            "icon": meta["icon"],
            "has_artifacts": has_artifact_tools(meta["agent"]),
            "has_memory": has_memory_tools(meta["agent"]),
            "has_rag": has_rag_tools(meta["agent"]),
        }
        for agent_id, meta in AGENT_REGISTRY.items()
    ]

def has_artifact_tools(agent: LlmAgent) -> bool:
    """Check whether *agent* has any of the artifact tool functions."""
    tools = getattr(agent, 'tools', None) or []
    for tool in tools:
        func = getattr(tool, "func", tool)
        if func in _ARTIFACT_FUNCTIONS:
            return True
    return False


def has_memory_tools(agent: LlmAgent) -> bool:
    """Check whether *agent* has any memory tools (preload or load)."""
    tools = getattr(agent, 'tools', None) or []
    for tool in tools:
        if type(tool).__name__ in ('PreloadMemoryTool', 'LoadMemoryTool'):
            return True
    return False

def has_rag_tools(agent: LlmAgent) -> bool:
    tools = getattr(agent, 'tools', None) or []
    for tool in tools:
        func = getattr(tool, 'func', tool)
        if callable(func) and getattr(func, '__name__', '') == 'search_rag_corpus':
            return True
    return False
