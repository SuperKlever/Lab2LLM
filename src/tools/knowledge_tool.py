from langchain_core.tools import tool

KNOWLEDGE_BASE = {
    "производная": (
        "Производная показывает скорость изменения функции. Формально это предел "
        "отношения приращения функции к приращению аргумента."
    ),
    "интеграл": (
        "Интеграл — обобщение суммы бесконечно малого. Используется для вычисления "
        "площадей, объемов и накопленных величин."
    ),
    "сирус": (
        "Сирус (Пробудитель миров) — это финальный босс дополнения «Завоеватели Атласа» и лидер других четырёх завоевателей Атласа."
        "Он известен как один из самых сложных боссов в игре из-за своего высокого урона, который включает физический, стихийный (огонь, холод, молния) и урон хаосом. "
    ),
}

@tool
def lookup(topic: str) -> str:
    """Краткое определение термина из базы знаний."""
    topic_lower = topic.strip().lower()
    for key, value in KNOWLEDGE_BASE.items():
        if key in topic_lower:
            print(f"[TOOL] lookup called with topic: {topic} and answer is {value}")
            return value
    print(f"[TOOL] lookup called with topic: {topic} and answer is No context")
    return (
        "No direct definition found in the knowledge base. "
        "Provide a general explanation using your own knowledge."
    )