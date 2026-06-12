"""Artifact tools – ADK function tools for saving and loading artifacts via GCS."""

from google.adk.tools.tool_context import ToolContext
from google.genai import types as genai_types

async def save_artifact(filename: str, content: str, tool_context: ToolContext) -> dict:
    """Save text content as an artifact in Google Cloud Storage.

    Args:
        filename: The name of the artifact file (e.g. 'summary.md', 'summary.pdf', 'summary.txt').
        content: The text content to save.

    Returns:
        A dict with status and filename.
    """
    # Determine mime type from filename
    if filename.endswith(".pdf"):
        mime_type = "application/pdf"
    elif filename.endswith(".md"):
        mime_type = "text/markdown"
    elif filename.endswith(".html"):
        mime_type = "text/html"
    else:
        mime_type = "text/plain"

    artifact = genai_types.Part(
        inline_data=genai_types.Blob(
            mime_type=mime_type,
            data=content.encode("utf-8"),
        )
    )
    await tool_context.save_artifact(filename=filename, artifact=artifact)
    return {"status": "ok", "filename": filename}


async def load_artifact(filename: str, tool_context: ToolContext) -> dict:
    """Load a previously saved artifact from Google Cloud Storage.

    Args:
        filename: The name of the artifact file to load.

    Returns:
        A dict with status and content.
    """
    artifact = await tool_context.load_artifact(filename=filename)
    if artifact is None:
        return {"status": "error", "message": f"Artifact '{filename}' not found."}
    content = artifact.inline_data.data.decode("utf-8")
    return {"status": "ok", "filename": filename, "content": content}


async def list_artifacts(tool_context: ToolContext) -> dict:
    """List all saved artifacts.

    Returns:
        A dict with a list of artifact filenames.
    """
    filenames = await tool_context.list_artifacts()
    return {"status": "ok", "artifacts": filenames}