"""Database models."""

from dataclasses import dataclass


@dataclass(slots=True)
class Message:
    user_id: int
    content: str


@dataclass(slots=True)
class Event:
    user_id: int
    title: str
    date: str
    description: str | None = None
