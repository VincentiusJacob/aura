"""Database access helpers."""

from casper_bot.db.models import Message, Event


class MessageRepository:
    def __init__(self) -> None:
        self._messages: list[Message] = []

    def save_message(self, message: Message) -> Message:
        self._messages.append(message)
        return message


class EventRepository:
    def __init__(self) -> None:
        self._events: list[Event] = []

    def save_event(self, event: Event) -> Event:
        self._events.append(event)
        return event
