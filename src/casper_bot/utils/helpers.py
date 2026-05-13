"""General helper utilities."""

from typing import Any
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

from ..config import settings



def chunk_text(text: str, size: int) -> list[str]:
    if size <= 0:
        raise ValueError("size must be greater than zero")
    return [text[index : index + size] for index in range(0, len(text), size)]




def create_llm_instance(model: str, temperature: float = 0.3) -> BaseChatModel:

    llm = ChatOpenAI(
        model=model,
        api_key=settings.OPENAI_API_KEY,
        temperature=temperature,
    )
    return llm