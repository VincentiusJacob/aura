"""
Shared state definition for the LangGraph agent.
All nodes read from and write to this TypedDict.
"""

from __future__ import annotations

from typing import Annotated, List, Tuple, TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """
    The single source of truth passed between every node in the graph.

    Fields
    ------
    messages:
        Full conversation history (human + AI). Uses LangGraph's built-in
        `add_messages` reducer so new messages are appended, never overwritten.
    plan:
        Ordered list of steps the Planner wants the Executor to carry out.
        The Executor pops steps from the front one at a time.
    past_steps:
        Accumulated log of (step_description, outcome) tuples produced by
        the Executor.  The Judge reads this to decide what to do next.
    final_response:
        The polished answer the Judge approved and that will be sent back
        to the Telegram user.  Empty string means the graph is still running.
    """

    messages: Annotated[List[AnyMessage], add_messages]
    plan: List[str]
    past_steps: List[Tuple[str, str]]
    final_response: str
    judge_decision: str
