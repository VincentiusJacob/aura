from casper_bot.agent.planner import PlannerAgent


def test_parse_plan_handles_numbered_and_bulleted_steps() -> None:
    raw_plan = """
    1. Search the web for the current weather.
    2) Summarize the forecast.
    - Ask whether the user wants a reminder.
    """

    assert PlannerAgent._parse_plan(raw_plan) == [
        "Search the web for the current weather.",
        "Summarize the forecast.",
        "Ask whether the user wants a reminder.",
    ]
