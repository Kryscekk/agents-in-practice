> 🇫🇷 **Lire en français** : [README.fr.md](README.fr.md)

# 18 — Triple defense in depth for production AI agents

**Difficulty**: 🔴 Advanced  |  **Estimated time**: 90 min

---

## What you'll learn

Three architectural layers that sit between a Claude API call and a production database, applied to non-coding-agent contexts (financial reasoning, medical workflows, advisory systems):

1. **Horizontal isolation** — multiple Claude instances with different scopes; the conversational agent has no write tools at all.
2. **Vertical ordering** — blocking state machine; methods refuse to run out of order, Python crashes instead of executing on bad state.
3. **Longitudinal traceability** — every Claude call and every final decision stored with cross-checks. Audit-ready months later, in the same SQLite file as the business data.

This is the pattern that would have prevented the PocketOS incident (April 2026, AI agent deleted entire production database in 9 seconds via a single GraphQL mutation).

## Companion article

**Long-form article on Dev.to** (recommended reading first):
*"AI agent governance: how I built triple defense in depth for production AI agents"* — https://gist.github.com/Kryscekk/efb334ed334f7ee15e84cd307225bd1c

The article covers the full reasoning, the PocketOS incident analysis, and honest comparison with Langfuse, pytransitions, and Claude Code subagents.

## Reproducible snippets

Three Python snippets you can copy into your own project:

- **[`01_tool_registry.py`](snippets/01_tool_registry.py)** — Tool registry pattern. 13 read-only tools, 2 admin tools, 1 fire-and-forget trigger. **No write tools exist in the dispatcher.**
- **[`02_state_machine.py`](snippets/02_state_machine.py)** — 12-state blocking state machine with `_advance_state` (5 lines) and crash-resume helpers.
- **[`03_provenance.py`](snippets/03_provenance.py)** — SQLite schemas for `claude_calls` and `fv_reasoning`. Insertion pattern, query examples.

## Architecture diagram

![Architecture](architecture.svg)

## What we'll build

A minimal version of the three-layer pattern using:
- One Anthropic API key (you can use the same key for clarity; in production you'd separate)
- SQLite as the only persistence layer (no external service required)
- Pure Python validators between Claude JSON output and database writes

## Prerequisites

- Python 3.10+
- An Anthropic API key
- Familiarity with `tool_use` (covered in tutorials 5-7)
- Optional but recommended: read tutorials 8-12 first

## Status

🚧 **Tutorial being written.** The companion article and reproducible snippets are already available. The hands-on tutorial walkthrough will follow.

**Star the repo** ([⭐ Star](https://github.com/Kryscekk/agents-in-practice)) to be notified when the full tutorial is released.
