# Amazon Strands Agents implementations

The same patterns from [`docs/design/`](../../docs/design/) implemented with
Amazon's [Strands Agents](https://strandsagents.com/) SDK, running Claude models
on **Amazon Bedrock**.

| # | Pattern | Strands approach |
| --- | --- | --- |
| 01 | [Tool Use](01-tool-use/) | `Agent(tools=[...])` with `@tool` functions |
| 02 | [Prompt Chaining](02-prompt-chaining/) | call agents in order in plain Python |
| 03 | [Routing](03-routing/) | a router `Agent` returns a label; Python dispatches |
| 04 | [Parallelization](04-parallelization/) | `ThreadPoolExecutor` fan-out + synthesizer |
| 05 | [Orchestrator–Workers](05-orchestrator-workers/) | agents-as-tools |
| 06 | [Evaluator–Optimizer](06-evaluator-optimizer/) | a capped Python `while` loop |
| 07 | [Autonomous Agent](07-autonomous-agent/) | one `Agent`, open-ended toolset |

Where Google's ADK offers first-class `SequentialAgent`/`ParallelAgent`/
`LoopAgent` constructs, Strands leans on plain Python for the control flow — so
these examples make the data flow and stopping conditions very explicit. (Strands
also ships higher-level `Swarm`, `GraphBuilder`, and workflow primitives; the
plain-Python versions here are chosen for clarity.)

## Setup

```bash
pip install -r ../../requirements-amazon.txt
cp ../../.env.example ../../.env   # then set your AWS credentials + region
```

You also need Bedrock **model access** enabled for the Claude model in your AWS
account/region.

## Run

```bash
python patterns/amazon-strands/02-prompt-chaining/agent.py
```

> All credentials are read from `.env`. The repo ships with **placeholders
> only** — set real AWS credentials (or a `AWS_BEARER_TOKEN_BEDROCK`) before
> running.
