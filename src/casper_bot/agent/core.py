"""
Core agent orchestration — assembles the LangGraph Plan-Execute-Judge graph.

Usage
-----
    from casper_bot.agent.core import build_agent
    from langchain_openai import ChatOpenAI         

    agent = build_agent(llm=ChatOpenAI(model="gpt-4o"), tools=[...])
    result = agent.invoke({"messages": [HumanMessage(content="What's the BTC price?")]})
    print(result["final_response"])
"""

from __future__ import annotations

from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
from langgraph.graph import END, StateGraph

from .executor import ExecutorAgent
from .judge import JudgeAgent, judge_router
from .memory import ConversationMemory
from .planner import PlannerAgent
from .state import AgentState


def build_agent(llm: BaseChatModel, tools: list[Any] | None = None):
    """
    Construct and compile the Plan-Execute-Judge LangGraph agent.

    Parameters
    ----------
    llm:
        Any LangChain-compatible chat model.  Must support tool-calling if
        you want the Executor to use `tools`.
    tools:
        LangChain tool objects available to the Executor node.

    Returns
    -------
    CompiledGraph
        A compiled LangGraph graph you can call with `.invoke()` or
        `.astream()`.

    Graph topology
    --------------

        ┌─────────┐
        │  START  │
        └────┬────┘
             │
        ┌────▼────┐
        │ Planner │ ◄──────────────────┐
        └────┬────┘                    │ REPLAN
             │                        │
        ┌────▼─────┐           ┌───────┴──────┐
        │ Executor │ ◄──────── │    Judge     │
        └────┬─────┘  CONTINUE └──────┬───────┘
             │                        │ COMPLETE
             └────────────────────────┘
                                       │
                                   ┌───▼───┐
                                   │  END  │
                                   └───────┘
    """

    tools = tools or []

    # Build a human-readable list of tool names + descriptions for the Planner
    tool_descriptions = "\n".join(
        f"  - {t.name}: {t.description}" for t in tools
    ) if tools else "(no tools available)"

    # ------------------------------------------------------------------ nodes

    planner  = PlannerAgent(llm=llm, tool_descriptions=tool_descriptions)
    executor = ExecutorAgent(llm=llm, tools=tools)
    judge    = JudgeAgent(llm=llm)

    # ------------------------------------------------------------------ graph
    
    graph = StateGraph(AgentState)

    graph.add_node("planner",  planner)
    graph.add_node("executor", executor)
    graph.add_node("judge",    judge)

    # ------------------------------------------------------------------ edges
    graph.set_entry_point("planner")

    graph.add_edge("planner",  "executor")
    graph.add_edge("executor", "judge")

    graph.add_conditional_edges(
        "judge",
        judge_router,
        {
            "executor": "executor",
            "planner":  "planner",
            "end":      END,
        },
    )

    return graph.compile()


# ---------------------------------------------------------------------------
# Convenience wrapper — thin async interface for the Telegram handler
# ---------------------------------------------------------------------------

class Agent:
    """
    High-level wrapper around the compiled graph.

    Example
    -------
        agent = Agent(llm=..., tools=[...])
        reply = await agent.arun("What is the weather in Bali?")
    """

    def __init__(self, llm: BaseChatModel, tools: list[Any] | None = None) -> None:
        self._graph = build_agent(llm=llm, tools=tools)
        
        # short-term memory
        self._memory = ConversationMemory(max_messages=20)

    def _initial_state(self, messages: list[AnyMessage]) -> AgentState:
        """Build a clean initial state dict."""
        return {
            "messages":       messages,
            "plan":           [],
            "past_steps":     [],
            "final_response": "",
            "judge_decision": "",
        }

    def run(
        self,
        user_message: str,
        user_id: int | None = None,
        history: list[AnyMessage] | None = None,
    ) -> str:
        """Synchronous invocation — returns the final response string."""

        messages = self._build_messages(user_message, user_id, history)
        human_msg = messages[-1]  # the HumanMessage we just appended

        result = self._graph.invoke(
            self._initial_state(messages),
            {"recursion_limit": 50},
        )
        response = result.get("final_response", "(no response generated)")

        # Persist the exchange in memory
        if user_id is not None:
            from langchain_core.messages import AIMessage
            self._memory.append(user_id, human_msg)
            self._memory.append(user_id, AIMessage(content=response))

        return response

    async def arun(
        self,
        user_message: str,
        user_id: int | None = None,
        history: list[AnyMessage] | None = None,
    ) -> str:
        """Asynchronous invocation — use this inside async Telegram handlers."""

        messages = self._build_messages(user_message, user_id, history)
        human_msg = messages[-1]

        result = await self._graph.ainvoke(
            self._initial_state(messages),
            {"recursion_limit": 50},
        )
        response = result.get("final_response", "(no response generated)")

        if user_id is not None:
            self._memory.append(user_id, human_msg)
            self._memory.append(user_id, AIMessage(content=response))

        return response

    def _build_messages(
        self,
        user_message: str,
        user_id: int | None,
        history: list[AnyMessage] | None,
    ) -> list[AnyMessage]:
        """Merge stored memory + explicit history + new user message."""

        messages: list[AnyMessage] = []
        if user_id is not None:
            messages.extend(self._memory.get(user_id))
        if history:
            messages.extend(history)
        messages.append(HumanMessage(content=user_message))
        return messages
