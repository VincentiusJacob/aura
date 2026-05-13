"""Agent tools — all tools available to the Casper agent."""

from casper_bot.tools.apps import create_calendar_entry, show_calendar_ui, show_notes_ui
from casper_bot.tools.search import search_web
from casper_bot.tools.utilities import get_current_datetime, calculate
from casper_bot.tools.reminders import set_reminder, get_reminders, complete_reminder
from casper_bot.tools.weather import get_weather


def get_tools() -> list:
    """Return all tools available to the agent."""
    return [
        # Search & info
        search_web,
        get_weather,
        get_current_datetime,
        calculate,
        # App UIs
        show_calendar_ui,
        show_notes_ui,
        # Calendar actions
        create_calendar_entry,
        # Reminders
        set_reminder,
        get_reminders,
        complete_reminder,
    ]


__all__ = [
    "search_web",
    "get_current_datetime",
    "calculate",
    "show_calendar_ui",
    "show_notes_ui",
    "create_calendar_entry",
    "set_reminder",
    "get_reminders",
    "complete_reminder",
    "get_tools",
]
