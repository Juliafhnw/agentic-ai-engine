import os
import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCard, AgentCapabilities, AgentSkill
from google import genai
from google.genai import types
import json
import tempfile

CRITIQUE_INSTRUCTION = """
You are an expert critique agent. You evaluate the quality of summaries.

For each summary you receive, provide:
1. **Quality Score**: Rate from 1-10
2. **Strengths**: What the summary does well
3. **Weaknesses**: What could be improved
4. **Verdict**: A one-sentence overall assessment

Be concise but specific in your feedback.
"""

class CritiqueAgentExecutor(AgentExecutor):
    def __init__(self):
        # Load credentials from env variable (for HuggingFace deployment)
        creds_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
        if creds_json:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
                f.write(creds_json)
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = f.name

        self.client = genai.Client(
            vertexai=True,
            project=os.getenv("GOOGLE_CLOUD_PROJECT"),
            location=os.getenv("GOOGLE_CLOUD_LOCATION", "europe-north1"),
        )
        

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        user_message = context.get_user_input()
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=CRITIQUE_INSTRUCTION + "\n\nSummary to evaluate:\n" + user_message,
            config=types.GenerateContentConfig(max_output_tokens=1000),
        )
        await event_queue.enqueue_event(response.text)

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        pass


agent_card = AgentCard(
    name="Critique Agent",
    description="Evaluates the quality of summaries and provides feedback.",
    url=os.getenv("AGENT_URL", "http://localhost:7860/"),
    version="1.0.0",
    defaultInputModes=["text"],
    defaultOutputModes=["text"],
    capabilities=AgentCapabilities(streaming=False),
    skills=[
        AgentSkill(
            id="critique_summary",
            name="Critique Summary",
            description="Evaluates a summary and gives quality feedback.",
            tags=["critique", "evaluation", "summary"],
            inputModes=["text"],
            outputModes=["text"],
        )
    ],
)

handler = DefaultRequestHandler(
    agent_executor=CritiqueAgentExecutor(),
    task_store=InMemoryTaskStore(),
)

app = A2AStarletteApplication(
    agent_card=agent_card,
    http_handler=handler,
).build()

if __name__ == "__main__":
    port = int(os.getenv("PORT", "7860"))
    uvicorn.run(app, host="0.0.0.0", port=port)