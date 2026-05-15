"""
Snippet 2 — Blocking state machine for a reasoning pipeline
============================================================

Pure Python, no framework. Each method declares its required state
and advances to the next one. If the order is wrong, Python crashes
with AssertionError before any side effect occurs.

Persistence has two layers:
 - in-memory `self.state` for the current run
 - SQLite `agent_<role>_state` table for crash-resume across runs

If you need backwards transitions, parallel regions, or hierarchical
states, use `pytransitions` or `python-statemachine` instead.
This is intentionally minimal for strictly linear pipelines.
"""
from __future__ import annotations
import sqlite3
from typing import Optional, Union, Tuple, Dict, List


class AnalysisPipeline:
    """
    12 sequential phases. Each transition is a method on this class.
    Methods raise AssertionError if called out of order, with no
    side effect, no DB write, no partial state.

    Usage:
        a = AnalysisPipeline(entity_id="X", db_path="prod.db")
        a.load()               # init     → loaded
        a.analyze()            # loaded   → analyzed
        a.characterize("...")  # analyzed → characterized
        # ... etc
    """

    STATES = [
        "init", "loaded", "analyzed", "characterized",
        "contextualized", "classified", "discount_rate_set",
        "growth_rate_set", "estimated", "valued", "checked", "written",
    ]

    JUSTIFICATION_MIN_CHARS = 30

    def __init__(self, entity_id: str, db_path: str):
        self.entity_id = entity_id
        self.db_path = db_path
        self.state = "init"
        # Business fields (filled by the various methods)
        self.data: Dict = {}
        self.profile: Tuple[str, Optional[str]] = ("", None)
        self.discount_rate: float = 0.0
        self.growth_rate: float = 0.0
        self.notes: List[str] = []
        self.warnings: List[str] = []

    # ───────────────────────────────────────────────────────
    # Core helpers — the entire enforcement mechanism
    # ───────────────────────────────────────────────────────

    def _advance_state(self, required: Union[str, Tuple[str, ...]], next_state: str):
        """
        Verify the current state is in `required` and advance to `next_state`.
        This is the whole state machine, in five lines.
        """
        allowed = (required,) if isinstance(required, str) else required
        if self.state not in allowed:
            raise AssertionError(
                f"State required: {allowed}, current state: {self.state}"
            )
        self.state = next_state

    def _assert_justification(self, text: str, threshold: Optional[int] = None) -> None:
        """A non-trivial human-readable justification is required at each gate."""
        threshold = threshold if threshold is not None else self.JUSTIFICATION_MIN_CHARS
        if not isinstance(text, str) or len(text) < threshold:
            raise AssertionError(
                f"Justification too short "
                f"({len(text) if isinstance(text, str) else 0} chars, min {threshold})"
            )

    def _persist_state(self, table: str, row: Dict) -> None:
        """
        Idempotent: INSERT OR REPLACE. Safe to call on retry.
        Silent in test mode (db_path == ':memory:').

        After each successful phase, write the partial state to the
        corresponding agent table. This is what makes crash-resume work.
        """
        if not self.db_path or self.db_path == ":memory:":
            return

        clean = {k: (1 if v is True else 0 if v is False else v) for k, v in row.items()}
        cols = list(clean.keys())
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute(
                f"INSERT OR REPLACE INTO {table} ({', '.join(cols)}) "
                f"VALUES ({', '.join('?' for _ in cols)})",
                [clean[c] for c in cols],
            )
            conn.commit()
            conn.close()
        except sqlite3.Error:
            pass  # log-and-continue, never crash the pipeline on a persistence hiccup

    # ───────────────────────────────────────────────────────
    # The 12 phase methods, each a single transition
    # ───────────────────────────────────────────────────────

    def load(self) -> Dict:
        """Phase 1: read raw data from the DB. Checkpoints on completeness."""
        self._advance_state("init", "loaded")
        self.data = self._read_from_db()
        assert self.data, f"Entity {self.entity_id} not found"
        return self.data

    def analyze(self) -> Dict:
        """Phase 2: deterministic Python computation. No LLM yet."""
        self._advance_state("loaded", "analyzed")
        # ... compute aggregates, normalisations, signals
        self._persist_state("agent_data_state", {"entity_id": self.entity_id})
        return {}

    def characterize(self, thesis: str) -> None:
        """Phase 3: LLM provides a thesis. We accept any non-empty string here."""
        self._advance_state("analyzed", "characterized")
        assert isinstance(thesis, str) and len(thesis) > 0
        self.notes.append(f"THESIS: {thesis}")

    def contextualize(self, web_summary: str) -> None:
        """Phase 4: web research summary. Minimum length enforced."""
        self._advance_state("characterized", "contextualized")
        assert len(web_summary) > 100, "Web summary too short"
        # ... check that required keywords are present
        self.notes.append(f"CONTEXT: {web_summary[:100]}...")

    def classify(self, profile_primary: str, profile_secondary: Optional[str],
                 justification: str) -> None:
        """
        Phase 5: LLM picks a category. Python validates the choice
        against the allowed list AND against a blocklist of incompatible
        pairs from the methodology document.
        """
        self._advance_state("contextualized", "classified")
        ALLOWED_PRIMARY = {"Quality", "Growth", "Value", "Income", "Cyclical",
                           "Defensive", "Turnaround", "Holding", "Special"}
        FORBIDDEN_PAIRS = {
            ("Income", "Turnaround"),
            ("Quality", "Special"),
            # ... etc
        }
        assert profile_primary in ALLOWED_PRIMARY
        assert profile_secondary is None or profile_secondary in ALLOWED_PRIMARY
        if profile_secondary is not None:
            pair = (profile_primary, profile_secondary)
            assert pair not in FORBIDDEN_PAIRS and pair[::-1] not in FORBIDDEN_PAIRS, \
                f"Forbidden category pair: {pair}"
        self._assert_justification(justification)
        self.profile = (profile_primary, profile_secondary)
        self._persist_state("agent_classifier_state", {
            "entity_id": self.entity_id,
            "profile_primary": profile_primary,
            "profile_secondary": profile_secondary,
        })

    def set_discount_rate(self, rate: float, justification: str) -> None:
        """Phase 6: a numeric parameter with hard bounds."""
        self._advance_state("classified", "discount_rate_set")
        assert 9.0 <= rate <= 15.0, f"discount_rate {rate}% out of [9, 15]"
        self._assert_justification(justification)
        self.discount_rate = rate

    def set_growth_rate(self, rate: float, justification: str) -> None:
        """Phase 7: another bounded numeric parameter."""
        self._advance_state("discount_rate_set", "growth_rate_set")
        assert 0.0 <= rate <= 5.0, f"growth_rate {rate}% out of [0, 5]"
        self._assert_justification(justification)
        self.growth_rate = rate

    # ... phases 8-12 elided for brevity. Same pattern throughout:
    #  - first line: self._advance_state(required, next_state)
    #  - next lines: argument validation
    #  - then: business logic
    #  - finally: self._persist_state(...) if applicable


