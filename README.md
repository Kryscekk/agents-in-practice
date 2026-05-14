> ### 🤖 This repo is run by my AI.
> Tutorials, posts, code, profile — everything written and managed end-to-end by my AI, from my own production code and projects. My role: decide and validate. Its role: execute, autonomously. To my knowledge, no one publicly owns this position today. I do — deliberately.

---

# Agents in Practice

> Learn how to build AI agents with Claude — from zero to production.

**Author**: Driss Amiroune — urologist in Fès, Morocco. Self-taught software architect.

This repo was originally written in French. **All 9 published tutorials are now available in English** (translation completed May 2026). Tutorials 10-17 are still being written and will be released in both languages.

🇫🇷 [Aussi disponible en français — cliquer ici](#français)

## Why this repo

A few months ago, I didn't know what an API was. Today I run four production systems thanks to Claude — one to manage my medical practice, one to analyze the stock market, one for my personal finances, and one for personalized AI watch.

This repo is what I wish I had found at the beginning. Not an abstract course, not dry official docs, not a 2-hour YouTube tutorial that skims everything. **The real journey**: first learn to *talk* to Claude (without writing a single line of code), then — only when the method is solid — move to Python and tools.

That's the order I actually followed during my first 6 weeks. Other tutorials make you start with the API. I start with the **discipline of thought**.

## What I already run (and which isn't open source)

- **~104,000 lines of Python** in production, added in a few months
- **4 business systems** orchestrated by Claude, on **a single server under 5€/month**
- **4 MCP servers** in parallel (medical practice, stock valuation, finances, R&D)
- **Defense-in-depth**: 4 separated Claude roles with safeguards preventing the agent from touching prod by accident
- **Versioned methodology charter** across 228 iterations, separated from code, enforced by `AssertionError` citing sections
- **Medical pipeline**: insurance dossier handling — OCR, patient identification, PDF assembly, WhatsApp notifications
- **Fundamental stock-valuation platform**: 7 archetypes × 68 parameters, 319 passing tests
- **30 orchestrated cron jobs**, automated supervision, medico-legal audit logs per domain
- **claude-agent-sdk** with `@tool` + `can_use_tool` callback for human-in-the-loop validation

None of these systems is open source — they hold sensitive data (patients, accounts). But **the patterns I built along the way will land here, as tutorials**, as they become stable enough to be pedagogically clear.

## Tutorials

✅ = published  ·  🇬🇧 = English version available  ·  🇫🇷 = French only (translation in progress)  ·  🚧 = being written

### Part 1 — Talking to Claude (no code)

| # | Tutorial | Folder | Status |
|---|---|---|---|
| **01** | How to talk to Claude so he understands you | [`01-talking-to-claude/`](01-talking-to-claude/) | ✅ 🇬🇧 🇫🇷 |
| **02** | What is an AI agent, really? | [`02-what-is-an-agent/`](02-what-is-an-agent/) | ✅ 🇬🇧 🇫🇷 |
| **03** | Building your first brief (a Claude role) | [`03-your-first-brief/`](03-your-first-brief/) | ✅ 🇬🇧 🇫🇷 |
| **04** | A `CLAUDE.md` for your project | [`04-claude-md/`](04-claude-md/) | ✅ 🇬🇧 🇫🇷 |
| **05** | Your first agent in chat (no code) | [`05-first-agent-in-chat/`](05-first-agent-in-chat/) | ✅ 🇬🇧 🇫🇷 |
| **06** | When and why to move to the API? | [`06-moving-to-the-api/`](06-moving-to-the-api/) | ✅ 🇬🇧 🇫🇷 |

### Part 2 — Building agents in Python

| # | Tutorial | Folder | Status |
|---|---|---|---|
| **07** | Your first Anthropic API call | [`07-first-api-call/`](07-first-api-call/) | ✅ 🇬🇧 🇫🇷 |
| **08** | **The 4 pillars of a production-grade agent** | [`08-the-4-pillars/`](08-the-4-pillars/) | ✅ 🇬🇧 🇫🇷 |

### Part 3 — Giving Claude tools (MCP)

| # | Tutorial | Folder | Status |
|---|---|---|---|
| **09** | Your first MCP server (4 useful tools) | [`09-first-mcp-server/`](09-first-mcp-server/) | ✅ 🇬🇧 🇫🇷 |
| **10** | Running your agent 24/7 with systemd | [`10-systemd-for-your-agent/`](10-systemd-for-your-agent/) | 🚧 |
| **11** | Making your agent speak via Telegram | [`11-telegram-bot/`](11-telegram-bot/) | 🚧 |

### Part 4 — Advanced patterns

| # | Tutorial | Folder | Status |
|---|---|---|---|
| **12** | Tracing every API call cost | [`12-cost-tracker/`](12-cost-tracker/) | 🚧 |
| **13** | Fix "database is locked" in SQLite | [`13-sqlite-locked/`](13-sqlite-locked/) | 🚧 |
| **14** | Versioning `/etc/nginx` with Git | [`14-nginx-in-git/`](14-nginx-in-git/) | 🚧 |
| **15** | URL screenshots from your agent | [`15-url-screenshot/`](15-url-screenshot/) | 🚧 |
| **16** | Free web search from your agent | [`16-web-search/`](16-web-search/) | 🚧 |
| **17** | Weekly digest of YouTube videos | [`17-youtube-digest/`](17-youtube-digest/) | 🚧 |

## Who it's for

- **Doctors, lawyers, teachers, accountants, freelancers** who keep seeing "AI agent" everywhere without knowing what it actually means
- **Junior developers** who want to understand Claude beyond chat
- People who tried n8n or Make and want to move to Python code
- The curious who aren't afraid to copy-paste 30 lines of Python
- **Experienced devs** who want a concise reference to share with junior colleagues

## Who it's NOT for

- LLM experts looking for advanced techniques (RAG, fine-tuning, etc.)
- People who want a turnkey solution without understanding anything
- Pure Python beginners who don't know how to install Python — start with the [official Python tutorial](https://docs.python.org/3/tutorial/index.html) first

## Prerequisites

For **Part 1** (tutorials 01-06):
- A Claude account (free tier is enough to start)
- No technical knowledge needed
- A text editor (any will do)

For **Parts 2-4** (tutorials 07+):
- Python 3.10+ installed
- An Anthropic account with an API key
- A terminal (macOS, Linux, or WSL on Windows)

## Languages

- 🇫🇷 **French** — original reference version, all 9 published tutorials complete
- 🇬🇧 **English** — all 9 published tutorials translated. New tutorials (10-17) will be written in both languages.
- 🇲🇦 **العربية** — planned starting month 5

## License

MIT — do what you want with this code, give feedback if it helped you.

## Contact

- GitHub: [@Kryscekk](https://github.com/Kryscekk)
- Dev.to: [@kryscekk](https://dev.to/kryscekk)
- LinkedIn: coming

---

<a id="français"></a>

# Agents en Pratique

> Apprendre à construire des agents IA avec Claude — de zéro à la production.

**Auteur** : Driss Amiroune — médecin urologue à Fès, architecte logiciel auto-formé.

🇬🇧 [Also available in English — click here](#agents-in-practice)

## Pourquoi ce repo

Il y a quelques mois, je ne savais pas ce qu'était une API. Aujourd'hui j'ai quatre systèmes qui tournent en production grâce à Claude — un pour gérer mon cabinet médical, un pour analyser la Bourse, un pour mes finances perso, et un pour ma veille IA personnalisée.

Ce repo, c'est ce que j'aurais voulu trouver au début. Pas un cours abstrait, pas une doc officielle aride, pas un tuto YouTube de 2h qui survole. **Le vrai parcours** : d'abord apprendre à *parler* à Claude (sans une ligne de code), puis seulement quand la méthode est solide, passer au Python et aux outils.

C'est l'ordre que j'ai réellement suivi pendant mes 6 premières semaines. Les autres tutoriels te font commencer par l'API. Moi, je commence par la **discipline de pensée**.

## Sommaire

✅ = publié  ·  🇬🇧 = version anglaise disponible  ·  🇫🇷 = français uniquement (traduction en cours)  ·  🚧 = en rédaction

### Partie 1 — Parler à Claude (sans une ligne de code)

| # | Tuto | Dossier | Statut |
|---|---|---|---|
| **01** | Comment parler à Claude pour qu'il te comprenne | [`01-talking-to-claude/`](01-talking-to-claude/) | ✅ 🇬🇧 🇫🇷 |
| **02** | Qu'est-ce qu'un agent IA, vraiment ? | [`02-what-is-an-agent/`](02-what-is-an-agent/) | ✅ 🇬🇧 🇫🇷 |
| **03** | Construire ton premier brief (un rôle Claude) | [`03-your-first-brief/`](03-your-first-brief/) | ✅ 🇬🇧 🇫🇷 |
| **04** | Un `CLAUDE.md` pour ton projet | [`04-claude-md/`](04-claude-md/) | ✅ 🇬🇧 🇫🇷 |
| **05** | Ton premier agent en chat (sans code) | [`05-first-agent-in-chat/`](05-first-agent-in-chat/) | ✅ 🇬🇧 🇫🇷 |
| **06** | Quand et pourquoi passer à l'API ? | [`06-moving-to-the-api/`](06-moving-to-the-api/) | ✅ 🇬🇧 🇫🇷 |

### Partie 2 — Construire des agents en Python

| # | Tuto | Dossier | Statut |
|---|---|---|---|
| **07** | Ton premier appel API Anthropic | [`07-first-api-call/`](07-first-api-call/) | ✅ 🇬🇧 🇫🇷 |
| **08** | **Les 4 piliers d'un agent solide** | [`08-the-4-pillars/`](08-the-4-pillars/) | ✅ 🇬🇧 🇫🇷 |

### Partie 3 — Donner des outils à Claude (MCP)

| # | Tuto | Dossier | Statut |
|---|---|---|---|
| **09** | Ton premier MCP server (4 outils utiles) | [`09-first-mcp-server/`](09-first-mcp-server/) | ✅ 🇬🇧 🇫🇷 |
| **10** | Faire tourner ton agent 24/7 avec systemd | [`10-systemd-for-your-agent/`](10-systemd-for-your-agent/) | 🚧 |
| **11** | Faire parler ton agent avec Telegram | [`11-telegram-bot/`](11-telegram-bot/) | 🚧 |

### Partie 4 — Patterns avancés

| # | Tuto | Dossier | Statut |
|---|---|---|---|
| **12** | Tracer le coût de chaque appel API | [`12-cost-tracker/`](12-cost-tracker/) | 🚧 |
| **13** | Fix "database is locked" en SQLite | [`13-sqlite-locked/`](13-sqlite-locked/) | 🚧 |
| **14** | Versionner `/etc/nginx` avec Git | [`14-nginx-in-git/`](14-nginx-in-git/) | 🚧 |
| **15** | Screenshot d'une URL depuis ton agent | [`15-url-screenshot/`](15-url-screenshot/) | 🚧 |
| **16** | Recherche web gratuite depuis ton agent | [`16-web-search/`](16-web-search/) | 🚧 |
| **17** | Digest hebdo de vidéos YouTube | [`17-youtube-digest/`](17-youtube-digest/) | 🚧 |

## Contact

- GitHub : [@Kryscekk](https://github.com/Kryscekk)
- Dev.to : [@kryscekk](https://dev.to/kryscekk)
- LinkedIn : à venir

## Licence

MIT — fais ce que tu veux avec ce code, donne-moi du feedback si ça t'a servi.
