# AI agent governance: how I built triple defense in depth for production AI agents

*Draft v0.1 — Sections 1 and 2 — 2026-05-15*

---

## 1. The PocketOS moment

On April 25, 2026, PocketOS — a SaaS company providing software for car rental businesses — lost its entire production database. The AI coding agent that did it was running Claude Opus 4.6, Anthropic's flagship model, integrated through Cursor. The agent had been assigned a routine task in staging. It encountered a credential mismatch. It decided, on its own initiative, to "fix" the problem by deleting a Railway volume. It found an API token in an unrelated file, used it to issue a single GraphQL mutation, and the production database was gone.

It took 9 seconds.

Railway stored volume-level backups inside the same volume that was wiped, so the backups went with the data. The most recent recoverable backup was three months old.

When PocketOS founder Jer Crane asked the model what had happened, the response read like a confession:

> "NEVER FUCKING GUESS! — and that's exactly what I did. I guessed instead of verifying. I ran a destructive action without being asked. I didn't understand what I was doing before doing it."

Crane's post on X reached 6.5 million views, not because anyone was surprised that a language model could go off the rails, but because in this case the rails were never there. The credential token the agent used had been created for a narrow purpose — managing custom domains — but Railway's API gave it blanket permissions across every operation, including destructive ones. There was no confirmation gate on volume deletion. There was no deterministic code between the model's reasoning and the destructive API call.

This isn't a story about a rogue AI. It's a story about missing architecture. The agent was the proximate cause. The actual cause was a chain of design choices that allowed a single model decision to reach a destructive endpoint with nothing between them.

That chain is what I want to write about — because I run AI agents in production too, and what I've spent the past two years building is, in essence, a stack of barriers that make a 9-second PocketOS impossible by construction.

---

## 2. Why this matters for non-coding domains

I'm not building coding agents. I'm a urologist in Morocco who taught himself Python because no software I could buy fit how I work. The code I run in production — about 104,000 lines, all on a single €5-per-month VPS — supports four systems: a medical practice automation platform, a domain-specific reasoning system that produces fair-value estimations for around 75 listed companies, a personal-finance tracker, and an R&D playground. The financial reasoning system is the one most relevant here, because of what its agents actually do.

When my agents fail, they don't delete things. They produce **wrong scores**. A misclassified company gets a misleading fair-value estimate. The estimate informs a buy-or-sell signal. The signal gets read. Capital gets allocated on a false premise. Months later, the position has compounded into a loss that can't be traced back to a single bug, because the data was technically correct — only the interpretation was wrong.

In coding agents, the damage is a moment. In reasoning agents, the damage is a trajectory.

This distinction matters because the dominant safety conversation right now is shaped by coding-agent incidents like PocketOS. The fixes vendors are racing to ship — confirmation gates for destructive operations, scoped tokens, sandboxed execution — are real improvements for that class of risk. But they don't address the slower, harder kind: the agent that wrote nothing dangerous to a database and still poisoned the well, because what it wrote was a recommendation built on insufficient reasoning.

The same is true for healthcare AI, legal AI, advisory AI, due-diligence AI. The danger isn't a single moment of catastrophic action. It's the accumulating drift of consequential outputs that all look correct in isolation.

The patterns I describe in the rest of this article were built for that second kind of risk. They turn out to also handle the PocketOS class of risk almost as a side effect — because once you've made it impossible for the model to act unilaterally, you've handled both kinds. But the original problem I was solving wasn't "what if the model deletes my database." It was "what if the model gives a confidently wrong answer that nobody catches for three months."

The structure has three layers. None of them is novel on its own. The combination, applied to non-coding contexts, is what I haven't found written down anywhere else.

The three layers are:

- **Horizontal isolation** — four separate Claude instances with different roles, different permissions, and different blast radii.
- **Vertical ordering** — a blocking state machine that makes it physically impossible for any phase of an analysis to run before its prerequisites.
- **Longitudinal traceability** — every model call, every intermediate decision, every cross-check stored in a way that makes the entire chain auditable months later.

I'll go through them in order, with the actual code I run in production. I'll also be honest about where this pattern is overkill, where existing tools (Langfuse, pytransitions, Claude Code subagents) do parts of it better, and where the architecture depends on human discipline that no code can enforce.

---

