"""Callback-query handlers for quick Telegram actions."""

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from casper_bot.bot.router import get_agent

router = Router()

class CreateEventState(StatesGroup):
    collecting = State()


@router.callback_query(F.data == "create_event")
async def handle_create_event(callback_query: CallbackQuery, state: FSMContext) -> None:
    await callback_query.answer("Starting event creation...")
    await state.set_state(CreateEventState.collecting)
    await callback_query.message.answer(
        "Describe the event you want to create. "
        "You can include title, date, time, location, and description."
    )


@router.callback_query(F.data.in_({"todays_event", "weekly_event", "monthly_event", "find_event"}))
async def handle_calendar_placeholder(callback_query: CallbackQuery) -> None:
    await callback_query.answer()
    await callback_query.message.answer(
        "That calendar action is scaffolded but not connected to storage yet."
    )


@router.callback_query(F.data == "cancel")
async def handle_cancel(callback_query: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback_query.answer("Cancelled")
    await callback_query.message.answer("Cancelled the current action.")


@router.message(CreateEventState.collecting)
async def handle_agent_collection(message: Message, state: FSMContext) -> None:
    response = await get_agent().arun(message.text or "")
    await message.answer(response)
    await state.clear()
