"""
Snippet 1 — Bot tool registry (read-only by construction)
==========================================================

This is the entire surface area of what the Telegram bot's Claude
can do. Anything not in this list does not exist for that agent.

Notice what is NOT here:
- No `create_*` or `update_*` or `delete_*` tools on business data
- No `run_sql` or `execute_query`
- No `write_to_file` or shell access
- The only "action" tool is `trigger_analysis`, which spawns an
  isolated subprocess. The bot does not see or write to that
  subprocess's output.
"""
from __future__ import annotations
from typing import Any
import asyncio

from your_app.db import read_only_queries as q
from your_app.charter import query_methodology
from your_app.orchestrator import runner

# ───────────────────────────────────────────────────────────
# 1. TOOL DEFINITIONS (Anthropic tool_use format)
# ───────────────────────────────────────────────────────────

TOOLS: list[dict[str, Any]] = [
    # ─── READ-ONLY TOOLS (13) ────────────────────────────
    {
        "name": "get_entity",
        "description": "Read a single entity's full record.",
        "input_schema": {
            "type": "object",
            "properties": {"id": {"type": "string"}},
            "required": ["id"],
        },
    },
    {
        "name": "get_score_details",
        "description": "Read the model parameters used to produce the current score.",
        "input_schema": {
            "type": "object",
            "properties": {"id": {"type": "string"}},
            "required": ["id"],
        },
    },
    {
        "name": "list_by_signal",
        "description": "List entities matching a given signal level.",
        "input_schema": {
            "type": "object",
            "properties": {"signal": {"type": "string"}},
            "required": ["signal"],
        },
    },
    {
        "name": "list_by_category",
        "description": "List entities in a given category, with their signals.",
        "input_schema": {
            "type": "object",
            "properties": {"category": {"type": "string"}},
            "required": ["category"],
        },
    },
    {
        "name": "get_watchlist",
        "description": "Return the current opportunity watchlist (read-only).",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "get_overview",
        "description": "High-level distribution of signals across the universe.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "get_known_issues",
        "description": "List methodological issues currently flagged.",
        "input_schema": {
            "type": "object",
            "properties": {"active_only": {"type": "boolean"}},
            "required": [],
        },
    },
    {
        "name": "get_red_flags",
        "description": "Entities with large gaps vs external consensus.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "get_methodology_decisions",
        "description": "Read currently active methodology rules.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "get_reclassifications",
        "description": "Historical record of category changes.",
        "input_schema": {
            "type": "object",
            "properties": {"id": {"type": "string"}},
            "required": [],
        },
    },
    {
        "name": "search_entities",
        "description": "Fuzzy search by name or identifier.",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    },
    {
        "name": "query_methodology_charter",
        "description": "Search the methodology document by topic/section.",
        "input_schema": {
            "type": "object",
            "properties": {
                "topic": {"type": "string"},
                "section": {"type": "string"},
                "limit": {"type": "integer"},
            },
            "required": [],
        },
    },
    {
        "name": "list_models_in_use",
        "description": "Read-only view of which Claude model each agent uses.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },

    # ─── ACTION TOOLS (2) — NOT direct writes ─────────────
    {
        "name": "configure_model",
        "description": (
            "Admin: change which Claude model an agent uses. Writes only to "
            "the model-config table, not to business data."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "agent": {"type": "string"},
                "model": {"type": "string"},
            },
            "required": ["agent", "model"],
        },
    },
    {
        "name": "trigger_analysis",
        "description": (
            "Spawn an isolated analysis subprocess for one entity. "
            "Returns immediately with an acknowledgement. "
            "The result arrives separately as a Telegram message. "
            "The bot does not see or write the result — that's the "
            "pipeline's job, with its own validation gate."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string"},
                "depth": {"type": "string", "enum": ["shallow", "full"]},
            },
            "required": ["id"],
        },
    },
]

# ───────────────────────────────────────────────────────────
# 2. DISPATCHER — each tool maps to a small handler
# ───────────────────────────────────────────────────────────

_HANDLERS = {
    "get_entity":                lambda i, ctx=None: q.get_entity(i["id"]),
    "get_score_details":         lambda i, ctx=None: q.get_score_details(i["id"]),
    "list_by_signal":            lambda i, ctx=None: q.list_by_signal(i["signal"]),
    "list_by_category":          lambda i, ctx=None: q.list_by_category(i["category"]),
    "get_watchlist":             lambda i, ctx=None: q.get_watchlist(),
    "get_overview":              lambda i, ctx=None: q.get_overview(),
    "get_known_issues":          lambda i, ctx=None: q.get_known_issues(i.get("active_only", True)),
    "get_red_flags":             lambda i, ctx=None: q.get_red_flags(),
    "get_methodology_decisions": lambda i, ctx=None: q.get_methodology_decisions(),
    "get_reclassifications":     lambda i, ctx=None: q.get_reclassifications(i.get("id")),
    "search_entities":           lambda i, ctx=None: q.search_entities(i["query"]),
    "query_methodology_charter": lambda i, ctx=None: query_methodology(**i),
    "list_models_in_use":        lambda i, ctx=None: q.list_models_in_use(),
    "configure_model":           lambda i, ctx=None: _configure(i),
    "trigger_analysis":          lambda i, ctx=None: _trigger(i, ctx),
}


def _configure(tool_input: dict) -> dict:
    """Admin tool: changes model config, not business data."""
    return q.update_model_config(tool_input["agent"], tool_input["model"])


def _trigger(tool_input: dict, context: dict) -> dict:
    """
    Fire-and-forget. Schedules the analysis on the main event loop
    and returns immediately. The bot never sees the pipeline output.
    """
    if not context or "loop" not in context:
        return {"ok": False, "error": "trigger_analysis requires context"}

    coro = runner.run_analysis(
        entity_id=tool_input["id"],
        depth=tool_input.get("depth", "shallow"),
        chat_id=context["chat_id"],
    )
    asyncio.run_coroutine_threadsafe(coro, context["loop"])
    return {"ok": True, "eta_sec": 30 if tool_input.get("depth") == "full" else 3}


def execute_tool(name: str, tool_input: dict, context: dict = None) -> dict:
    """
    Single entry point. If the name isn't in _HANDLERS, the call is
    refused. There is no fallback to "try harder" — unknown tool is
    just unknown.
    """
    handler = _HANDLERS.get(name)
    if not handler:
        return {"error": f"Unknown tool: {name}"}
    try:
        result = handler(tool_input or {}, context)
        if not isinstance(result, dict):
            return {"error": f"Tool {name} returned {type(result).__name__}, expected dict"}
        return result
    except KeyError as e:
        return {"error": f"Missing required parameter: {e}"}
    except Exception as e:
        return {"error": f"Tool {name} failed: {type(e).__name__}: {e}"}


# Public set of allowed tool names — used by the bot's prompt template
# to render the system prompt that tells Claude what's available.
TOOL_NAMES = set(_HANDLERS.keys())
