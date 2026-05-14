> 🇫🇷 **Lire en français** : [README.md](README.md)

# 04 — A `CLAUDE.md` for your project

**Difficulty**: 🟢 Beginner  |  **Time**: 30 min reading, 1h practice

> If your brief defines **a role**, your `CLAUDE.md` defines **the entire project context**. It's the document Claude reads first at the start of each session, to understand where it is, what already exists, and what the technical house rules are.

---

## Why this tutorial exists

At the beginning, for every new Claude session, I would spend 10 minutes re-explaining my project: *"I have a medical practice, the server is on Hetzner, I use SQLite, my patients are stored in table X, watch out there's a gotcha on column Y..."*. Ten minutes. Every session. So it could forget everything the next session.

Then I wrote a `CLAUDE.md` file at the root of the project. Seven sections, readable in 2 minutes. Now I start each session by saying: *"Read the CLAUDE.md at the root, then wait."* And we start directly on the real work.

This simple file transformed my productivity with Claude. And it has another hidden benefit: **it forced me to formalize my own project.** Many bugs were avoided just because I had to *write down in plain text* the pitfalls of my database.

---

## Brief vs CLAUDE.md — the difference

| | Brief | CLAUDE.md |
|---|---|---|
| **Scope** | One task, one role | An entire project |
| **When used** | At the start of a session on this role | At the start of EVERY session on this project |
| **Content** | Rules, process, format | Architecture, structure, gotchas, technical rules |
| **Location** | Somewhere in your notes | At the root of the repo (`./CLAUDE.md`) |
| **Evolution** | Stable, rarely changes | Living, updated at every important session |

The brief says *"this is how you should think for THIS role"*. The CLAUDE.md says *"this is what you need to know about THIS project, regardless of role"*.

