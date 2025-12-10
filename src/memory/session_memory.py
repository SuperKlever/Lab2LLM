from __future__ import annotations

from typing import Iterable, Optional

from src.graph.state import ConversationState, default_state

class SessionMemory:
    """Lightweight session memory built on top of the typed graph state."""

    def __init__(self, initial: Optional[ConversationState] = None) -> None:
        self._state: ConversationState = initial or default_state()

    @property
    def state(self) -> ConversationState:
        return self._state

    def load(self) -> ConversationState:
        """Return a shallow copy of the current state."""

        return ConversationState(**self._state)

    def update(self, **kwargs: object) -> ConversationState:
        """Merge incoming fields into state and return updated copy."""

        self._state.update(kwargs)  # type: ignore[arg-type]
        return self.load()

    def add_history(self, items: Iterable[str]) -> ConversationState:
        """Append entries to history."""

        history = list(self._state.get("history", []))
        history.extend(items)
        self._state["history"] = history
        return self.load()