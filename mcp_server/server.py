from typing import Literal

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from pydantic import BaseModel

from mcp_server.mock_data import CARDS, CARD_PROCEDURES

mcp = MCPServer("Banking Support MCP Server")


class CardStatus(BaseModel):
    customer_id: str
    last_four: str
    status: str
    replacement_status: str
    estimated_delivery: str | None


class CardProcedure(BaseModel):
    issue: str
    title: str
    steps: list[str]
    emergency_contact: str


@mcp.tool()
def get_card_status(customer_id: str) -> CardStatus:
    """
    Get the current card and replacement status for a customer.

    Use this tool when the customer asks about:
    - card status
    - replacement card status
    - card delivery
    - whether a replacement card has shipped
    """

    card = CARDS.get(customer_id)

    if card is None:
        raise ToolError(
            f"No card information was found for customer {customer_id!r}."
        )

    return CardStatus(**card)


@mcp.tool()
def get_card_procedure(
    issue: Literal["lost", "stolen"],
) -> CardProcedure:
    """
    Get the approved banking procedure for a lost or stolen card.

    This tool only retrieves instructions.
    It does not freeze, cancel, or modify the customer's card.
    """

    procedure = CARD_PROCEDURES.get(issue)

    if procedure is None:
        raise ToolError(
            f"No card procedure exists for issue {issue!r}."
        )

    return CardProcedure(**procedure)


if __name__ == "__main__":
    mcp.run()