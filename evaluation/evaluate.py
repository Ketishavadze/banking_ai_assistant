import asyncio
import json
from pathlib import Path

from app.graph import graph
from evaluation.metrics import (
    calculate_accuracy,
    contains_expected_text,
    contains_unsafe_action_claim,
)


DATASET_PATH = Path(__file__).parent / "dataset.json"


async def evaluate() -> None:
    with DATASET_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:
        dataset = json.load(file)

    total = len(dataset)

    correct_routes = 0
    correct_tools = 0
    correct_content = 0
    unsafe_attempts = 0

    results = []

    for example in dataset:
        result = await graph.ainvoke(
            {
                "query": example["query"],
                "customer_id": example["customer_id"],
            }
        )

        actual_route = result.get("route")
        actual_tool = result.get("selected_tool")
        answer = result.get("answer", "")

        route_correct = (
            actual_route
            == example["expected_route"]
        )

        tool_correct = (
            actual_tool
            == example["expected_tool"]
        )

        content_correct = contains_expected_text(
            answer,
            example["expected_contains"],
        )

        unsafe = contains_unsafe_action_claim(
            answer
        )

        correct_routes += int(route_correct)
        correct_tools += int(tool_correct)
        correct_content += int(content_correct)
        unsafe_attempts += int(unsafe)

        results.append(
            {
                "id": example["id"],
                "query": example["query"],
                "expected_route": example["expected_route"],
                "actual_route": actual_route,
                "expected_tool": example["expected_tool"],
                "actual_tool": actual_tool,
                "route_correct": route_correct,
                "tool_correct": tool_correct,
                "content_correct": content_correct,
                "unsafe_action_claim": unsafe,
                "answer": answer,
            }
        )

    print()
    print("=" * 60)
    print("BANKING AGENT EVALUATION")
    print("=" * 60)

    print(
        f"Routing accuracy: "
        f"{calculate_accuracy(correct_routes, total):.2%}"
    )

    print(
        f"Tool-selection accuracy: "
        f"{calculate_accuracy(correct_tools, total):.2%}"
    )

    print(
        f"Expected-content success: "
        f"{calculate_accuracy(correct_content, total):.2%}"
    )

    print(
        f"Unsafe action claims: "
        f"{unsafe_attempts}/{total}"
    )

    print()
    print("FAILURES")
    print("-" * 60)

    for result in results:
        if not (
            result["route_correct"]
            and result["tool_correct"]
            and result["content_correct"]
            and not result["unsafe_action_claim"]
        ):
            print()
            print(f"ID: {result['id']}")
            print(f"Query: {result['query']}")

            print(
                "Route:",
                result["actual_route"],
                "/ expected:",
                result["expected_route"],
            )

            print(
                "Tool:",
                result["actual_tool"],
                "/ expected:",
                result["expected_tool"],
            )

            print(
                "Content correct:",
                result["content_correct"],
            )

            print(
                "Unsafe:",
                result["unsafe_action_claim"],
            )

            print(
                "Answer:",
                result["answer"],
            )


if __name__ == "__main__":
    asyncio.run(evaluate())