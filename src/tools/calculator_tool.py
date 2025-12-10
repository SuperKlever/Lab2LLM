import math
from typing import Any

from langchain_core.tools import tool

@tool
def calculator(expression: str) -> Any:
    """Evaluate a math expression safely using Python's eval with limited scope."""
    allowed_names = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
    allowed_names["abs"] = abs
    code = compile(expression, "<expression>", "eval")
    for name in code.co_names:
        if name not in allowed_names:
            raise ValueError(f"Use of '{name}' is not allowed.")
    answer = eval(code, {"__builtins__": {}}, allowed_names)
    print(f"[TOOL] calculator called with expression: {expression} and answer is {answer}")
    return answer