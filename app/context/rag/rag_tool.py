"""RAG retrieval tool – searches the Vertex AI RAG corpus."""

from google.adk.agents import LlmAgent
from google.adk.tools import AgentTool
import vertexai as _vertexai
from vertexai.preview import rag
from vertexai.preview.generative_models import GenerativeModel, Tool
from app import config
from app.context.rag.rag_engine_handler import rag_engine_handler


async def search_rag_corpus(query: str) -> dict:
    """Search the RAG corpus for relevant documents.

    Args:
        query: The search query to find relevant documents.

    Returns:
        A dict with the retrieved text chunks.
    """
    if not rag_engine_handler.available:
        return {"status": "error", "message": "RAG corpus not available"}

    try:
        _vertexai.init(
            project=config.GOOGLE_CLOUD_PROJECT,
            location=config.GOOGLE_CLOUD_LOCATION,
        )
        rag_retrieval_tool = rag.RagResource(
            rag_corpus=rag_engine_handler.corpus_name,
        )
        response = rag.retrieval_query(
            rag_resources=[rag_retrieval_tool],
            text=query,
            similarity_top_k=5,
        )
        contexts = []
        for context in response.contexts.contexts:
            contexts.append({
                "text": context.text,
                "source": context.source_uri,
                "score": context.score,
            })
        return {"status": "ok", "contexts": contexts}
    except Exception as e:
        return {"status": "error", "message": str(e)}