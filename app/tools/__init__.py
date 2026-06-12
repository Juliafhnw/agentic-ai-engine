"""fetch_url tool – fetches web page content directly via httpx."""

import httpx
from google.adk.tools import FunctionTool


async def fetch_url(url: str) -> dict:
    """Fetch the content of a web page and return it as plain text.

    Args:
        url: The URL of the web page to fetch.

    Returns:
        A dict with the page content or an error message.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; AgenticAI/1.0)"}
        async with httpx.AsyncClient(follow_redirects=True, timeout=15) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return {"status": "ok", "content": response.text}
    except Exception as e:
        return {"status": "error", "message": str(e)}


fetch_url_tool = FunctionTool(func=fetch_url)