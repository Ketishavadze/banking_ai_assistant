import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from app.state import AgentState


load_dotenv()


model = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-5.6-luna"),
)


FAQ_KNOWLEDGE = """
BANK CARD FAQ

International use:
Cards can be used internationally wherever the card network is accepted.
Customers should check foreign transaction fees before travelling.

Replacement cards:
A standard replacement card usually arrives within 5 to 7 business days.

PIN:
Customers should never share their PIN with another person, including
someone claiming to be a bank employee.

Lost cards:
Customers should temporarily freeze a missing card as soon as possible.

Stolen cards:
Customers should freeze the card immediately and contact banking support.

Suspicious transactions:
Customers should report transactions they do not recognize as soon as possible.

Card security:
The bank will never ask a customer to provide their full PIN through chat.
"""


FAQ_SYSTEM_PROMPT = f"""
You are a banking support assistant.

Answer the customer's question using ONLY the information contained
in the knowledge base below.

Do not invent banking policies, fees, limits, or procedures.

If the knowledge base does not contain enough information, say:

"I don't have enough verified information to answer that question."

Keep the response short and helpful.

KNOWLEDGE BASE:

{FAQ_KNOWLEDGE}
"""


async def faq_node(state: AgentState) -> dict:
    response = await model.ainvoke(
        [
            ("system", FAQ_SYSTEM_PROMPT),
            ("human", state["query"]),
        ]
    )

    return {
        "answer": response.content,
    }