# Triple defense in depth for AI agents — code snippets

Reference code for the article *"AI agent governance: how I built triple defense in depth for production AI agents"*.

Three layers, three files:

| Layer | File | What it shows |
|---|---|---|
| **Horizontal isolation** | `01_tool_registry.py` | The full set of tools available to a long-running bot agent. 13 read-only, 2 admin, 1 fire-and-forget trigger. No DB write tool exists on this surface. |
| **Vertical ordering** | `02_state_machine.py` | A 12-phase blocking state machine in pure Python (5-line core). Methods refuse to run out of order. SQLite remembers where we are after a crash. |
| **Longitudinal traceability** | `03_provenance.py` | Two SQLite tables: `claude_calls` for every API call (cost, tokens, errors), `decisions` for every business output (narrative reasoning, cross-checks JSON, sources). |

## Status

These snippets are extracted, anonymised, and slightly simplified from a production codebase (~17k LOC) that has handled ~500 Claude calls across ~75 entities, with full crash-resume.

The point isn't that the code is novel — it isn't. The point is that the combination is what makes it robust: tool restrictions, blocking transitions, and persistent traceability working together.

## License

MIT — use, adapt, learn from. No warranty. If you build something on top, I'd love to hear about it.

— Kryscekk
