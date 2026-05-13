"""Date, time, and utility tools."""

from datetime import datetime

from langchain_core.tools import tool


@tool
def get_current_datetime(timezone: str = "Asia/Jakarta") -> str:
    """Get the current date and time. Default timezone is Asia/Jakarta (WIB).
    Use this when the user asks what day/time it is or needs date-related info."""
    try:
        from zoneinfo import ZoneInfo

        tz = ZoneInfo(timezone)
    except (ImportError, KeyError):
        from zoneinfo import ZoneInfo

        tz = ZoneInfo("UTC")

    now = datetime.now(tz)
    return now.strftime("%A, %B %d, %Y at %I:%M %p %Z")


@tool
def calculate(expression: str) -> str:
    """Safely evaluate a mathematical expression and return the result.
    Examples: '2 + 2', '100 * 0.15', 'sqrt(144)'.
    Use this when the user asks for any calculation."""
    import ast
    import math

    # Provide common math functions in the evaluation namespace
    allowed_names = {
        "abs": abs,
        "round": round,
        "min": min,
        "max": max,
        "sum": sum,
        "pow": pow,
        "sqrt": math.sqrt,
        "log": math.log,
        "log10": math.log10,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "pi": math.pi,
        "e": math.e,
    }

    try:
        # Parse into AST and only allow expressions (not statements)
        tree = ast.parse(expression, mode="eval")

        # Walk the tree to ensure no dangerous nodes
        for node in ast.walk(tree):
            if isinstance(node, (ast.Call,)):
                # Only allow whitelisted function names
                if isinstance(node.func, ast.Name):
                    if node.func.id not in allowed_names:
                        return f"Function '{node.func.id}' is not allowed."
                else:
                    return "Only simple function calls are allowed."

        result = eval(compile(tree, "<calc>", "eval"), {"__builtins__": {}}, allowed_names)  # noqa: S307
        return str(result)
    except Exception as e:
        return f"Could not evaluate '{expression}': {e}"
