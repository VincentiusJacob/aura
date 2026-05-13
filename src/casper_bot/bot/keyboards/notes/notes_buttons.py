from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_notes_buttons():
    buttons = [
        InlineKeyboardButton(text="Create New Note", callback_data="create_note"),
        InlineKeyboardButton(text="Update Note", callback_data="update_note"),
        InlineKeyboardButton(text="Find Note", callback_data="find_note"),
        InlineKeyboardButton(text="Delete Note", callback_data="delete_note"),
        InlineKeyboardButton(text="View All Notes", callback_data="view_all_note"),
    ]

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [buttons[0], buttons[1]],
            [buttons[2], buttons[3]],
            [buttons[4]],
        ]
    )
