"""
Snippet 3 — Provenance trail for every Claude call
====================================================

Two tables in SQLite:
 - claude_calls   : one row per API call. Cost, tokens, retry attempt,
                    error message. Whether the call succeeded or failed.
 - decisions      : one row per business decision. Narrative reasoning,
                    cross-checks against alternative methods, sources.

Together they answer: "Six months later, why did the system say X?"

Every Claude call goes through `log_call()`. The wrapper around the
Anthropic SDK calls this at the end, in a finally block — success
and failure both produce a row.
"""
from __future__ import annotations
import sqlite3
import json
from typing import Optional, Dict, List
from datetime import datetime, timezone


# ───────────────────────────────────────────────────────────
# SCHEMA
# ───────────────────────────────────────────────────────────

SCHEMA = """
CREATE TABLE IF NOT EXISTS claude_calls (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    ts              TEXT NOT NULL DEFAULT (datetime('now')),
    agent_name      TEXT NOT NULL,    -- 'classifier', 'estimator', 'valuator', 'validator'
    entity_id       TEXT,
    trace_id        TEXT,             -- groups retries of the same logical call
    batch_id        TEXT,             -- groups all calls of one full analysis
    model           TEXT NOT NULL,
    input_tokens    INTEGER DEFAULT 0,
    output_tokens   INTEGER DEFAULT 0,
    cache_read      INTEGER DEFAULT 0,
    cache_write     INTEGER DEFAULT 0,
    duration_ms     INTEGER DEFAULT 0,
    cost_usd        REAL    DEFAULT 0.0,
    stop_reason     TEXT,
    attempt         INTEGER DEFAULT 1,
    error_message   TEXT
);

CREATE INDEX IF NOT EXISTS idx_claude_calls_entity   ON claude_calls(entity_id);
CREATE INDEX IF NOT EXISTS idx_claude_calls_trace    ON claude_calls(trace_id);
CREATE INDEX IF NOT EXISTS idx_claude_calls_batch    ON claude_calls(batch_id);
CREATE INDEX IF NOT EXISTS idx_claude_calls_agent_ts ON claude_calls(agent_name, ts);

CREATE TABLE IF NOT EXISTS decisions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_id       TEXT NOT NULL,
    decision_date   TEXT NOT NULL,
    score           REAL,
    market_value    REAL,
    signal          TEXT,             -- 'STRONG_BUY' | 'BUY' | 'WATCH' | ...
    method          TEXT,             -- which valuation method was used
    confidence      TEXT,             -- 'HIGH' | 'MEDIUM' | 'LOW'
    reasoning       TEXT NOT NULL,    -- narrative justification
    cross_checks    TEXT,             -- JSON: alternative methods + deltas
    sources         TEXT,             -- JSON: list of source docs/URLs
    created_at      TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_decisions_entity_date ON decisions(entity_id, decision_date);
"""


# ───────────────────────────────────────────────────────────
# 1. LOG EVERY CLAUDE CALL — success or failure
# ───────────────────────────────────────────────────────────

def log_call(
    db_path: str,
    agent_name: str,
    model: str,
    duration_ms: int,
    input_tokens: int = 0,
    output_tokens: int = 0,
    cache_read: int = 0,
    cache_write: int = 0,
    cost_usd: float = 0.0,
    entity_id: Optional[str] = None,
    trace_id: Optional[str] = None,
    batch_id: Optional[str] = None,
    stop_reason: Optional[str] = None,
    attempt: int = 1,
    error_message: Optional[str] = None,
) -> bool:
    """
    Insert one row into claude_calls. Returns False silently on DB error
    (we never crash the pipeline just because logging hiccuped).

    Called from the Anthropic SDK wrapper in a finally block, so the
    row goes in whether the call succeeded or raised.
    """
    if not db_path or db_path == ":memory:":
        return False
    try:
        conn = sqlite3.connect(db_path)
        conn.execute(
            """
            INSERT INTO claude_calls
                (agent_name, entity_id, trace_id, batch_id, model,
                 input_tokens, output_tokens, cache_read, cache_write,
                 duration_ms, cost_usd, stop_reason, attempt, error_message)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                agent_name, entity_id, trace_id, batch_id, model,
                int(input_tokens), int(output_tokens),
                int(cache_read), int(cache_write),
                int(duration_ms), float(cost_usd),
                stop_reason, int(attempt), error_message,
            ),
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error:
        return False


# ───────────────────────────────────────────────────────────
# 2. PERSIST THE FINAL DECISION (with cross-checks)
# ───────────────────────────────────────────────────────────

def persist_decision(
    db_path: str,
    entity_id: str,
    score: float,
    market_value: float,
    signal: str,
    method: str,
    confidence: str,
    reasoning: str,
    cross_checks: Dict,
    sources: List[Dict],
) -> int:
    """
    Insert one row into decisions. Returns the new row's id.
    Re-evaluations are appended, not overwritten — history is the table.
    """
    conn = sqlite3.connect(db_path)
    cur = conn.execute(
        """
        INSERT INTO decisions
            (entity_id, decision_date, score, market_value, signal,
             method, confidence, reasoning, cross_checks, sources)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            entity_id,
            datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            float(score),
            float(market_value),
            signal,
            method,
            confidence,
            reasoning,
            json.dumps(cross_checks, ensure_ascii=False),
            json.dumps(sources, ensure_ascii=False),
        ),
    )
    decision_id = cur.lastrowid
    conn.commit()
    conn.close()
    return decision_id


# ───────────────────────────────────────────────────────────
# 3. QUERY THE TRAIL — months later
# ───────────────────────────────────────────────────────────

def reconstruct_analysis(db_path: str, batch_id: str) -> Dict:
    """
    Pull every Claude call from one analysis batch, in order.
    Useful when investigating "why did we say X on date Y?".
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    calls = conn.execute(
        """
        SELECT ts, agent_name, model, input_tokens, output_tokens,
               cost_usd, attempt, stop_reason, error_message
          FROM claude_calls
         WHERE batch_id = ?
         ORDER BY ts ASC
        """,
        (batch_id,),
    ).fetchall()
    conn.close()
    return {"batch_id": batch_id, "calls": [dict(r) for r in calls]}


def history_for_entity(db_path: str, entity_id: str) -> List[Dict]:
    """
    All decisions ever made for one entity, in chronological order.
    Each row carries its own reasoning and cross-checks at the time.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        """
        SELECT id, decision_date, score, market_value, signal, method,
               confidence, reasoning, cross_checks, sources, created_at
          FROM decisions
         WHERE entity_id = ?
         ORDER BY decision_date ASC, id ASC
        """,
        (entity_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ───────────────────────────────────────────────────────────
# 4. EXAMPLE OF WHAT cross_checks LOOKS LIKE IN PRODUCTION
# ───────────────────────────────────────────────────────────

EXAMPLE_CROSS_CHECKS = {
    "ddm_alternative": 629.0,
    "implicit_pe_from_market": 692.0,
    "broker_consensus": 884.0,
    "gap_to_consensus_pct": -11.7,
    "peg": 1.4,
    "upside_pct": 10.9,
}
"""
That single JSON tells me, six months from now:
  - Primary method said 780.
  - DDM alternative said 629.
  - Market is pricing an implicit P/E of 692 — extremely high.
  - Broker consensus is 884, 11.7% above us.
  - PEG of 1.4, upside of 10.9%.

If the position crashed after I said BUY at 780, I have the exact
state of disagreement at the time of the call. The 'why' is in the row.
"""