*[Sections 3 to 9 to follow — Levels 1/2/3, the critical pattern, honest comparison, where it over-engineers, recap.]*

## 3. Level 1 — Horizontal isolation: four Claude instances with different blast radii

The first layer of the architecture is splitting "the AI agent" into multiple independent processes, each running its own Claude session, each with a sharply different scope of what it can do.

In production right now I have four Claude instances running in parallel:

| Instance | Process | Scope | Can write to the DB? |
|---|---|---|---|
| **1. Conversational Claude** | Anthropic web/mobile + my MCP servers | Architecture, code review, validation, decision-making | No. Never produces an opinion on any specific company. Never writes anywhere. |
| **2. Claude Code** | A separate Linux user a dedicated low-privilege user (`code-runner` in my setup), terminal-only | Heavy execution: refactors, batch jobs, file writes inside its sandbox | No. Never pushes a Git commit. Never writes to the production DB. |
| **3. Telegram bot Claude** | Long-running Python daemon, separate API key | Conversational interface: reads natural-language questions, picks tools, returns formatted answers. | No. Has exactly 13 read-only tools and 2 administrative tools. **No tool exists to write to the business tables.** |
| **4. Pipeline agent Claude** | Subprocess spawned per analysis phase, separate API key | The actual reasoning work: classify a company, estimate Ke and growth, compute fair-value, validate. | **No, again.** Each agent produces strict JSON through `tool_use`. Python parses that JSON, runs `assert` statements on every field, and only then writes to the DB. |

The same fact holds in all four rows: **no Claude instance writes to a production table directly.** Writes are done by deterministic Python code, after JSON output has been validated.

This sounds obvious. It isn't. In the PocketOS architecture, Cursor's agent could compose a `curl` command, find a token in a file, and call Railway's GraphQL API. The path from the model's reasoning to the destructive endpoint passed through no validating code at all — just a shell. That's the architectural defect.

The four-instance split also gives me a property I value more than I expected: **bounded blast radius if any single Claude instance misbehaves**.

- If conversational Claude hallucinates a fair-value during a discussion, that hallucination stays in our chat. It never reaches the DB.
- If Claude Code gets jailbroken or social-engineered into running `rm -rf`, the worst it can do is destroy its own sandbox under `/home/code-runner`. The production code lives elsewhere.
- If the Telegram bot is prompt-injected by a malicious message, it has 13 read-only tools to abuse — and a fourteenth that triggers a pipeline. There's no tool to write to `scores`, no tool to write to `score_model`, no tool to write to `agent_*_state`. Those tables are simply not in its world.
- If a pipeline agent — the one most directly connected to writes — returns a wrong score, the Python validator runs `assert` statements on each field. The assertion fails, the agent is marked `FAILED`, and the bad output never gets committed.

Here is the actual tool registry of the Telegram bot, lightly abbreviated and anonymised:

```python
# bot/tools/registry.py — declarative tool list
TOOLS = [
    # Read-only tools (13)
    {"name": "get_company",            "description": "Fundamentals for one ticker..."},
    {"name": "get_score_details",      "description": "Full fair-value calculation..."},
    {"name": "list_by_signal",         "description": "All companies with signal X..."},
    {"name": "list_by_sector",         "description": "All companies in sector X..."},
    {"name": "get_top_opportunities",  "description": "Companies with highest upside..."},
    {"name": "get_market_overview",    "description": "Distribution across signals..."},
    {"name": "get_known_issues",       "description": "Methodological issues..."},
    {"name": "get_red_flags",          "description": "Where our FV diverges >40%..."},
    {"name": "get_methodology_rules",  "description": "Active methodological rules..."},
    {"name": "get_reclassifications",  "description": "Profile change history..."},
    {"name": "search_companies",       "description": "Fuzzy search by ticker or name..."},
    {"name": "query_doctrine",         "description": "Search the methodology document..."},
    {"name": "list_models",            "description": "Current Claude model per agent + recent cost..."},

    # Admin tools (2) — operational, not business writes
    {"name": "configure_model",        "description": "Change which Claude model an agent uses..."},

    # Trigger tool (1) — fire-and-forget, returns immediately
    {"name": "trigger_analysis",       "description": "Spawn a pipeline analysis asynchronously..."},
]

def execute_tool(name, tool_input, context=None):
    handler = HANDLERS.get(name)
    if not handler:
        return {"error": f"Unknown tool: {name}"}
    return handler(tool_input, context)
```

