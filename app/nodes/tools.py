from app.mcp_client import call_mcp_tool
from app.state import AgentState


async def card_status_tool_node(state: AgentState) -> dict:
    tool_name = "get_card_status"

    arguments = {
        "customer_id": state["customer_id"],
    }

    result = await call_mcp_tool(
        tool_name=tool_name,
        arguments=arguments,
    )

    return {
        "selected_tool": tool_name,
        "tool_arguments": arguments,
        "tool_result": result,
    }


async def lost_card_tool_node(state: AgentState) -> dict:
    tool_name = "get_card_procedure"

    arguments = {
        "issue": "lost",
    }

    result = await call_mcp_tool(
        tool_name=tool_name,
        arguments=arguments,
    )

    return {
        "selected_tool": tool_name,
        "tool_arguments": arguments,
        "tool_result": result,
    }


async def stolen_card_tool_node(state: AgentState) -> dict:
    tool_name = "get_card_procedure"

    arguments = {
        "issue": "stolen",
    }

    result = await call_mcp_tool(
        tool_name=tool_name,
        arguments=arguments,
    )

    return {
        "selected_tool": tool_name,
        "tool_arguments": arguments,
        "tool_result": result,
    }