"""Judge node — evaluates progress and decides the next routing step."""

from __future__ import annotations

import json

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.language_models import BaseChatModel

from .state import AgentState
from .prompts import JUDGE_SYSTEM


# Valid decisions the judge can emit
COMPLETE = "COMPLETE"
CONTINUE = "CONTINUE"
REPLAN   = "REPLAN"


class JudgeAgent:
    """
    LangGraph node that evaluates `past_steps` and routes accordingly.

    Returns a partial state update with:
      - `final_response` (only when decision == COMPLETE)
    
    The actual routing is done by the `judge_router` function below,
    which reads the decision stored in the state by this node.
    """

    def __init__(self, llm: BaseChatModel) -> None:
        self.llm = llm

    # ------------------------------------------------------------------
    # Node callable
    # ------------------------------------------------------------------
    def __call__(self, state: AgentState) -> dict:
        past_steps = state.get("past_steps", [])
        plan = state.get("plan", [])

        # Build a readable summary of what has been done
        steps_summary = "\n".join(
            f"  Step {i + 1}: {step}\n  Result: {result}"
            for i, (step, result) in enumerate(past_steps)
        )
        remaining = "\n".join(f"  - {s}" for s in plan) or "  (none)"

        judge_prompt = (
            f"Executed steps so far:\n{steps_summary}\n\n"
            f"Remaining plan steps:\n{remaining}\n\n"
            "If no steps remain ('none'), you must choose either COMPLETE (if the request is finished) "
            "or REPLAN (if you need more steps to finish it). Do not choose CONTINUE if the plan is empty.\n\n"
            "Based on the original user request, what is your decision?"
        )

        system_msg = SystemMessage(content=JUDGE_SYSTEM)
        judge_msg = HumanMessage(content=judge_prompt)
        messages = [system_msg] + state["messages"] + [judge_msg]

        response = self.llm.invoke(messages)
        parsed = self._parse_response(response.content)

        decision = parsed.get("decision", CONTINUE).upper()
        final_response = parsed.get("final_response", "")

        # Store both so the router function (below) can read them
        update: dict = {"judge_decision": decision}
        if decision == COMPLETE and final_response:
            update["final_response"] = final_response

        return update

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _parse_response(raw: str) -> dict:
        """Safely parse the JSON decision block from the LLM."""
        # Find the first '{' and last '}' to extract only the JSON part
        start = raw.find("{")
        end = raw.rfind("}")
        
        if start != -1 and end != -1:
            json_str = raw[start : end + 1]
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass

        # Fallback if no valid JSON found
        return {"decision": CONTINUE, "final_response": ""}


# ---------------------------------------------------------------------------
# Router — used as the conditional edge out of the Judge node
# ---------------------------------------------------------------------------

def judge_router(state: AgentState) -> str:
    """
    Reads the Judge's decision from the state and returns the next node name.
    """
    decision = state.get("judge_decision", CONTINUE).upper()
    plan = state.get("plan", [])

    if decision == COMPLETE:
        return "end"
    
    if decision == REPLAN:
        return "planner"
    
    # If CONTINUE but nothing left in plan, we must replan
    if decision == CONTINUE and not plan:
        return "planner"
        
    return "executor"
