import asyncio

from app.graph import graph


CUSTOMER_ID = "user_002"


async def main() -> None:
    print("=" * 60)
    print("Banking Support Assistant")
    print("=" * 60)
    print()
    print(f"Demo customer: {CUSTOMER_ID}")
    print("Type 'exit' to quit.")
    print()

    while True:
        query = input("You: ").strip()

        if not query:
            continue

        if query.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        result = await graph.ainvoke(
            {
                "query": query,
                "customer_id": CUSTOMER_ID,
            }
        )

        print()
        print(f"Assistant: {result['answer']}")

        print()
        print(
            f"[debug] route={result.get('route')} "
            f"tool={result.get('selected_tool')}"
        )

        print()


if __name__ == "__main__":
    asyncio.run(main())