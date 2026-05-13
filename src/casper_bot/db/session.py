"""Database session utilities."""

from dataclasses import dataclass


@dataclass(slots=True)
class DatabaseSession:
    url: str
