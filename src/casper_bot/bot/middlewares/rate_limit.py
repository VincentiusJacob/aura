"""Rate limit middleware — prevents users from spamming the bot."""

import time
from collections import defaultdict
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message


class RateLimitMiddleware(BaseMiddleware):
    """
    Middleware to limit the number of requests a user can make per minute.
    """

    def __init__(self, limit: int = 20, window: int = 60):
        self.limit = limit
        self.window = window
        self.users: Dict[int, list[float]] = defaultdict(list)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if not isinstance(event, Message):
            return await handler(event, data)

        user_id = event.from_user.id if event.from_user else None
        if not user_id:
            return await handler(event, data)

        now = time.time()
        # Clean up old timestamps
        self.users[user_id] = [t for t in self.users[user_id] if now - t < self.window]

        if len(self.users[user_id]) >= self.limit:
            return await event.answer("Whoa there! You're sending messages too fast. Please slow down a bit.")

        self.users[user_id].append(now)
        return await handler(event, data)
