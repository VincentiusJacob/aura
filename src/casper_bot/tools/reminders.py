"""Reminder tool — stores and retrieves user reminders in memory."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime

from langchain_core.tools import tool

# Simple in-memory store keyed by user (global singleton for now)
_reminders: dict[str, list[dict]] = defaultdict(list)


@tool
def set_reminder(reminder: str) -> str:
    """Set a reminder for the user. They will be able to view it later.
    Use this when the user says things like 'remind me to...' or 'don't let me forget...'."""
    _reminders["default"].append(
        {
            "text": reminder,
            "created_at": datetime.now().isoformat(),
            "done": False,
        }
    )
    return f"✅ Reminder set: {reminder}"


@tool
def get_reminders() -> str:
    """Get all active reminders for the user.
    Use this when the user asks 'what are my reminders?' or 'show reminders'."""
    items = [r for r in _reminders["default"] if not r["done"]]
    if not items:
        return "You have no active reminders."

    lines = []
    for i, r in enumerate(items, 1):
        lines.append(f"{i}. {r['text']}  (set: {r['created_at'][:16]})")
    return "\n".join(lines)


@tool
def complete_reminder(reminder_number: int) -> str:
    """Mark a reminder as done by its number (1-based).
    Use this when the user says 'done with reminder 1' or 'complete reminder 2'."""
    items = [r for r in _reminders["default"] if not r["done"]]
    if not items:
        return "You have no active reminders to complete."
    if reminder_number < 1 or reminder_number > len(items):
        return f"Invalid reminder number. You have {len(items)} active reminder(s)."

    items[reminder_number - 1]["done"] = True
    return f"✅ Marked reminder #{reminder_number} as done."
