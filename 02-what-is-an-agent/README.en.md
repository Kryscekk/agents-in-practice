> 🇫🇷 **Lire en français** : [README.md](README.md)

# 02 — What is an AI agent, really?

**Difficulty**: 🟢 Beginner  |  **Time**: 20 min reading

> The word "agent" is used for everything and its opposite. A chatbot, an assistant, a no-code workflow, a Python script calling an API — all of these are currently called "AI agents". This tutorial cuts through the noise and gives you a precise, usable definition.

---

## Why this tutorial exists

When I started, I saw the word "AI agent" everywhere. On LinkedIn, in ads, in YouTube videos. No one ever defined what it concretely meant.

After a few weeks, I understood that **the same word covers four different realities**, and that this confusion is what makes beginners not know where to start. If I tell you *"build an agent"* and you think of one thing while I think of another, we lose time.

This tutorial cleans this up. With concrete examples, so you know **where you want to go**.

---

## Four levels people call "agent"

### Level 1 — The chatbot

You ask a question, the system answers. Once. No memory across sessions, no clear role, no objective.

**Examples**: Claude on claude.ai without specific context. ChatGPT for a one-off question. The support widget on a site that answers FAQs.

**Characteristic**: it's *transactional*. Question → answer. End.

It's useful, but **it's not really an agent**. It's a correspondent you ask questions to.

### Level 2 — The role-based agent (structured chat)

You give Claude a **precise role** with rules and a format. It no longer answers as a generalist, it answers in its role.

**Concrete example**: you paste to Claude a text saying *"You are the assistant for writing my medical CRs. Here are your rules..."*. From there, in the conversation, it plays that role. You give it your raw notes, it outputs a CR formatted according to your rules. You don't re-explain how to do it — you give it the raw material and it applies.

**Characteristic**: it's *contextual*. The role persists throughout the conversation. You don't have to re-explain.

**This is already an agent**, in the useful sense of the word. And **you can build it today, without a single line of code**. That's exactly the subject of tutorials 03, 04, and 05 in this repo.

### Level 3 — The automated agent (code + API)

You turn the role into **Python code that runs on its own**. No need to open a conversation, copy-paste, wait. The code takes an input (a PDF arriving, a clock ticking, a message received), calls Claude via the API, processes the output, and moves on.

**Concrete example**: a script that watches a `/incoming/` folder. As soon as a PDF arrives, it OCRs it, asks Claude to identify the document type, classifies the file, updates a database, and notifies on WhatsApp. All without human intervention.

**Characteristic**: it's *autonomous*. The agent runs while you do something else or sleep.

**This is the goal of Parts 2 and 3 of this repo** (tutorials 07 to 11). That's what we build with Python + the Anthropic API + possibly an MCP server.

### Level 4 — The multi-tool agent making complex decisions

The automated agent becomes **an agent that decides**. We give it a toolbox (read files, query a database, send messages, run code), and it chooses by itself which tools to use, in what order, to reach a goal.

**Concrete example**: you tell the agent *"give me the morning brief"*. The agent decides on its own to call your server-logs reader tool, then your calendar reader tool, then your API-costs calculator tool, then formulates a coherent summary.

**Characteristic**: it's *agentic* in the strong sense. The agent chooses the path, not you.

**This is the horizon of Part 4 and beyond** in this repo.

---

## Why this progression makes sense

Many beginners want to start **directly at level 4**. It's tempting — that's what we see in LinkedIn demos. But it's almost always a mistake, for three reasons:

### Reason 1 — You don't yet know what you want

At level 4, the agent decides. You still need to **know precisely what to decide**. If you haven't formulated your rules, criteria, constraints (level 2), the agent makes random decisions and you have no idea why.

### Reason 2 — You can't diagnose what's failing

When a multi-tool automated agent breaks, you have **ten possible sources**: poorly written prompt, crashing tool, corrupted data, hallucinating model, broken code, API timeout, misbehaving database, etc. If you've never mastered level 2, you don't have the reflex to formulate the right hypothesis.

