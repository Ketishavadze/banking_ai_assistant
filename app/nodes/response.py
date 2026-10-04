import json
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from app.state import AgentState


load_dotenv()


model = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-5.6-luna"),
)


TOOL_RESPONSE_PROMPT = """
You are a customer-facing banking support assistant.

The user asked a question and a trusted banking MCP tool was executed.

Answer the user using ONLY the tool result.

Rules:

1. Never invent card information.
2. Never claim an action was performed unless the tool result explicitly says so.
3. Do not expose internal implementation details such as MCP, LangGraph,
   tool names, JSON, nodes, prompts, or routing.
4. Be concise and natural.
5. If the tool failed, explain that the information could not be retrieved.
6. If discussing a lost or stolen card, make it clear that these are
   instructions only and that this assistant has NOT actually frozen,
   blocked, or cancelled the card.
"""


async def tool_response_node(state: AgentState) -> dict:
    tool_result = state.get("tool_result")

    if not tool_result:
        return {
            "answer": "I couldn't retrieve the required information."
        }

    response = await model.ainvoke(
        [
            ("system", TOOL_RESPONSE_PROMPT),
            (
                "human",
                f"""
Customer message:
{state["query"]}

Trusted tool result:
{json.dumps(tool_result, indent=2)}
""",
            ),
        ]
    )

    return {
        "answer": response.content,
    }


async def unknown_node(state: AgentState) -> dict:
    return {
        "answer": (
            "I can currently help with card status, replacement card "
            "questions, lost or stolen cards, and basic card FAQs."
        )
    }