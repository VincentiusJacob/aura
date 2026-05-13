from casper_bot.tools import get_tools
from casper_bot.tools.calendar import create_calendar_entry
from casper_bot.tools.search import search_web


def test_get_tools_returns_langchain_tools() -> None:
    tools = get_tools()

    assert [tool.name for tool in tools] == ["search_web", "create_calendar_entry"]


def test_search_web_returns_placeholder_message() -> None:
    result = search_web.invoke({"query": "weather in jakarta"})

    assert "not connected yet" in result
    assert "weather in jakarta" in result


def test_create_calendar_entry_returns_placeholder_message() -> None:
    result = create_calendar_entry.invoke({"request": "Dinner tomorrow at 7 pm"})

    assert "Calendar integration is not connected yet" in result
    assert "Dinner tomorrow at 7 pm" in result
