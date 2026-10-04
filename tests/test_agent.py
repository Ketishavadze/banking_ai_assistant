import pytest

from app.graph import graph


@pytest.mark.asyncio
async def test_card_status_request():
    result = await graph.ainvoke(
        {
            "query": "Where is my replacement card?",
            "customer_id": "user_002",
        }
    )

    assert result["route"] == "card_status"
    assert result["selected_tool"] == "get_card_status"
    assert result["answer"]


@pytest.mark.asyncio
async def test_lost_card_request():
    result = await graph.ainvoke(
        {
            "query": "I lost my debit card.",
            "customer_id": "user_001",
        }
    )

    assert result["route"] == "lost_card"
    assert result["selected_tool"] == "get_card_procedure"
    assert result["tool_arguments"]["issue"] == "lost"


@pytest.mark.asyncio
async def test_stolen_card_request():
    result = await graph.ainvoke(
        {
            "query": "Someone stole my card.",
            "customer_id": "user_001",
        }
    )

    assert result["route"] == "stolen_card"
    assert result["selected_tool"] == "get_card_procedure"
    assert result["tool_arguments"]["issue"] == "stolen"


@pytest.mark.asyncio
async def test_faq_request_does_not_use_account_tool():
    result = await graph.ainvoke(
        {
            "query": "Can I use my card internationally?",
            "customer_id": "user_001",
        }
    )

    assert result["route"] == "faq"
    assert result.get("selected_tool") is None