### Reason 3 — You build fragility

An agent running on its own (level 3 or 4) **must** respect the 4 pillars of robustness (observability, reliability, security, deployment — that's tutorial 08 of the repo). If you start directly at level 3 without understanding these pillars, you're building something that works in demo and silently breaks the day you're not in front of your screen.

---

## The right progression — the one I actually followed

```
Level 1  →  Level 2  →  Level 3  →  Level 4
chatbot      structured       code agent       multi-tool agent
             role             (Python+API)     (MCP/tools)
                ↓                  ↓                   ↓
            (tutorials 03-05)  (tutorials 06-12)   (tutorial 09 and beyond)
            no code            with Python         with MCP/tools
```

**Level 1 → Level 2**: you learn to formalize a role. That's what you do with a brief + a CLAUDE.md (tutorials 03 and 04). **You can do it today, in chat, without installing anything.**

**Level 2 → Level 3**: when your role is stable and you catch yourself reusing it daily, you move it to code. That's the move to the API (tutorials 06 and 07). You write your first Python script that does the same thing you were doing in chat — but automatically.

**Level 3 → Level 4**: when your code runs well and you want the agent to make complex decisions, you give it tools via MCP (tutorial 09). There, you become an agent orchestrator — not just an executor.

---

## Concretely, what do we call an "agent" in this repo?

In all tutorials of this repo, when I say "agent", I mean **at minimum a level 2**: Claude with a structured role, rules, expected output format. Not a generalist chatbot.

Starting from **Part 2** (tutorial 07), "agents" are level 3: Python code running on its own. That's what developers often call "agent" without specifying.

Starting from **Part 3** (tutorial 09), agents can **use tools**: MCP servers, HTTP calls, database access. That's the emerging level 4.

---

## False friends and confusions to avoid

### "ChatGPT is an agent"
No. It's a chatbot (level 1) on which you can build an agent (level 2+). OpenAI's custom instructions system lets you reach level 2 without code — it's the equivalent of a brief.

### "Any LLM called in a loop is an agent"
Not necessarily. If you put Claude in a loop that asks the same thing 100 times, that's **a script that calls Claude 100 times**, not an agent. A useful agent is a loop where the LLM **decides** something that influences the next iteration.

### "Without MCP, it's not an agent"
False. You can have an excellent level-3 agent without MCP, just with the API and Python code. MCP is useful when you want Claude to drive your environment (read files, query a database, run commands) **without you having to code each interaction**.

### "An n8n/Make workflow is an agent"
It's a level 2-3 agent depending on complexity. No-code tools let you automate, but they have limits: less fine control over the prompt, limited traceability, often higher cost than a Python script. For simple cases, it's fine. For serious production, code takes the lead.

---

## The question to ask yourself for your first agent

Before getting started, answer honestly:

1. **What level do I want to reach?** (be honest: most useful cases stop at level 2 or 3)
2. **How much time can I invest?** (level 2: a few hours. Level 3: a few days. Level 4: a few weeks.)
3. **What concrete case do I want to solve?** (not "an AI agent in general". A specific case: *"automate my consultation reports"*, *"sort my client emails by category"*, *"generate a weekly report from my data"*.)

If you have these three clear answers, you know which tutorial to start with.

If you don't yet have an answer, **start with tutorial 03**. Pick any task you do regularly and that frustrates you, and formalize it into a brief. You'll learn a lot, with no risk, no cost.

---

## Memorable recap

> Four levels: **chatbot** (generic, no role), **role-based agent** (Claude with a brief, in chat), **automated agent** (Python code calling the API), **multi-tool agent** (the agent chooses its tools). In this repo, "agent" = level 2 minimum. You progress in order — skipping level 2 without mastering it builds fragility.

---

## Going further

- **Tutorial 03 — Building your first brief**: reach level 2 concretely, no code
- **Tutorial 06 — When and why to move to the API?**: the right moment to reach level 3

---

[← Back to summary](../README.md)
