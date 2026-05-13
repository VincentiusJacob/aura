from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart


router = Router()

@router.message(CommandStart())
async def handle_start(message: Message):
    username = message.from_user.first_name

    await message.answer(
        f"Hello {username}!\n"
        "Tell me what you need",
    )
