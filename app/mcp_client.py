from typing import Any

from mcp import Client
from mcp.types import TextContent

from mcp_server.server import mcp


async def call_mcp_tool(
    tool_name: str,
    arguments: dict[str, Any],
) -> dict[str, Any]:
    """
    Call one of our banking MCP tools through a real MCP client.

    For V1 we connect directly to the MCP server object in memory.
    """

    async with Client(mcp) as client:
        result = await client.call_tool(
            tool_name,
            arguments,
        )

        if result.is_error:
            error_messages = []

            for block in result.content:
                if isinstance(block, TextContent):
                    error_messages.append(block.text)

            return {
                "ok": False,
                "error": " ".join(error_messages),
                "data": None,
            }

        return {
            "ok": True,
            "error": None,
            "data": result.structured_content,
        }