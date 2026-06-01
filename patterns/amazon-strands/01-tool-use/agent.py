"""Pattern 01 — Augmented LLM / Tool Use (Amazon Strands).

A single Strands Agent given two @tool functions. The model decides when to call
each one. This is the atom every other pattern is built from.

Design doc: docs/design/01-augmented-llm-tool-use.md
"""

import ast
import operator
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shared.config import make_model, require_credentials  # noqa: E402

from strands import Agent, tool  # noqa: E402

_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
        ast.Div: operator.truediv, ast.Pow: operator.pow, ast.USub: operator.neg}


def _eval(node):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.BinOp):
        return _OPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp):
        return _OPS[type(node.op)](_eval(node.operand))
    raise ValueError("unsupported expression")


# --- Tools -----------------------------------------------------------------
# In Strands a tool is a function decorated with @tool; the docstring and type
# hints are what the model reads to decide whether/how to call it.

@tool
def calculate(expression: str) -> str:
    """Evaluate a basic arithmetic expression like '12 * (3 + 4)'.

    Use this for ANY arithmetic instead of computing in your head.
    """
    try:
        return str(_eval(ast.parse(expression, mode="eval").body))
    except Exception as exc:  # noqa: BLE001 - return a model-friendly error
        return f"error: could not evaluate '{expression}': {exc}"


@tool
def get_population(city: str) -> str:
    """Return the approximate population of a major city (demo data)."""
    data = {
        "tokyo": 37_400_000, "delhi": 32_900_000, "shanghai": 29_200_000,
        "paris": 11_100_000, "london": 9_500_000, "new york": 18_800_000,
    }
    pop = data.get(city.strip().lower())
    if pop is None:
        return f"error: no population data for '{city}'. Known: {list(data)}"
    return str(pop)


# --- Agent -----------------------------------------------------------------
agent = Agent(
    model=make_model(),
    system_prompt=(
        "You are a precise assistant. Use the `calculate` tool for ANY "
        "arithmetic — never do math in your head. Use `get_population` for city "
        "populations. State which tool(s) you used and show the numbers."
    ),
    tools=[calculate, get_population],
)


if __name__ == "__main__":
    require_credentials()
    question = (
        "What is the combined population of Tokyo and Paris? Give the exact sum."
    )
    print("Q:", question)
    print("A:", agent(question))
