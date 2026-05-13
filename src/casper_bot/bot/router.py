from __future__ import annotations

from functools import lru_cache
from typing import Any

from aiogram import Bot

from casper_bot.agent import Agent
from casper_bot.config import settings
from casper_bot.tools import get_tools
from casper_bot.utils.helpers import create_llm_instance


@lru_cache(maxsize=1)
def build_llm() -> Any:
    settings.require("OPENAI_API_KEY")
    return create_llm_instance(model=settings.OPENAI_MODEL)


class TeleBot:
    def __init__(self, llm: Any | None = None, tools: list[Any] | None = None) -> None:
        settings.require("TELEGRAM_BOT_TOKEN")
        self.bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        self.llm = llm or build_llm()
        self.tools = tools or get_tools()
        self.agent = Agent(self.llm, self.tools)

    def get_bot(self) -> Bot:
        return self.bot

    def get_llm(self) -> Any:
        return self.llm

    def get_agent(self) -> Agent:
        return self.agent

    def get_tools(self) -> list[Any]:
        return self.tools


@lru_cache(maxsize=1)
def get_app() -> TeleBot:
    return TeleBot()


def get_bot() -> Bot:
    return get_app().get_bot()


def get_agent() -> Agent:
    return get_app().get_agent()


    
    
