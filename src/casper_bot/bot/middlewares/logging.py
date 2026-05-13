"""Logging middleware — logs every incoming update with timing."""

import logging
import time

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data: dict):
        # BEFORE the handler
        start_time = time.time()
        user = data.get("event_from_user")
        user_info = f"user_id={user.id}" if user else "unknown_user"

        logger.info(f"[IN]  {event.__class__.__name__} from {user_info}")

        # Call the actual handler
        result = await handler(event, data)

        # AFTER the handler
        duration = time.time() - start_time
        logger.info(f"[OUT] {event.__class__.__name__} handled in {duration:.3f}s")

        return result
