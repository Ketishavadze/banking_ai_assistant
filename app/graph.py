from langgraph.graph import END, START, StateGraph

from app.nodes.faq import faq_node
from app.nodes.response import tool_response_node, unknown_node
from app.nodes.router import router_node
from app.nodes.tools import (
    card_status_tool_node,
    lost_card_tool_node,
    stolen_card_tool_node,
)
from app.state import AgentState


def route_after_classification(state: AgentState) -> str:
    return state["route"]


builder = StateGraph(AgentState)


builder.add_node("router", router_node)
builder.add_node("faq", faq_node)

builder.add_node(
    "card_status_tool",
    card_status_tool_node,
)

builder.add_node(
    "lost_card_tool",
    lost_card_tool_node,
)

builder.add_node(
    "stolen_card_tool",
    stolen_card_tool_node,
)

builder.add_node(
    "tool_response",
    tool_response_node,
)

builder.add_node(
    "unknown",
    unknown_node,
)


builder.add_edge(
    START,
    "router",
)


builder.add_conditional_edges(
    "router",
    route_after_classification,
    {
        "faq": "faq",
        "card_status": "card_status_tool",
        "lost_card": "lost_card_tool",
        "stolen_card": "stolen_card_tool",
        "unknown": "unknown",
    },
)


builder.add_edge(
    "card_status_tool",
    "tool_response",
)

builder.add_edge(
    "lost_card_tool",
    "tool_response",
)

builder.add_edge(
    "stolen_card_tool",
    "tool_response",
)


builder.add_edge(
    "faq",
    END,
)

builder.add_edge(
    "tool_response",
    END,
)

builder.add_edge(
    "unknown",
    END,
)


graph = builder.compile()