"""Application entry point."""

import asyncio
import logging

from aiogram import Dispatcher

from casper_bot.bot.handlers import actions, chat, start
from casper_bot.bot.middlewares import LoggingMiddleware, UserContextMiddleware, RateLimitMiddleware
from casper_bot.bot.router import get_bot
from casper_bot.config import settings


async def main():
    logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
    bot = get_bot()

    dp = Dispatcher()

    # Register middleware (runs on every update)
    dp.message.middleware(LoggingMiddleware())
    dp.callback_query.middleware(LoggingMiddleware())

    dp.message.middleware(UserContextMiddleware())
    dp.callback_query.middleware(UserContextMiddleware())

    dp.message.middleware(RateLimitMiddleware(limit=10, window=60))

    # Register routers — most specific first, catch-all last
    dp.include_router(start.router)
    dp.include_router(actions.router)
    dp.include_router(chat.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
