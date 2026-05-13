"""User context middleware — injects user metadata into every handler."""

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class UserContextMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data: dict):
        user = data.get("event_from_user")

        if user:
            # These keys become available as handler function parameters
            data["user_id"] = user.id
            data["username"] = user.username or user.first_name or "Unknown"
            data["language"] = user.language_code or "en"

        return await handler(event, data)
