> 🇫🇷 **Lire en français** : [README.md](README.md)

# 06 — When and why to move to the API?

**Difficulty**: 🟢 Beginner  |  **Time**: 15 min reading

> You have a chat agent that works. The question now isn't *"how to make it better?"* — it's *"is this the right time to automate?"*. This tutorial gives you the seven signals that answer this question, and prepares you for the most structuring decision of your journey.

---

## Why this tutorial exists

I've seen too many people (myself included) move to the API too early. The result is always the same: you end up debugging Python code for a case you barely mastered in chat. You lose a week fixing technical problems that wouldn't have existed if you'd stayed in chat.

Conversely, I've seen people stay in chat **too long** while their cases clearly deserved automation. They keep manually copy-pasting their briefs twice a day, and overall lose more time than the API would save them.

This tutorial gives you the **seven concrete signals** that tell you it's the right time. If you tick 4 or more, go. If you tick 2 or fewer, wait.

---

## The seven signals that say "move to the API"

### Signal 1 — You do the same task every day, manually

If you find yourself copy-pasting your brief, re-pasting an email, waiting for the answer, executing the suggested action — **several times a day, every day** — it's mechanical. Code can do that thing for you.

Test: *"This week, how many times did I do this task manually?"*. If the answer is **more than 5 times**, signal ticked.

### Signal 2 — You want it to run while you sleep (or consult, or eat)

Some tasks are **triggered by events**: an email arrives, a file appears, an hour strikes, a data point changes. If you wait for these events to happen to handle them by hand, you **miss** the event when you're not at your screen.

Typical example: a document scan that arrives on your server at 2pm during your afternoon consultation. You'll see it at 7pm, process at 8pm, send at 9pm. If it were automatic, it'd be done at 2:01pm, and the client would have their answer 6 hours earlier.

Test: *"Does my human processing latency cost me something?"*. If yes (clients waiting, missed opportunities, irritation from counterparts), signal ticked.

### Signal 3 — You want to integrate with another system

You want the result of your agent to **land directly** in your CRM, calendar, database, project management tool, WhatsApp bot. **You don't want to copy-paste anymore.**

In chat, you copy-paste by hand. In code, you write the connection once and it's done forever.

Test: *"Am I dreaming of a magic button that would take Claude's output and send it directly elsewhere?"*. If yes, signal ticked.

### Signal 4 — You want to track costs precisely

In chat (Claude.ai subscription), you pay a flat fee. You don't know how much each task really costs. For personal use, that's OK.