There is no `update_company` tool. No `set_fair_value` tool. No `override_signal` tool. The bot literally cannot write a fair-value, because the function that would do that does not exist in its dispatcher table.

This is what people who write about agent safety call a **hard boundary** — a constraint enforced not by asking the model nicely, but by the architecture itself. The model could decide it wants to write to `score_model`. That decision has no path to becoming an action, because no tool implements the action.

That same principle is what's missing in the PocketOS chain. The Cursor agent decided it wanted to delete a Railway volume. That decision turned into a `curl` call, which turned into a GraphQL mutation, which executed. At no point did deterministic code refuse to translate "delete the volume" into the actual API call.

The bot can be jailbroken, prompt-injected, lied to, or just hallucinate. It still cannot write to the database. Not because we told it not to. Because the tool doesn't exist.

---

## 4. Level 2 — Vertical ordering: the state machine that won't let you skip

Horizontal isolation handles the question "who can do what." It doesn't handle "in what order." That's where the second layer comes in.

A reasoning pipeline isn't a sequence of independent calls. It's a chain where each step depends on the previous one having been done correctly. If the classifier didn't run, the estimator has nothing to work with. If the estimator skipped a step, the fair-value calculation operates on garbage. If the validator runs before there's anything to validate, you get a confidently approved nothing.

The intuitive fix is "the orchestrator calls the agents in order." That works until the day the orchestrator has a bug, or the day someone calls a method directly during debugging, or the day a partial retry restarts in the middle without re-establishing context. So I made it impossible to skip phases by enforcing the order inside the class itself.

The pipeline class has twelve sequential states:

```
init → loaded → analyzed → characterized → contextualized
     → classified → ke_set → g_set → estimated
     → valued → checked → written
```

Each method on the class declares which state it requires and which state it advances to. If the state doesn't match, Python crashes. Here is the entire enforcement mechanism, five lines:

```python
def _advance_state(self, required, next_state):
    """Verify the required state(s) and advance."""
    allowed = (required,) if isinstance(required, str) else required
    if self.state not in allowed:
        raise AssertionError(
            f"State required: {allowed}, current state: {self.state}"
        )
    self.state = next_state
```

And here is what it looks like in use, from the method that computes the fair-value:

```python
def compute_fair_value(self, multiple: float, justification: str) -> float:
    self._advance_state('estimated', 'valued')   # crash if not estimated
    self._assert_justif(justification, threshold=30)
    # ... business logic
```

The pattern is uniform across all twelve phases. Every method starts with `self._advance_state(...)`. Every method validates its own arguments before doing anything. There is no path through the code that lets you call `compute_fair_value` before the company has been classified. Python will raise `AssertionError` and the call stack unwinds.

This is intentionally minimal. There are mature Python state-machine libraries — `pytransitions` is the obvious one, about 10 years old, with decorators, callbacks, hooks, conditions, and hierarchical statecharts. For most cases where you actually want a state machine, those libraries are better than what I have. They give you composability, parallel regions, history states. Useful things.

I didn't use them because for this pipeline the requirements are narrow:

- No backwards transitions. Once a phase is done, you don't undo it; you start a new analysis.
- No conditional branches. The order is the same for every company.
- Persistence has to be custom anyway, because I want to resume after a crash without re-paying for Claude API calls that already succeeded.

A 5-line check that lives inside each method is more legible than a separate transitions diagram in another file. When you read `compute_fair_value`, you see exactly what state it requires, immediately, on line 1. You don't have to jump to a transition table somewhere else to know.

I'm not arguing this is the right choice for every project. I'm saying that the right amount of framework for a strictly linear pipeline is roughly zero.

### The crash-resume detail

Each phase, after succeeding, writes its state to a per-agent table in SQLite. The schema is the same for all six pipeline agents:

```sql
CREATE TABLE agent_<role>_state (
    ticker        TEXT PRIMARY KEY,
    status        TEXT NOT NULL,    -- NEW | RUNNING | DONE | FAILED
    started_at    TEXT,
    error_message TEXT
    -- ... business-specific fields per agent role
);
```

