"""Executor node — carries out one plan step at a time using bound tools."""

from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.language_models import BaseChatModel

from .state import AgentState
from .prompts import EXECUTOR_SYSTEM


class ExecutorAgent:
    """
    LangGraph node that executes the *next* step in the plan.

    The LLM is bound to the available tools so it can call them freely.
    After the step completes (tool call + observation), the result is
    appended to `past_steps` and the step is removed from `plan`.
    """

    def __init__(self, llm: BaseChatModel, tools: list) -> None:
        """
        Parameters
        ----------
        llm:
            A ChatModel that supports tool-calling (e.g. ChatOpenAI,
            ChatGoogleGenerativeAI, ChatAnthropic).
        tools:
            List of LangChain-compatible tool objects (decorated with
            @tool or wrapped with StructuredTool).
        """
        
        self.llm_with_tools = llm.bind_tools(tools) if tools else llm
        self.tools_by_name: dict = {t.name: t for t in tools}

    # ------------------------------------------------------------------
    # Node callable
    # ------------------------------------------------------------------
    def __call__(self, state: AgentState) -> dict:
        plan = list(state.get("plan", []))

        if not plan:
            # Nothing left to execute — let the Judge decide what to do
            return {}

        # Pop the very first step
        current_step = plan.pop(0)

        # Ask the LLM (with tools) to carry out this step
        system_msg = SystemMessage(content=EXECUTOR_SYSTEM)
        step_msg = HumanMessage(content=f"Execute this step: {current_step}")
        messages = [system_msg] + state["messages"] + [step_msg]

        response = self.llm_with_tools.invoke(messages)
        print(f"LLM Response: {response}")

        # If the model issued a tool call, run it and collect the result
        outcome = self._run_tool_calls(response)

        # Update state: remove the executed step, log the outcome
        past_steps = list(state.get("past_steps", []))
        past_steps.append((current_step, outcome))

        return {
            "plan": plan,
            "past_steps": past_steps,
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _run_tool_calls(self, response) -> str:
        """
        If the LLM's response contains tool_calls, invoke them and return
        a concatenated string of all results.  Otherwise return the
        text content directly.
        """

        tool_calls = getattr(response, "tool_calls", None)
        if not tool_calls:
            return response.content or "(no output)"

        results = []
        for call in tool_calls:
            tool_name = call["name"]
            tool_args = call["args"]
            tool = self.tools_by_name.get(tool_name)

            if tool is None:
                results.append(f"[Tool '{tool_name}' not found]")
                continue

            print(f"Invoking tool: {tool_name} with args: {tool_args}")
            result = tool.invoke(tool_args)

            print(f"Tool Invokation result: {result}")
            results.append(str(result))

        return "\n".join(results)
