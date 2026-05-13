from casper_bot.bot.keyboards.calendar import get_calendar_buttons
from casper_bot.bot.keyboards.notes import get_notes_buttons


def test_calendar_buttons_layout_is_valid() -> None:
    keyboard = get_calendar_buttons()

    assert len(keyboard.inline_keyboard) == 3
    assert sum(len(row) for row in keyboard.inline_keyboard) == 6


def test_notes_buttons_layout_is_valid() -> None:
    keyboard = get_notes_buttons()

    assert len(keyboard.inline_keyboard) == 3
    assert sum(len(row) for row in keyboard.inline_keyboard) == 5
