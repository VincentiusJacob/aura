"""Calendar tool placeholder."""

from langchain_core.tools import tool

# ------------------------- calendar apps ---------------------------------

@tool
def create_calendar_entry(request: str) -> str:
    """Create a calendar entry from a natural-language request."""
    return (
        "Calendar integration is not connected yet. "
        f"Draft event request saved: {request}"
    )

@tool
def show_calendar_ui() -> str:
    """Call this tool when the user wants to set up a plan, see calendar options, view their schedule, or manage their events."""
    return "SHOW_CALENDAR_UI"

# ------------------------- notes apps ---------------------------------

@tool
def show_notes_ui() -> str:
    """Call this tool when the user wants to create a new note, update a note, delete a note, records some information"""
    return "SHOW_NOTES_UI"