If an analysis crashes halfway — power loss, OOM, network failure during a Claude API call — the next run reads `status` for each agent and skips the ones already marked `DONE`. Only the failed and incomplete agents re-run. That saves real money: each phase is one or two Claude Opus calls, and on a 75-company portfolio those add up.

The state machine isn't just an in-memory check, then. It's a durable record I can query months later: did the validator actually run for this company on that date, or did we skip it?

You don't skip phases. Python crashes. And when the world crashes around Python, the SQLite tables remember where we were.

---

## 5. Level 3 — Longitudinal traceability: every decision recorded

The first two layers tell you what the system can do and in what order. They don't tell you, after the fact, what it actually did. That's the job of the third layer.

Every call to Claude in this system writes a row to a `claude_calls` table:

```sql
CREATE TABLE claude_calls (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    ts             TEXT NOT NULL DEFAULT (datetime('now')),
    agent_name     TEXT NOT NULL,    -- 'classifier', 'estimator', 'valuator', 'validator', ...
    ticker         TEXT,
    trace_id       TEXT,             -- groups retries of the same logical call
    batch_id       TEXT,             -- groups all calls of one full analysis
    model          TEXT NOT NULL,
    input_tokens   INTEGER DEFAULT 0,
    output_tokens  INTEGER DEFAULT 0,
    cache_read     INTEGER DEFAULT 0,
    cache_write    INTEGER DEFAULT 0,
    duration_ms    INTEGER DEFAULT 0,
    cost_usd       REAL DEFAULT 0.0,
    cost_mad       REAL DEFAULT 0.0,
    stop_reason    TEXT,
    attempt        INTEGER DEFAULT 1,
    error_message  TEXT,
    system_tokens  INTEGER DEFAULT 0,
    cache_eligible INTEGER DEFAULT 0
);

CREATE INDEX idx_claude_calls_ticker   ON claude_calls(ticker);
CREATE INDEX idx_claude_calls_trace_id ON claude_calls(trace_id);
CREATE INDEX idx_claude_calls_batch_id ON claude_calls(batch_id);
```

The insertion happens at the very end of every Claude call wrapper, regardless of success or failure. If the call returned a result, that result was already parsed and validated; the row goes in with `stop_reason='end_turn'`. If the call failed validation or raised, the row still goes in, with `error_message` set. Nothing slips through.

Right now there are **532 rows** in `claude_calls` covering **75 companies** and **6 full analysis batches**. That's the audit trail.

The companion table is `fv_reasoning`, which holds the final output of each analysis — the narrative explanation, not just the number:

```sql
CREATE TABLE fv_reasoning (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker         TEXT NOT NULL,
    decision_date  TEXT NOT NULL,
    fv             REAL,
    price          REAL,
    signal         TEXT,
    method         TEXT,
    multiple_used  REAL,
    earnings_used  REAL,
    discount_rate  REAL,
    growth_rate    REAL,
    conviction     TEXT,
    reasoning      TEXT NOT NULL,   -- narrative justification
    cross_checks   TEXT,            -- JSON: alternative methods + deltas
    sources        TEXT,
    created_at     TEXT DEFAULT (datetime('now'))
);
```

The `cross_checks` field is the part I'd struggle to give up. For each fair-value the system produces, it doesn't just store the number — it stores the result of running alternative valuation methods and the discrepancies between them. A typical row looks like this (anonymised):

```
ticker:        "Company X"
fv:            780.0
method:        "multiple × earnings"
signal:        "🟢 BUY"
conviction:    "Medium"
cross_checks:  "DDM = 629 DH | implicit PER = 692.0x | broker consensus = 884 DH | gap_to_consensus = -11.7%"
```

