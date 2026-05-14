> ### 🤖 This repo is run by my AI.
> Tutorials, posts, code, profile — everything written and managed end-to-end by my AI, from my own production code and projects. My role: decide and validate. Its role: execute, autonomously. To my knowledge, no one publicly owns this position today. I do — deliberately.

---

**Language** :   🇬🇧 [English](#english)  ·  🇫🇷 [Français](#français)

---

<a id="english"></a>

# Agents in Practice

> Learn how to build AI agents with Claude — from zero to production.

**Author**: Driss Amiroune — urologist in Fès, Morocco. Self-taught software architect.

This repo was built first in French. **Tutorials are being translated to English progressively** — each tutorial shows its current language status in the table below. The full English version is expected by month 3.

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

✅ = published and readable  ·  🇬🇧 = English available  ·  🇫🇷 = French only (translation in progress)

### Part 1 — Talking to Claude (no code)

| # | Tutorial | Status |
|---|---|---|
| **01** | How to talk to Claude so he understands you | ✅ 🇫🇷 |
| **02** | What is an AI agent, really? | ✅ 🇫🇷 |
| **03** | Building your first brief (a Claude role) | ✅ 🇫🇷 |
| **04** | A `CLAUDE.md` for your project | ✅ 🇫🇷 |
| **05** | Your first agent in chat (no code) | ✅ 🇫🇷 |
| **06** | When and why to move to the API? | ✅ 🇫🇷 |

### Part 2 — Building agents in Python

| # | Tutorial | Status |
|---|---|---|
| **07** | Your first Anthropic API call | ✅ 🇫🇷 |
| **08** | **The 4 pillars of a production-grade agent** | ✅ 🇬🇧 🇫🇷 |

### Part 3 — Giving Claude tools (MCP)

| # | Tutorial | Status |
|---|---|---|
| **09** | Your first MCP server (4 useful tools) | ✅ 🇫🇷 |
| **10** | Running your agent 24/7 with systemd | 🚧 |
| **11** | Making your agent speak via Telegram | 🚧 |

### Part 4 — Advanced patterns

| # | Tutorial | Status |
|---|---|---|
| **12** | Tracing every API call cost | 🚧 |
| **13** | Fix "database is locked" in SQLite | 🚧 |
| **14** | Versioning `/etc/nginx` with Git | 🚧 |
| **15** | URL screenshots from your agent | 🚧 |
| **16** | Free web search from your agent | 🚧 |
| **17** | Weekly digest of YouTube videos | 🚧 |

## Who it's for

- **Doctors, lawyers, teachers, accountants, freelancers** who keep seeing "AI agent" everywhere without knowing concretely what it is
- **Junior developers** who want to understand Claude beyond chat
- People who tried n8n or Make and want to move to Python code
- The curious who aren't afraid to copy-paste 30 lines of Python
- **Experienced devs** who want a concise FR reference to share with junior colleagues

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

- 🇫🇷 **French** — primary, reference version
- 🇬🇧 **English** — translation in progress (priority: foundational tutorials 03, 04, 08, then the rest)
- 🇲🇦 **العربية** — planned starting month 5 once English is complete

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

Ce repo a été construit d'abord en français. **Les tutoriels sont traduits en anglais progressivement** — chaque tuto affiche son statut linguistique actuel dans le tableau ci-dessous.

## Pourquoi ce repo

Il y a quelques mois, je ne savais pas ce qu'était une API. Aujourd'hui j'ai quatre systèmes qui tournent en production grâce à Claude — un pour gérer mon cabinet médical, un pour analyser la Bourse, un pour mes finances perso, et un pour ma veille IA personnalisée.

Ce repo, c'est ce que j'aurais voulu trouver au début. Pas un cours abstrait, pas une doc officielle aride, pas un tuto YouTube de 2h qui survole. **Le vrai parcours** : d'abord apprendre à *parler* à Claude (sans une ligne de code), puis seulement quand la méthode est solide, passer au Python et aux outils.

C'est l'ordre que j'ai réellement suivi pendant mes 6 premières semaines. Les autres tutoriels te font commencer par l'API. Moi, je commence par la **discipline de pensée**.

## Ce que je fais déjà (et qui n'est pas open source)

- **~104 000 lignes de Python** en production, ajoutées en quelques mois
- **4 systèmes métier** orchestrés par Claude, sur **un seul serveur à moins de 5 €/mois**
- **4 serveurs MCP** en parallèle (cabinet médical, valuation boursière, finances, R&D)
- **Defense-in-depth** : 4 rôles Claude séparés avec garde-fous pour empêcher l'agent de toucher à la prod par accident
- **Charte méthodologique versionnée** sur 228 itérations, séparée du code, enforced par `AssertionError` citant les sections
- **Pipeline médical** d'assurance : OCR, extraction patient, assemblage PDF, notifications WhatsApp
- **Plateforme de valuation fondamentale** boursière : 7 archétypes × 68 paramètres, 319 tests verts
- **30 crons orchestrés**, supervision auto, audit log médico-légal par domaine
- **claude-agent-sdk** avec `@tool` + `can_use_tool` callback pour validation humaine en boucle

Aucun de ces systèmes n'est public — ils contiennent des données sensibles (patients, comptes). Mais **les patterns que j'ai construits en chemin finiront ici, en tutoriels**, au fur et à mesure qu'ils deviennent assez stables pour être pédagogiquement clairs.

## Sommaire

✅ = publié, lisible immédiatement  ·  🇬🇧 = version anglaise disponible  ·  🇫🇷 = français uniquement (traduction en cours)

### Partie 1 — Parler à Claude (sans une ligne de code)

| # | Tuto | Statut |
|---|---|---|
| **01** | Comment parler à Claude pour qu'il te comprenne | ✅ 🇫🇷 |
| **02** | Qu'est-ce qu'un agent IA, vraiment ? | ✅ 🇫🇷 |
| **03** | Construire ton premier brief (un rôle Claude) | ✅ 🇫🇷 |
| **04** | Un `CLAUDE.md` pour ton projet | ✅ 🇫🇷 |
| **05** | Ton premier agent en chat (sans code) | ✅ 🇫🇷 |
| **06** | Quand et pourquoi passer à l'API ? | ✅ 🇫🇷 |

### Partie 2 — Construire des agents en Python

| # | Tuto | Statut |
|---|---|---|
| **07** | Ton premier appel API Anthropic | ✅ 🇫🇷 |
| **08** | **Les 4 piliers d'un agent solide** | ✅ 🇬🇧 🇫🇷 |

### Partie 3 — Donner des outils à Claude (MCP)

| # | Tuto | Statut |
|---|---|---|
| **09** | Ton premier MCP server (4 outils utiles) | ✅ 🇫🇷 |
| **10** | Faire tourner ton agent 24/7 avec systemd | 🚧 |
| **11** | Faire parler ton agent avec Telegram | 🚧 |

### Partie 4 — Patterns avancés

| # | Tuto | Statut |
|---|---|---|
| **12** | Tracer le coût de chaque appel API | 🚧 |
| **13** | Fix "database is locked" en SQLite | 🚧 |
| **14** | Versionner `/etc/nginx` avec Git | 🚧 |
| **15** | Screenshot d'une URL depuis ton agent | 🚧 |
| **16** | Recherche web gratuite depuis ton agent | 🚧 |
| **17** | Digest hebdo de vidéos YouTube | 🚧 |

## À qui ça s'adresse

- Aux **médecins, juristes, profs, comptables, indépendants** qui voient passer "agent IA" partout sans savoir ce que c'est concrètement
- Aux **développeurs juniors** qui veulent comprendre Claude au-delà du chat
- Aux gens qui ont essayé n8n ou Make et qui veulent passer à du code Python
- Aux curieux qui n'ont pas peur de copier-coller 30 lignes de Python
- Aux **devs expérimentés** qui veulent une référence FR concise à partager à des collègues débutants

## À qui ça ne s'adresse PAS

- Aux experts en LLM qui cherchent des techniques avancées (retrieval-augmented generation, fine-tuning, etc.)
- Aux gens qui veulent une solution clé-en-main sans rien comprendre
- Aux purs débutants Python qui ne savent pas installer Python — commence par [le tuto officiel Python](https://docs.python.org/fr/3/tutorial/index.html) d'abord

## Pré-requis communs

Pour la **Partie 1** (tutos 01-06) :
- Un compte Claude (gratuit suffit pour démarrer)
- Aucune connaissance technique
- Un éditeur de texte (n'importe lequel)

Pour les **Parties 2-4** (tutos 07+) :
- Python 3.10+ installé
- Un compte Anthropic avec une clé API
- Un terminal (macOS, Linux, ou WSL sur Windows)

## Langues

- 🇫🇷 **Français** — langue principale, version de référence
- 🇬🇧 **English** — traduction en cours (priorité : 03, 04, 08 puis le reste)
- 🇲🇦 **العربية** — prévue à partir du mois 5 une fois l'anglais terminé

## Licence

MIT — fais ce que tu veux avec ce code, donne-moi du feedback si ça t'a servi.

## Contact

- GitHub : [@Kryscekk](https://github.com/Kryscekk)
- Dev.to : [@kryscekk](https://dev.to/kryscekk)
- LinkedIn : à venir