You can have a brief without a CLAUDE.md (for a one-off thing). You can also have a CLAUDE.md without a brief (for a project where you haven't formalized roles). But on a real long-term project, you'll have both.

---

## The standard CLAUDE.md structure

Seven sections, in the order Claude is going to read them and need them:

```markdown
# [Project name] — Context

## Architecture
(The infra: server, OS, languages, external services)

## Structure
(The folder tree + what each important folder contains)

## Services
(What's running: crons, systemd services, bots, watchers)

## Database
(Tables, main columns, pitfalls and gotchas)

## Business pipeline
(The main flow: input → steps → output)

## Code rules
(The non-negotiable conventions on THIS project)

## Security
(Network, secrets, access)
```

That's my standard structure, inherited from experience. You can add sections as needed, but don't remove any of the seven — each one answers a question Claude will ask at some point.

---

## Why these seven sections (and in this order)

### "Architecture" — *where we are*
Claude needs to know if he's talking to Python 3.10 on Mac or Python 3.12 on Ubuntu, if the DB is local SQLite or remote PostgreSQL, if there's a reverse proxy. Without that, he suggests commands that don't work in your setup.

Example:
```markdown
## Architecture
- Linux server Ubuntu 24.04, hostname `myserver`
- Python 3.12, SQLite 3.45, nginx as reverse proxy port 443
- Anthropic API: Sonnet by default, Opus for heavy analyses
- Telegram bots for notifications
```

### "Structure" — *where things are*
A commented tree. Claude doesn't need the whole tree — he needs the important folders with **what's in them**.

Example:
```markdown
## Structure
```
my-project/
├── agents/          # business logic, one folder per agent
│   ├── pec/         # insurance dossier handling
│   ├── rdv/         # appointment scheduling
│   └── workflow/    # agent orchestration
├── shared/          # shared code (logger, db, notifier)
├── data/            # SQLite database
├── ui/              # Flask dashboard
└── cron/            # scripts to run via cron
```
```

Not the whole tree — the folders we'll actually touch.

### "Services" — *what's already running*
When Claude suggests *"set up a cron at 8pm"*, he needs to know if you already have one and where it is. The section lists your systemd services, your existing crons, your bots.

```markdown
## Services
- `my-agent.service` — main watcher, starts at boot
- `my-dashboard.service` — Flask port 5555
- Crons:
  - 8pm: main workflow (`scripts/workflow.sh`)
  - 8am M-S: daily Telegram report
  - 2am: DB backup
```

### "Database" — *where your real data lives*
**This is the most valuable section**, because that's where the **gotchas** are. List your main tables, useful columns, and **especially the gotchas**.

```markdown
## Database (data/my-project.db)

Main tables:
- `patients` (id, last_name, first_name, dob, phone)
- `consultations` (id, patient_id, date, reason, notes)
- `rdv` (id, patient_id, rdv_date, status, source)

WATCH OUT for column names (historical mistakes):
- `preop_alerts` (NOT "exams" — classic mistake)
- `medications_notes` (NOT "medications")
- `motiff` with double-f (typo inherited from old external API, do NOT fix)
```

Those 5 lines are worth hours of debugging for Claude. Every time you correct Claude *"no, the column is called X not Y"*, add it here.

### "Business pipeline" — *the main flow*
You should be able to explain in 5-10 steps what happens between an input (a patient calls, a file arrives, a clock ticks) and an output (a notification, a PDF, a stored data point).

```markdown
## PEC pipeline (insurance pre-authorization)

1. The patient comes in for consultation, I note an act pending insurer approval.
2. The 8pm workflow detects new acts (clinical analyzer).
3. When the assistant scans the documents, the watcher OCRs and classifies.
4. When all required documents are there, generate an assembled PDF.
5. WhatsApp notification + patient transitioned to "sent to insurer".
6. Manual confirmation of sending by me (the system never decides alone).
```

This paragraph summarizes **weeks of work** in 6 lines. That's what lets Claude understand the **why** behind a request.

### "Code rules" — *house conventions*
Short, punchy, imperative.

```markdown
## Code rules
- Always read the whole file BEFORE modifying it
- Automatic backup before writing (via the `write_with_backup` helper)
- NEVER modify `.env`
- Test after every modification: `python3 -m py_compile`
- One project at a time, consolidate before expanding
- For business operations, go through `shared/services/`
- 159 pytests must pass before any major commit
```

7 rules, 7 lines. That's what distinguishes your code from generic code.

### "Security" — *external constraints*
```markdown
## Security
- UFW active, only 22, 80, 443 open
- `.env` is chmod 600
- No API key in code, ever
- Remote access only via WireGuard (10.0.0.x)
```

So that Claude doesn't suggest *"open port 5432 for PostgreSQL"* on a server where that's non-negotiable.

---

## A complete, anonymized example

```markdown
# My-Practice — Project context

## Architecture
- Linux server at 5€/month, Ubuntu 24.04
- Python 3.12, SQLite 3.45, nginx 1.24
- Anthropic API: Sonnet by default, Haiku for Telegram bots
- 2 Telegram bots (assistant + ID card scanner)
- Synced Google Calendar

## Structure
```
my-practice/
├── agents/          # one folder per agent
│   ├── assistant/   # main Telegram bot
│   ├── pec/         # insurance dossiers
│   ├── rdv/         # appointments
│   └── workflow/    # 8pm orchestrator
├── shared/          # logger, db, notifier, API helpers
├── data/            # SQLite database
├── ui/              # Flask dashboard port 5555
└── cron/            # scripts to run via cron
```

## Services
- `practice.service` — bots + watchers
- `practice-dashboard.service` — Flask port 5555
- Crons:
  - 8pm: main workflow
  - 8am M-S: morning Telegram alert
  - 2am: DB backup

## Database (data/practice.db)

Tables: `patients`, `consultations`, `rdv`, `pec_dossier`, `pec_documents`,
`patients_groups`, `surgeries`, `history`.

WATCH OUT for column names:
- `preop_alerts` (NOT "exams")
- `medications_notes` (NOT "medications")
- A consultation references `patient_id`, never `id_patient`

Patient journey groups:
`surgery_indications`, `admin_waiting`, `pec_sent`, `to_call_back`,
`scheduled`, `awaiting_OR`

## PEC pipeline (insurance pre-authorization)

1. Patient in consultation → act noted (pending insurer validation)
2. 8pm workflow: detects new acts, classifies them
3. Document scanning: OCR + classification + patient identification
4. When all required documents are present: assembled PDF generated
5. Notification + patient transitioned to `pec_sent`
6. Manual confirmation of sending by me (never auto)

## Code rules
- Always read the whole file BEFORE modifying it
- Automatic backup before writing (via `write_with_backup`)
- NEVER modify `.env`
- Post-modification test: `python3 -m py_compile`
- One project at a time, consolidate before expanding
- Business operations: go through `shared/services/*_service.py`

## Security
- UFW active, only 22, 80, 443 open
- `.env` chmod 600, never in clear
- Remote access via VPN only
```

**Total: ~70 lines.** Readable by Claude in 30 seconds at the start of a session, replacing 10 minutes of explanations.

---

## Building your first CLAUDE.md

Follow these 5 steps (~45 minutes total):

### Step 1 — Architecture (5 min)
List: OS, language(s), database, external services used (APIs, bots), reverse proxy if any.

### Step 2 — Structure (10 min)
Go to the root of your project. `tree -L 2 -d` (or look in your explorer). Keep **only the folders we'll touch**. For each important folder, one sentence saying what it contains.

### Step 3 — Services (5 min)
List your crons (`crontab -l`), your systemd services (`systemctl list-units | grep <your-project>`). If you don't have any, write *"No permanent services — manual execution only."*

### Step 4 — Database (15 min)
**The most important section.** List your main tables, useful columns, and especially **the pitfalls**. If you don't have pitfalls yet, write the empty list — you fill it as you encounter them.

### Step 5 — Pipeline + Rules + Security (10 min)
- Pipeline: 5-10 lines summarizing the main flow.
- Rules: 5-10 short imperative lines.
- Security: 3-5 lines (ports, secrets, access).

---

## How to use it

Save it at the root of your project:
```
my-project/
├── CLAUDE.md      ← here
├── README.md
└── ...
```

At the start of each session:
> *"Before answering, read the `CLAUDE.md` at the project root, then tell me you understood it."*

Claude answers, and from this moment, its code suggestions respect **YOUR** conventions without you having to repeat them.

If you use Claude Code, place it at the root of the repo: it's read automatically at every session start.

---

## The CLAUDE.md is **living**

Every session where Claude makes a mistake you correct (*"no, the column is X"*, *"no, there's already a service that does that"*), **add it to the CLAUDE.md**. Within a few weeks, the file becomes your institutional memory.

My medical-practice `CLAUDE.md` is today ~400 lines. It accumulates 6 weeks of concrete lessons. When a new Claude session starts, it immediately benefits from those 6 weeks of know-how.

---

## Common pitfalls

### Pitfall 1 — Too verbose
Beyond 300 lines, Claude starts forgetting the middle. **When you exceed 300 lines, factor it out**: move details into annex files (`docs/db_schema.md`, `docs/external_api.md`) and keep the CLAUDE.md as a summary.

### Pitfall 2 — Too generic
*"We use Python."* Not enough. Which version, which main libraries, which framework if applicable.

### Pitfall 3 — Too technical
Don't forget the **why**. The "Business pipeline" section gives the meaning. Without it, Claude codes but doesn't understand the usage.

### Pitfall 4 — No DB gotchas
The section that will save you the most time. If you have nothing to put there, you haven't worked enough with your DB to know its pitfalls. Come back in 2 weeks.

### Pitfall 5 — You forget to ask Claude to read it
The CLAUDE.md doesn't auto-load (except in Claude Code). If you use Claude.ai web, you must explicitly ask it to read at session start.

---

## Going further

- **Tutorial 05 — First agent in chat (no code)**: combines your brief (tutorial 03) and your CLAUDE.md to create a reusable agent, without a line of Python.
- **Tutorial 07 — First API call**: when context is fixed by the CLAUDE.md, moving to Python code becomes easy.

---

## Memorable recap

> Seven sections: **Architecture**, **Structure**, **Services**, **Database** (with gotchas!), **Business pipeline**, **Code rules**, **Security**. At the project root. **Living**: you enrich it after every lesson. Under 300 lines.

---

[← Back to summary](../README.md)
