"""Per-user conversation history storage."""

from __future__ import annotations

from collections import defaultdict

from langchain_core.messages import AnyMessage


class ConversationMemory:
    """
    In-memory sliding-window store for per-user LangChain messages.

    Keeps the most recent `max_messages` messages per user to provide
    conversational context without unbounded memory growth.
    """

    def __init__(self, max_messages: int = 20) -> None:
        
        self._store: dict[int, list[AnyMessage]] = defaultdict(list)
        self._max = max_messages

    def get(self, user_id: int) -> list[AnyMessage]:
        """Return the last N messages for a user."""

        return list(self._store[user_id][-self._max:])

    def append(self, user_id: int, message: AnyMessage) -> None:
        """Add a message and trim if necessary."""

        self._store[user_id].append(message)
        if len(self._store[user_id]) > self._max * 2:
            self._store[user_id] = self._store[user_id][-self._max:]

    def clear(self, user_id: int) -> None:
        """Wipe history for a specific user."""

        self._store.pop(user_id, None)
