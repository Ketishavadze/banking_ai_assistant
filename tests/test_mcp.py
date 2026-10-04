import pytest

from app.mcp_client import call_mcp_tool


@pytest.mark.asyncio
async def test_get_card_status():
    result = await call_mcp_tool(
        "get_card_status",
        {
            "customer_id": "user_002",
        },
    )

    assert result["ok"] is True

    data = result["data"]

    assert data["customer_id"] == "user_002"
    assert data["last_four"] == "1934"
    assert data["replacement_status"] == "shipped"


@pytest.mark.asyncio
async def test_lost_card_procedure():
    result = await call_mcp_tool(
        "get_card_procedure",
        {
            "issue": "lost",
        },
    )

    assert result["ok"] is True

    data = result["data"]

    assert data["issue"] == "lost"
    assert len(data["steps"]) > 0


@pytest.mark.asyncio
async def test_unknown_customer_returns_error():
    result = await call_mcp_tool(
        "get_card_status",
        {
            "customer_id": "does_not_exist",
        },
    )

    assert result["ok"] is False
    assert result["data"] is None
    assert result["error"] is not None