from typing import Any, Literal, TypedDict


Route = Literal[
    "faq",
    "card_status",
    "lost_card",
    "stolen_card",
    "unknown",
]


class AgentState(TypedDict, total=False):
    query: str
    customer_id: str

    route: Route

    selected_tool: str | None
    tool_arguments: dict[str, Any] | None
    tool_result: dict[str, Any] | None

    answer: str