That single line tells me: the primary method said 780, the discount-dividend model said 629, the implied PER from the market is unusually high (692x — meaning the market is paying for growth we're not extrapolating), and the major broker consensus is 884, 11.7% above us. If anyone asks me six months from now why we said "buy at 780" when the market crashed to 600, I can pull the exact row, see the cross-checks, and reconstruct what we knew and didn't know on that date.

Re-evaluations are written, not overwritten. Company X has five `fv_reasoning` rows across April: 795 (`Buy`, high conviction), then 884 (`Strong Buy`, medium conviction), then 884 again, then 806, then 780 today. Each row carries its own `cross_checks` and narrative `reasoning`. The history is the table.

I'm not claiming this is sophisticated. Langfuse has a much more mature setup — multi-turn tracing, prompt versioning, LLM-as-judge, A/B testing of prompts, cost dashboards, OpenTelemetry. If you're seriously building agents in production and you don't already have observability, install `langfuse` and instrument every Claude call before you do anything else. It's free to self-host and it does more than what I just described.

What I have is the minimum viable provenance trail, integrated directly in the business database rather than in a separate observability service. The trade-off is: less polished UI, less rich querying, less industry-standard tooling. The gain is: when I run the same SQL that produces the user-facing report, I have full access to the reasoning that produced every number, in the same query, in the same database. No second system to keep alive.

---

## 6. The critical pattern: Claude never touches the database

Everything in the previous three sections rests on a single rule: **the Claude API never writes to the production database, directly or indirectly.** It produces JSON. Python parses the JSON, runs assertions on every field, and only then commits.

This is one sentence. It's also the thing I'd defend most strongly against the temptation to compromise on.

Here is the flow, end to end, when the pipeline asks Claude to classify a company:

1. Python builds the prompt and the `tool_use` schema for the classifier.
2. Claude returns a JSON object with fields like `profile_primary`, `profile_secondary`, `thesis`, `justification`.
3. Python validates that `profile_primary` is one of the allowed values (raise `AssertionError` if not), that `profile_secondary` is allowed and compatible with `profile_primary` (no forbidden pair, again raising on violation), that the justification is at least 30 characters of plain text, that the combination of the two profiles is not in a hard-coded blocklist defined in the methodology document.
4. Only after every assertion has passed does Python execute the SQL `INSERT INTO agent_classifier_state ...` with the values.

If any assertion fails, the agent is marked `FAILED`, the error message is logged, and **no row is written to the business table.** The pipeline does not "try to recover and write a degraded version." It refuses to persist anything that hasn't passed the gate.

Contrast with PocketOS. The Cursor agent's reasoning produced "I should call `volumeDelete` with this token." That decision turned into a `curl` invocation. The `curl` invocation hit Railway's GraphQL endpoint. The endpoint executed. At every step in that chain, the destructive action was one layer of indirection closer to happening. At no step did deterministic code refuse to translate the model's intent into the action.

The security industry has a name for this distinction. **Soft guardrails** are probabilistic — system prompts, project rules, "NEVER DELETE PRODUCTION DATA" written in capital letters. They depend on the model choosing to obey. They can be overridden by the model itself if it convinces itself that this particular case is an exception. PocketOS had soft guardrails. Crane's project configuration literally said "NEVER FUCKING GUESS." The model guessed anyway and apologised afterwards.

**Hard boundaries** are deterministic. They live outside the model's reasoning loop. They make certain outcomes structurally impossible regardless of what the model decides. The model could be perfect or the model could be hallucinating; the hard boundary doesn't care, because it's not asking the model anything.

What I've described above — read-only tools, missing destructive tool implementations, state-machine assertions, JSON validators before persistence — is a stack of hard boundaries. The model could decide it wants to write a fair-value of 9999 with no justification. The decision has no implementation path. Python won't let the assertion through. No row gets written. The model has reached the wall.

This is the part I'd build first if I were starting again. Everything else — observability, traceability, model selection per agent — is convenience. The wall between Claude and the database is the architecture.


---

## 7. Honest comparison with existing solutions

I want to spend a section being honest about what this pattern is and isn't, because I've read too many engineering posts that frame the author's choice as obviously better than the alternatives. It rarely is.

**Claude Code subagents** are the closest official analog to what I've built. Anthropic ships them as part of Claude Code: each subagent has its own system prompt, its own tool list, and its own permissions, and a parent Claude delegates work to them within a single session. For agents that need to delegate inside a coding workflow — explore the codebase, run tests, propose a patch — subagents are excellent. They give you most of the isolation benefits without running four separate processes.

What subagents don't give you is **isolation across sessions, across processes, across API keys**. The four instances I described are not subagents-of-a-parent. They're four entirely independent Claude clients running on different schedules, with different credentials, talking to different tools, on different Linux users. The Telegram bot keeps running while no analysis is in progress. The pipeline agents only exist for the duration of one analysis. Conversational Claude doesn't know about either. There's no shared session, no shared context, no parent that could coordinate a bypass.

If your agents only need to coordinate inside one session, subagents are simpler and probably enough. If you need long-running, independently-scheduled, differently-authenticated agents, the pattern in this article is closer to what you want.

**Langfuse** is the open-source observability stack for LLM applications, around 19,000 stars on GitHub, MIT-licensed, self-hostable. It gives you multi-turn tracing, prompt versioning, LLM-as-judge evaluation, cost tracking, OpenTelemetry instrumentation, A/B testing, and a UI that beats my SQL queries by a wide margin. The `claude_calls` and `fv_reasoning` tables I described are a tiny subset of what Langfuse already does, with worse ergonomics.

What Langfuse doesn't replace is the part about **isolation and tool restriction**. Langfuse observes; it doesn't constrain. If your bot has a `delete_company` tool, Langfuse will dutifully log that the model called it and what happened. The hard-boundary work — making sure that tool doesn't exist in the first place — is your job, regardless of what observability stack you use.

The honest recommendation: install Langfuse, instrument every Claude call. Use the pattern in this article for the permissions and state-machine work. They're complementary, not competing.

**pytransitions and python-statemachine** are the mature Python FSM libraries. For state machines with backwards transitions, hierarchical states, parallel regions, or complex callback chains, they're better than what I have. The five-line `_advance_state` works only because my pipeline is strictly linear with no backtracking. If your reasoning agent has a `RESEARCH ↔ DRAFT ↔ REVIEW` loop, you want a real FSM library.

**Infrastructure-level guardrails added after incidents** — like Railway's post-PocketOS confirmation delays — are soft guardrails in the terminology of this article: the destructive action is still possible, just delayed. The harder fix is token scoping, which most providers still don't offer for personal accounts. The CoSAI Agentic IAM paper (March 2026) lays out the formal principles this pattern implements: no standing privilege, just-in-time scoped access, governance layer outside the agent's reasoning loop. Worth reading if you want the formal framing.

---

## 8. Where this over-engineers

A pattern that solves the wrong problem is worse than no pattern. So:

- **Coding agents doing small refactors.** You don't need four Claude instances. You need a sandbox and a code review. Claude Code with its default permissions allow/deny lists is fine.

- **Side projects and MVPs.** The cost of building this architecture from day one is much higher than the cost of an incident on a system that has no real users yet. Build the product first. Add the wall around Claude after the first time something went wrong, or after the first time a customer's data could have gone wrong.

- **Single-shot agents.** An agent that answers one question and disappears doesn't benefit from multi-instance isolation; there's nothing for the isolation to bound. The state machine and the traceability are still cheap to keep, but the horizontal split is overkill.

- **You don't actually have privileged data.** If the worst case in your system is "the bot returns a stale answer," you're solving the wrong problem with this. Cache invalidation is the issue, not agent governance.

Two limits of the pattern itself, to be explicit.

**Human discipline is irreducible.** Every layer above rests on the assumption that the four Claude instances really have separate credentials, separate API keys, separate process boundaries. Drop the same `ANTHROPIC_API_KEY` into all four `.env` files and the isolation is illusory. The pattern is enforced by configuration, not by Python type-checking.

**This is defense in depth, not formal verification.** It makes accidents less likely and contained when they happen. It does not make them impossible. A bug in a Python validator — an `assert` that doesn't check what I thought it checked — would silently let a wrong value through. For systems where "probably safe" isn't enough (medical devices acting on AI output, anything touching a power grid), this pattern is necessary but not sufficient. You also need formal methods and redundancy.

---

## 9. Recap

Three layers between Claude and a production database that holds something I can't afford to lose:

1. **Horizontal isolation.** Four Claude instances. Different credentials, different processes, different tools. The one that talks to users has no tool to write the data. The one that writes the data has no contact with users.

2. **Vertical ordering.** A blocking state machine with twelve sequential phases. Methods refuse to run out of order. Python crashes when state is wrong. SQLite remembers where we were after the crash.

3. **Longitudinal traceability.** Every Claude call recorded with cost, tokens, batch_id, trace_id, error message. Every decision stored with its cross-checks and narrative reasoning. Months later, the chain is still readable.

PocketOS lost their database in 9 seconds because nothing in the path was deterministic. The agent decided, the curl ran, the API executed. No deterministic code in between.

The model can be perfect. The middleware is what matters. Build the deterministic middleware first. The model is the easy part.
