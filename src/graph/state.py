from typing import List, Literal, Optional, TypedDict


class ConversationState(TypedDict, total=False):
    question: str
    intent: Literal["explanation", "problem_solving", "unknown"]
    subject: Optional[str]
    level: Optional[str]
    history: List[str]
    answer: Optional[str]


def default_state() -> ConversationState:
    """Return an empty state with sensible defaults."""

    return ConversationState(
        question="",
        intent="unknown",
        subject=None,
        level=None,
        history=[],
        answer=None,
    )

class RouterAnswer(TypedDict, total=False):
    intent: Literal["explanation", "problem_solving", "unknown"]
    subject: str

class ExplanationAgentAnswer(TypedDict, total=False):
    answer_text: str

class ProblemSolvingAgentAnswer(TypedDict, total=False):
    answer_text: str