The moment you want to **sell** your agent to clients, **measure the profitability** of a workflow, **optimize** the cost/quality ratio (Haiku vs Sonnet vs Opus), you need code. The API gives you a precise cost for each call — input, output, model. You can log all of this (and that's exactly tutorial 12 on the cost tracker).

Test: *"Is someone other than me going to use this agent, or do I want to know precisely how much it costs me?"*. If yes, signal ticked.

### Signal 5 — You want to version your method (for real)

In chat, you have a folder with your briefs in `.md`. If you modify a brief by mistake, you lose the previous version (unless you do your backups by hand, which nobody really does).

In code, you put your briefs in a Git repo. Each modification is tracked, each version is recoverable, you can branch out to experiment without breaking your working version.

Test: *"Is my current brief an asset I don't want to lose?"*. If yes, signal ticked.

### Signal 6 — You already write code (even a little)

If you've already tinkered with Python (even 100 lines), if you know what a terminal is, if you've already installed a library with `pip`, **moving to the API will cost you a few days, not a few weeks**.

If you've **never** touched code, the investment is heavier — but not insurmountable. Tutorial 07 is designed so a complete beginner can get there.

Test: *"Am I capable of opening a terminal and typing `python3 --version` without panicking?"*. If yes, signal ticked.

### Signal 7 — Your brief has been stable for at least 2 weeks

The worst would be to code an agent and have to refactor your code every time you change a rule. Before moving to the API, your brief must be **stable**. Not frozen forever — but not changing every 48 hours either.

Test: *"Over the last 2 weeks, how many times did I substantially modify my brief?"*. If the answer is **0 or 1**, signal ticked. If it's **3+**, your brief isn't ready.

---

## The score

- **5 to 7 signals ticked** → move to the API. Tutorial 07 now.
- **3 to 4 signals ticked** → borderline. If you have time and you're technically comfortable, go. Otherwise, stay in chat a bit longer.
- **0 to 2 signals ticked** → stay in chat. Strengthen your brief, broaden your covered cases, measure what works. Come back to this tutorial in 2-3 weeks.

---

## What you gain by moving to the API

### Time autonomy
The agent runs while you sleep. It handles what comes in. You wake up with the work done.

### Integration
The agent sends results directly where you want: your database, your CRM, your Telegram/WhatsApp bot, your dashboard.

### Cost precision
Every API call is logged: model, input tokens, output tokens, exact cost in dollars. You can optimize your API budget.

### Versioning and reproducibility
Your code and your briefs live in a Git repo. You can roll back, compare, share.

### Composition
You can have **several agents that collaborate**. The first classifies a document, the second extracts it, the third stores it in the database, the fourth notifies the client. That's the subject of Parts 3 and 4 of the repo.

### Automated tests
You can write tests that spend your whole day checking your agents respond correctly on known cases. If a model update changes a behavior, you know immediately.

---

## What you lose (and need to know)

### The beauty of the chat interface
Claude.ai has a very well-made interface. The history, formatting, artifacts, conversation search. The API gives you raw. If you want a nice UI, you must build it yourself (or use third-party tools).

### The flat-rate convenience
Claude.ai Pro at $20/month is practically unlimited use for most people. The API is billed by usage. For small volume, you'll pay less. For high volume, you'll potentially pay more, but with measurable and optimizable cost.

### Startup simplicity
In chat, you copy-paste and go. In code, you install Python, get an API key, write your first `requirements.txt`, debug your first `import`. **It's a real step** — but only one, after which everything becomes more fluid.

### Hands-on evaluation
In chat, you immediately see if the answer is good or bad. You can say *"redo shorter"* and adjust. In code, you must build tools to evaluate the quality of your outputs (logs, metrics, reference examples). It's real work but necessary — and it's exactly the subject of the "Observability" pillar from tutorial 08.

---

## Prerequisites for tutorial 07

If you decide to move to the API, check that you have:

### On the software side
- **Python 3.10 or newer** installed on your machine (`python3 --version` must show 3.10+)
- **pip** installed (comes with Python normally)
- **A proper text editor**: VS Code, Sublime, or even a simple editor — not Word

### On the account side
- **An Anthropic account** at [console.anthropic.com](https://console.anthropic.com) (free)
- **An API key** created from this account (5 free credits offered to start, then you add your card)
- **A few dollars of credit** to launch your first calls ($5 credit gives you thousands of calls with Haiku)

### On the knowledge side
- You did tutorial 05 and you have a working chat agent
- You know how to open a terminal (Mac: Terminal, Windows: PowerShell or WSL, Linux: you already know)
- You know what a `.py` file and a `.env` file are

If one box is unchecked, take 30 minutes to fill it before tackling tutorial 07.

---

## The bad reasoning to avoid

> *"I'll move to the API because it's more pro."*

Not the right criterion. You'll move because **the seven signals** tell you it's the right time. Not because it sounds more serious on LinkedIn.

> *"I'll move to the API because in chat I have to copy-paste."*

If that's your only criterion, maybe you can automate **just the copy-paste** with a keyboard shortcut or a simple script, and keep using Claude.ai. The API is a heavier decision than reducing a copy-paste.

> *"I'll move to the API because everyone's doing it."*

The other trap. Nobody knows how many people use Claude **only** in chat and are very happy with it. You owe nothing to fashion.

---

## The good reasoning

Your chat agent saves you time. You've quantified how much. You sense there's an extra step you could climb **for a reasonable investment**. You want to. You have the prerequisites.

**So you go.**

That's what we do in the next tutorial.

---

## Memorable recap

> Seven signals: **daily task**, **events during your absence**, **integration with other tools**, **cost tracking**, **method versioning**, **comfortable with code**, **brief stable for 2 weeks**. 5 ticked or more → tutorial 07. 2 or fewer → stay in chat and come back in 3 weeks.

---

## Going further

- **Tutorial 07 — First Anthropic API call**: your first Python script that does the same job as your chat agent.
- **Tutorial 08 — The 4 pillars of a solid agent**: to read in parallel with your first developments. It's the manifesto that distinguishes a throwaway agent from one that holds in production.

---

[← Back to summary](../README.md)
