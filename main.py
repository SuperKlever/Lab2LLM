import argparse
from typing import Any, Dict

from src.graph.workflow import build_workflow
from src.memory.session_memory import SessionMemory


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Учебный ассистент (LangGraph).")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Показывать промежуточные состояния графа.",
    )
    return parser.parse_args()


def main() -> None:
    """CLI loop to demo the LangGraph multi-agent system."""

    args = parse_args()
    memory = SessionMemory()
    app = build_workflow().compile()

    png_bytes = app.get_graph().draw_mermaid_png()
    with open("graph.png", "wb") as f:
        f.write(png_bytes)

    print("Учебный ассистент готов. Напишите вопрос (или 'exit').")
    while True:
        question = input("> ").strip()
        if question.lower() in {"exit", "quit"}:
            break

        state = memory.load()
        state["question"] = question

        if args.debug or 1:
            result: Dict[str, Any] = {}
            print("[DEBUG] Запуск графа.")
            for step in app.stream(state, stream_mode="values"):
                print("[DEBUG]", step)
                result = step
        else:
            result = app.invoke(state)

        memory.update(**result)

        answer = result.get("answer") or "Нет ответа."
        print(answer)


if __name__ == "__main__":
    main()
