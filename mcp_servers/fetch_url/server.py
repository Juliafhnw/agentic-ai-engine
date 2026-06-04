import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("fetch-url-server")


@mcp.tool()
def fetch_url(url: str) -> str:
    """Fetch the content of a web page and return it as plain text.

    Args:
        url: The URL of the web page to fetch.

    Returns:
        The text content of the page, or an error message.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; MCP-FetchBot/1.0)"}
        with httpx.Client(follow_redirects=True, timeout=10) as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()
            return response.text
    except Exception as e:
        return f"Error fetching {url}: {e}"


if __name__ == "__main__":
    mcp.run(transport="stdio")