"""Main chat handler — catch-all for regular user messages."""

from aiogram import Router
from aiogram.types import Message

from casper_bot.bot.router import get_agent
from casper_bot.utils.logger import get_logger
from casper_bot.bot.keyboards.calendar import get_calendar_buttons
from casper_bot.bot.keyboards.notes import get_notes_buttons

logger = get_logger(__name__)
router = Router()


@router.message()
async def handle_chat(message: Message):
    user_id = message.from_user.id if message.from_user else None
    parsed_message = message.text or ""

    if not parsed_message.strip():
        return

    try:
        # Show "typing..." while the agent is working
        await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")

        response = await get_agent().arun(parsed_message, user_id=user_id)

        # Handle UI signal responses
        if "SHOW_CALENDAR_UI" in response:
            clean_text = response.replace("SHOW_CALENDAR_UI", "").strip()
            await message.answer(
                clean_text or "Here's your calendar! 📅",
                reply_markup=get_calendar_buttons(),
            )
            return

        if "SHOW_NOTES_UI" in response:
            clean_text = response.replace("SHOW_NOTES_UI", "").strip()
            await message.answer(
                clean_text or "Here are your notes! 📝",
                reply_markup=get_notes_buttons(),
            )
            return

        await message.answer(text=response)

    except Exception as exc:
        logger.exception("Error in handle_chat: %s", exc)
        await message.answer(
            text="Sorry, something went wrong. Please try again."
        )
