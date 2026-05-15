# Triple defense in depth for production AI agents

A pattern stack for AI agents that handle high-stakes, non-coding workloads (financial reasoning, healthcare assistance, due diligence). Three layers — horizontal isolation, vertical ordering, longitudinal traceability — combined into one architecture.

## Read

- [English version](en/README.md) — main article (~4 800 words)
- [Version française](fr/README.md) — article complet (~5 000 mots)

## Reference code

- [`assets/architecture.mmd`](assets/architecture.mmd) — Mermaid source of the architecture diagram
- [`assets/architecture.svg`](assets/architecture.svg) — rendered SVG (~47 KB)
- [`snippets/`](snippets/) — three runnable, anonymised Python snippets:
  - `01_tool_registry.py` — bot tool surface (13 read-only + 2 admin + 1 trigger)
  - `02_state_machine.py` — 12-phase blocking state machine, 5-line core
  - `03_provenance.py` — claude_calls + decisions schemas + query helpers

Also available as a [public GitHub Gist](https://gist.github.com/Kryscekk/a3a445d10e2e44f8ea615cb7f9850914).

## Why an essay folder and not a numbered tutorial?

The numbered tutorials (`01-…` through `17-…`) teach incremental building blocks. This piece is different: it describes an architecture pattern that emerged from running ~100k LOC across four production codebases, in response to incidents like the PocketOS database deletion of April 2026. It's a step back, not a step forward.

— Kryscekk, May 2026
