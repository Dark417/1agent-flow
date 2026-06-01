"""Pattern 07 — Autonomous Agent (Google ADK).

One LlmAgent, an open-ended goal, and a toolbox. The model runs its own
reason -> act -> observe loop: it must discover the distance and fuel price via
tools, then compute the cost — deciding the order of steps itself. Nothing in
this file scripts that sequence.

Design doc: docs/design/07-autonomous-agent.md
"""

import ast
import operator
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shared.config import MODEL, require_api_key, run  # noqa: E402

from google.adk.agents import LlmAgent  # noqa: E402

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
def get_distance_km(origin: str, destination: str) -> dict:
    """Return the one-way driving distance in km between two cities (demo data)."""
    table = {("berlin", "munich"): 585, ("paris", "lyon"): 465,
             ("madrid", "barcelona"): 620}
    key = (origin.strip().lower(), destination.strip().lower())
    dist = table.get(key) or table.get((key[1], key[0]))
    if dist is None:
        return {"error": f"No route data for {origin}->{destination}."}
    return {"distance_km": dist}


def get_fuel_price(country: str) -> dict:
    """Return the fuel price per liter (EUR) for a country (demo data)."""
    prices = {"germany": 1.75, "france": 1.85, "spain": 1.55}
    price = prices.get(country.strip().lower())
    if price is None:
        return {"error": f"No fuel price for {country}."}
    return {"eur_per_liter": price}


def calculate(expression: str) -> dict:
    """Evaluate a basic arithmetic expression, e.g. '585 * 2 * 0.07 * 1.75'."""
    try:
        return {"result": _eval(ast.parse(expression, mode="eval").body)}
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}


# --- Agent: open-ended goal, no scripted steps -----------------------------
root_agent = LlmAgent(
    name="trip_planner",
    model=MODEL,
    description="Figures out trip fuel costs by gathering data with tools.",
    instruction=(
        "You are an autonomous trip-cost agent. Use the available tools to find "
        "whatever you need (distances, fuel prices), then compute the answer "
        "with the `calculate` tool. Always do arithmetic via the tool. Decide "
        "the steps yourself. When done, state the total clearly and show your "
        "working."
    ),
    tools=[get_distance_km, get_fuel_price, calculate],
)


if __name__ == "__main__":
    require_api_key()
    goal = (
        "I'm driving round-trip from Berlin to Munich in Germany. My car uses "
        "7 liters per 100 km. How much will fuel cost in EUR?"
    )
    print("Goal:", goal)
    print("\n--- Agent answer ---\n")
    print(run(root_agent, goal))
