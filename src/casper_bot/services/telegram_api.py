"""Telegram API wrapper."""


class TelegramAPI:
    def send_message(self, chat_id: int, text: str) -> dict[str, object]:
        return {"chat_id": chat_id, "text": text}
