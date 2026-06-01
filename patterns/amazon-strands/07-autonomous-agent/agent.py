"""Pattern 07 — Autonomous Agent (Amazon Strands).

One Strands Agent, an open-ended goal, and a toolbox. The agent runs its own
reason -> act -> observe loop: it must discover the distance and fuel price via
tools, then compute the cost — deciding the order of steps itself. Nothing here
scripts that sequence.

Design doc: docs/design/07-autonomous-agent.md
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
    raise ValueError("unsupported")


# --- Tools (the agent picks which to use, and in what order) ---------------
@tool
def get_distance_km(origin: str, destination: str) -> str:
    """Return the one-way driving distance in km between two cities (demo data)."""
    table = {("berlin", "munich"): 585, ("paris", "lyon"): 465,
             ("madrid", "barcelona"): 620}
    key = (origin.strip().lower(), destination.strip().lower())
    dist = table.get(key) or table.get((key[1], key[0]))
    return str(dist) if dist else f"error: no route data for {origin}->{destination}"


@tool
def get_fuel_price(country: str) -> str:
    """Return the fuel price per liter (EUR) for a country (demo data)."""
    prices = {"germany": 1.75, "france": 1.85, "spain": 1.55}
    price = prices.get(country.strip().lower())
    return str(price) if price else f"error: no fuel price for {country}"


@tool
def calculate(expression: str) -> str:
    """Evaluate a basic arithmetic expression, e.g. '585 * 2 * 0.07 * 1.75'."""
    try:
        return str(_eval(ast.parse(expression, mode="eval").body))
    except Exception as exc:  # noqa: BLE001
        return f"error: {exc}"


# --- Agent: open-ended goal, no scripted steps -----------------------------
agent = Agent(
    model=make_model(),
    tools=[get_distance_km, get_fuel_price, calculate],
    system_prompt=(
        "You are an autonomous trip-cost agent. Use the available tools to find "
        "whatever you need (distances, fuel prices), then compute the answer with "
        "the `calculate` tool. Always do arithmetic via the tool. Decide the "
        "steps yourself. When done, state the total clearly and show your working."
    ),
)


if __name__ == "__main__":
    require_credentials()
    goal = (
        "I'm driving round-trip from Berlin to Munich in Germany. My car uses "
        "7 liters per 100 km. How much will fuel cost in EUR?"
    )
    print("Goal:", goal)
    print("\n--- Agent answer ---\n")
    print(agent(goal))
