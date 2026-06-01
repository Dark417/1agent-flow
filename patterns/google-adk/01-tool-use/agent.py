"""Pattern 01 — Augmented LLM / Tool Use (Google ADK).

A single LlmAgent given two tools. The model decides when to call each one.
This is the atom every other pattern is built from.

Design doc: docs/design/01-augmented-llm-tool-use.md
"""

import ast
import operator
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shared.config import MODEL, require_api_key, run  # noqa: E402

from google.adk.agents import LlmAgent  # noqa: E402


# --- Tools -----------------------------------------------------------------
# In ADK a "tool" is just a typed Python function with a clear docstring.
# The docstring is what the model reads to decide whether/how to call it.

_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.Pow: operator.pow, ast.USub: operator.neg,
}


def _safe_eval(node: ast.AST) -> float:
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.BinOp):
        return _OPS[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
    if isinstance(node, ast.UnaryOp):
        return _OPS[type(node.op)](_safe_eval(node.operand))
    raise ValueError("unsupported expression")


def calculate(expression: str) -> dict:
    """Evaluate a basic arithmetic expression.

    Args:
        expression: arithmetic using numbers and + - * / ** ( ),
            e.g. "12 * (3 + 4)".

    Returns:
        A dict with 'result' on success or 'error' describing the problem.
    """
    try:
        return {"result": _safe_eval(ast.parse(expression, mode="eval").body)}
    except Exception as exc:  # noqa: BLE001 - return a model-friendly error
        return {"error": f"Could not evaluate '{expression}': {exc}"}


def get_population(city: str) -> dict:
    """Look up the approximate population of a major city (demo data).

    Args:
        city: the city name, e.g. "Tokyo".

    Returns:
        A dict with 'population' or an 'error' if the city is unknown.
    """
    data = {
        "tokyo": 37_400_000, "delhi": 32_900_000, "shanghai": 29_200_000,
        "paris": 11_100_000, "london": 9_500_000, "new york": 18_800_000,
    }
    pop = data.get(city.strip().lower())
    if pop is None:
        return {"error": f"No population data for '{city}'. Known: {list(data)}"}
    return {"population": pop}


# --- Agent -----------------------------------------------------------------
root_agent = LlmAgent(
    name="tool_user",
    model=MODEL,
    description="Answers questions using a calculator and a city-population lookup.",
    instruction=(
        "You are a precise assistant. Use the `calculate` tool for ANY "
        "arithmetic — never do math in your head. Use the `get_population` "
        "tool for city populations. State which tool(s) you used and show the "
        "numbers."
    ),
    tools=[calculate, get_population],
)


if __name__ == "__main__":
    require_api_key()
    question = (
        "What is the combined population of Tokyo and Paris? "
        "Give me the exact sum."
    )
    print("Q:", question)
    print("A:", run(root_agent, question))
