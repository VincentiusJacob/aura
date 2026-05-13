from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_calendar_buttons():
    buttons = [
        InlineKeyboardButton(text="Create Event", callback_data="create_event"),
        InlineKeyboardButton(text="Today's Event", callback_data="todays_event"),
        InlineKeyboardButton(text="Cancel", callback_data="cancel"),
        InlineKeyboardButton(text="Weekly Event", callback_data="weekly_event"),
        InlineKeyboardButton(text="Monthly Event", callback_data="monthly_event"),
        InlineKeyboardButton(text="Find Event", callback_data="find_event"),
    ]

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [buttons[0], buttons[1]],
            [buttons[2], buttons[3]],
            [buttons[4], buttons[5]],
        ]
    )
