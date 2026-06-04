import os
import httpx
from google.adk.tools import FunctionTool

CRITIQUE_AGENT_URL = os.getenv(
    "CRITIQUE_AGENT_URL",
    "https://juxlia-critique-agent.hf.space"
)


async def critique_summary(summary: str) -> str:
    """Send a summary to the external Critique Agent and return its evaluation.

    Args:
        summary: The summary text to evaluate.

    Returns:
        The critique and quality feedback from the Critique Agent.
    """
    payload = {
        "jsonrpc": "2.0",
        "method": "message/send",
        "id": "1",
        "params": {
            "message": {
                "role": "user",
                "parts": [{"kind": "text", "text": summary}],
                "messageId": "msg-1",
            }
        }
    }
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            f"{CRITIQUE_AGENT_URL}/",
            json=payload,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        data = response.json()
        # Extract text from A2A response
        parts = data.get("result", {}).get("parts", [])
        return " ".join(p.get("text", "") for p in parts if p.get("kind") == "text")


critique_tool = FunctionTool(func=critique_summary)