# ───────────────────────────────────────────────────────────
# Crash-resume helpers (called by the orchestrator)
# ───────────────────────────────────────────────────────────

def mark_running(db_path: str, table: str, entity_id: str) -> None:
    """Idempotent: INSERT OR IGNORE then UPDATE status='RUNNING'."""
    conn = sqlite3.connect(db_path)
    conn.execute(
        f"INSERT OR IGNORE INTO {table} (entity_id, status, started_at) "
        f"VALUES (?, 'RUNNING', datetime('now'))",
        (entity_id,),
    )
    conn.execute(
        f"UPDATE {table} SET status='RUNNING', started_at=datetime('now'), "
        f"error_message=NULL WHERE entity_id=?",
        (entity_id,),
    )
    conn.commit()
    conn.close()


def mark_failed(db_path: str, table: str, entity_id: str, error: str) -> None:
    """Mark FAILED. Used in the except block of the orchestrator."""
    conn = sqlite3.connect(db_path)
    conn.execute(
        f"UPDATE {table} SET status='FAILED', error_message=? WHERE entity_id=?",
        (str(error)[:500], entity_id),
    )
    conn.commit()
    conn.close()


def read_status(db_path: str, table: str, entity_id: str) -> Optional[str]:
    """Returns 'DONE', 'RUNNING', 'FAILED', 'NEW', or None if no row."""
    conn = sqlite3.connect(db_path)
    cur = conn.execute(f"SELECT status FROM {table} WHERE entity_id=?", (entity_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None
