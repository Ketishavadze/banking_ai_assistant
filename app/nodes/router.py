import os
from typing import Literal

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from app.state import AgentState


load_dotenv()


class RouteDecision(BaseModel):
    route: Literal[
        "faq",
        "card_status",
        "lost_card",
        "stolen_card",
        "unknown",
    ] = Field(
        description="The correct destination for the user's request."
    )


model = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-5.6-luna"),
)

router_model = model.with_structured_output(RouteDecision)


ROUTER_PROMPT = """
You are an intent router for a banking support assistant.

Classify the user's message into exactly one category.

Categories:

card_status:
The customer wants information about their existing card,
replacement card, card delivery, shipping, or current card status.

lost_card:
The customer says their card is lost or they cannot find it.

stolen_card:
The customer says the card was stolen or taken.

faq:
The customer asks a general informational question about:
- card usage
- international card use
- fees
- replacement times
- PIN security
- suspicious or unrecognized transactions
- general card security
- banking card policies

Use faq when the customer is asking what they SHOULD DO about a suspicious
or unrecognized transaction, as long as they are not asking for
customer-specific transaction data.

The question must NOT require customer-specific account information.

unknown:
The message does not belong to the supported banking card topics.

Do not answer the customer.
Only classify their intent.
"""


async def router_node(state: AgentState) -> dict:
    user_query = state["query"]

    decision = await router_model.ainvoke(
        [
            ("system", ROUTER_PROMPT),
            ("human", user_query),
        ]
    )

    return {
        "route": decision.route,
    }