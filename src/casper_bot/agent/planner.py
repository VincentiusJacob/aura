"""
Planner node — turns the user's request into an ordered list of steps.
"""

from __future__ import annotations

from langchain_core.messages import SystemMessage
from langchain_core.language_models import BaseChatModel

from .state import AgentState
from .prompts import PLANNER_SYSTEM, PLANNER_REPLAN_SUFFIX


class PlannerAgent:
    """
    LangGraph node that reads the conversation and emits a fresh plan.

    The node is called both at the START of the graph and when the Judge
    decides to REPLAN.  On a replan, it receives `past_steps` in the state
    and produces a revised plan for the remaining work.
    """

    def __init__(self, llm: BaseChatModel, tool_descriptions: str = "") -> None:
        self.llm = llm
        self.tool_descriptions = tool_descriptions

    # ------------------------------------------------------------------
    # Node callable — LangGraph calls this with the current state dict
    # ------------------------------------------------------------------
    def __call__(self, state: AgentState) -> dict:

        past_steps = state.get("past_steps", [])

        # Build the system prompt (add replan context when applicable)
        base_prompt = PLANNER_SYSTEM.format(
            tool_descriptions=self.tool_descriptions or "(no tools available)"
        )

        if past_steps:

            steps_summary = "\n".join(
                f"  Step: {step}\n  Result: {result}"
                for step, result in past_steps
            )

            system_content = base_prompt + PLANNER_REPLAN_SUFFIX.format(
                past_steps=steps_summary
            )
            
        else:
            system_content = base_prompt


        system_msg = SystemMessage(content=system_content)
        messages = [system_msg] + state["messages"]

        response = self.llm.invoke(messages)

        plan = self._parse_plan(response.content)

        return {"plan": plan}

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _parse_plan(raw: str) -> list[str]:
        """
        Convert the LLM's numbered-list output into a clean Python list.

        Handles both:
          "1. Do something"
          "1) Do something"
        and strips trailing whitespace / empty lines.

        """
    
        steps = []
        for line in raw.splitlines():
            line = line.strip()
            if not line:
                continue
            # Strip leading numbering like "1.", "1)", "- ", "* "
            for prefix_len in range(1, 5):
                if line[:prefix_len].rstrip(". )") .isdigit():
                    line = line[prefix_len:].lstrip(". )").strip()
                    break
            if line.startswith(("-", "*")):
                line = line[1:].strip()
            if line:
                steps.append(line)
        return steps