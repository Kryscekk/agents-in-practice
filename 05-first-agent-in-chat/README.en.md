> 🇫🇷 **Lire en français** : [README.md](README.md)

# 05 — Your first agent in chat (no code)

**Difficulty**: 🟢 Beginner  |  **Time**: 30 min reading, 1h-2h practice

> You're going to build your first real agent — a Claude that plays a precise role, follows strict rules, produces a consistent format. Without a line of Python. Just a brief, a light CLAUDE.md, and the discipline of always starting your conversation the same way.

---

## Why this tutorial exists

When people hear "AI agent", they immediately imagine complex code, APIs, servers. That representation discourages anyone without a CS background. Yet **80% of an agent's value comes from method, not code**.

Before writing my first line of Python, I spent several weeks building agents in chat alone. I gave them a brief, a context, and worked with them. It's enough for many real cases — and it teaches you what matters before you tackle code you wouldn't know how to debug.

This tutorial takes you all the way through: an agent you'll **actually use**, not a theoretical exercise.

---

## What we're building

A chat agent that:
- Has a **clear role** (defined by your brief)
- Knows your **project context** (defined by your light CLAUDE.md)
- Produces **consistent** results at every use
- That you can summon in 30 seconds to do its job

We'll take a concrete end-to-end example: **a "client email triager" agent**. You'll adapt it to your trade afterwards.

---

## Prerequisites

- Have read and done tutorial **03 — Building your first brief**
- Have read and done tutorial **04 — A CLAUDE.md for your project**
- A Claude account (free is enough to start, but Pro/Max is much more comfortable for long sessions)
- 30 quiet minutes

---

## Step 1 — Pick a real task you'll actually use

This is the most important step, and the one most often skipped. If you pick a fake task to practice, you'll never use the agent and you'll learn nothing.

**Criteria for a good first task for a chat agent**:

1. You do it **at least once a week**
2. It takes **between 10 and 60 minutes** each time
3. The result always follows **more or less the same format**
4. You can describe it in **5 to 10 sentences**
5. **No irreversible decisions** (the agent can be wrong without breaking your life)

Examples by trade:

| Trade | Good first task |
|---|---|
| Doctor | Prepare a consultation report from raw notes |
| Lawyer | Summarize a court ruling in a precise format |
| Accountant | Categorize a bank statement against your chart of accounts |
| Teacher | Write a student evaluation sheet from notes |
| Marketer | Turn a long article into a LinkedIn post |
| Freelancer | Prepare a quote from a client brief |
| Manager | Synthesize your weekly 1:1 reports |

For the rest of this tutorial, we'll use the example **"triage my client emails"**. Concrete, frequent, consistent format. Adapt it to your own task.

---

## Step 2 — Write the brief

You already know the pattern (tutorial 03): Role / Fundamental principle / Rules / Process / Output format.

Here's the brief for our example:

```markdown
# Brief — Client-Email-Triager Agent

> Role: Read an email received from a client and categorize it according to
> my rules so I can handle each type efficiently.

## Fundamental principle

A mis-categorized email is worse than an uncategorized email. **If you
hesitate between two categories, mark "TO REVIEW" and explain your
hesitation in two lines — I'll decide.** NEVER guess.

## Rules

1. NEVER invent content absent from the email.
2. If the email contains several distinct subjects, categorize it under
   the main category but flag the others in notes.
3. Priority is measured by my business impact, not the client's tone.
4. A "spam" category exists and is handled differently (action = delete).
5. If the client explicitly asks to speak to me by phone, priority
   automatically goes up to HIGH.

## Process

### 1. Read the entire email
Never reply based on the subject alone. Read everything, including the
signature and mentioned attachments.

### 2. Identify the main category
- `QUOTE` — pricing request / commercial proposal
- `ORDER_FOLLOWUP` — question about an ongoing order
- `COMPLAINT` — problem with a delivered product or service
- `GENERAL_INFO` — informational question with no action requested
- `APPOINTMENT` — appointment request
- `SPAM` — promotional, automatic, unsolicited
- `TO_REVIEW` — can't decide, explain in two lines

### 3. Assess priority
- `HIGH`: client asks for a short deadline (<48h), serious complaint,
  client expresses dissatisfaction, mention of competition, explicit
  request to be called
- `MEDIUM`: quote or appointment request with no displayed urgency
- `LOW`: informational question, routine follow-up

### 4. Extract key elements
Requested date if applicable, amount if applicable, order reference,
contact name, client sentiment (positive/neutral/negative).

### 5. Suggest an action
A concrete action I can execute in 5 minutes.

## Output format

```
SUBJECT : [exact reuse of email subject]
FROM    : [name + email]

CATEGORY : [QUOTE | ORDER_FOLLOWUP | COMPLAINT | GENERAL_INFO | APPOINTMENT | SPAM | TO_REVIEW]
PRIORITY : [HIGH | MEDIUM | LOW]

CLIENT      : [name, company if applicable]
REFERENCE   : [order number, quote, etc. — or "none"]
SENTIMENT   : [positive | neutral | negative]

SUMMARY (2 lines):
[factual summary of the request]

SUGGESTED ACTION:
[one sentence, concrete action executable in <5 min]

NOTES (if applicable):
[other subjects mentioned, points of attention, hesitations]
```
```

This brief is ~70 lines. You can write it in 30 minutes using this structure as inspiration.

---

## Step 3 — Write a light CLAUDE.md

For a chat agent, you don't need the full `CLAUDE.md` from tutorial 04 (which serves for code projects). You need **2-3 sections only**:

```markdown
# Dr Amiroune Practice — Email context

## Activity
Urology medical practice in Fès. I receive emails from patients,
fellow doctors, suppliers (medical equipment, insurance, labs), and
lots of spam.

## Recurring clients/contacts
- Akdital Clinic (partner) — often insurance authorizations to validate
- Echo-Plus Labs (ultrasound equipment)
- Dr X's practice (colleague) — patient sharing
- FAR insurance — military dossier handling

## My business priorities
- Insurance pre-authorizations are top priority: any delay impacts the patient.
- New-patient appointments are top priority: never miss one.
- Medical-equipment emails can wait 48-72h.
- Spam: straight to trash.

## Sentiments to watch particularly
If a patient or insurer expresses frustration about a pre-authorization
delay, it's immediately HIGH.
```

This mini-context is ~25 lines. It complements your brief by giving Claude **the names, contacts, priorities** specific to your world.

---

## Step 4 — Build your usage routine

This is where many beginners go wrong. **An agent that works is an agent you use the same way every time.** You need to build a ritual.

Here's the ritual I recommend:

### a) Open a new Claude conversation

On claude.ai, click *"New chat"*. You start with a clean slate for this task.

### b) First message: paste the brief + the CLAUDE.md

In this first message, paste:

```
Here's my brief for the Client-Email-Triager agent, along with my project
context. Read everything in full, confirm you understood, and wait for my
emails to triage.

================================================================
BRIEF
================================================================
[the content of your brief]

================================================================
PROJECT CONTEXT
================================================================
[the content of your light CLAUDE.md]
```

Claude answers: *"Brief received, I'm ready. Send me the first email."*

### c) Send your emails one by one

Copy the email (subject + body + signature) and paste in chat. Claude answers in the expected format. You read, validate, or correct.

### d) When Claude is wrong, you improve the brief

If Claude classifies an email as `GENERAL_INFO` when it was a `QUOTE` in your view, **two options**:

1. **One-off**: you correct Claude in the conversation (*"no, this is a QUOTE because..."*). Claude learns for the rest of the conversation.
2. **Recurring**: you **modify the brief** on your disk. You add a rule or refine the definition of the category.

Option 2 is the key. **Your brief isn't frozen. It evolves with your usage.** After a few weeks, your brief becomes sharp on your real cases.

### e) Save your briefs

Save your briefs in a dedicated folder on your disk (e.g. `~/Documents/claude-briefs/`). Version with a dated filename: `brief_email_triage_v2_2026-05-15.md`. That way you can revert to a previous version if a modification caused a regression.

---

## Step 5 — Evaluate your agent

After **1 week of use** (so ten or so times), ask yourself 5 questions:

1. **Am I saving time?** How many minutes saved per use × how many uses per week?
2. **Is Claude still wrong on the same cases?** If yes, those cases aren't covered by your current brief.
3. **Am I copy-pasting the brief every time?** If yes, that's normal — it's exactly what automated code would do.
4. **Am I tempted to skip the brief?** If yes, that's a sign you're starting to internalize your own rules. Good sign.
5. **Is the output really usable?** Can you copy-paste it into your CRM, calendar, email?

**If 4 out of 5 answers are positive**, your agent is a success. You can move to the next tutorial and consider automating via the API.

**If you hesitate on several questions, DON'T attack the API.** Iterate on the brief until it's solid. Otherwise you'd build on sand.

---

## The limits of the chat agent

Let's be honest: the chat agent (level 2 from tutorial 02) has real limits:

- **You must be at your screen.** The agent doesn't run without you.
- **You copy-paste every time.** No integration with your email, CRM, calendar.
- **You have no systematic trace.** If you want to know how many emails you triaged last week, you have to count by hand.
- **Context is lost between conversations.** If you close the chat, you start over next time (unless you re-paste the brief).
- **Costs are barely visible.** You know how much Claude.ai costs per month, not how much each task costs precisely.

These limits **aren't defects**. They're normal at this level. And they tell you when to move to the next level — that's exactly the subject of tutorial 06.

---

## The classic trap: skipping this step

Many beginners want to jump straight to Python code because it feels "more serious". That's a mistake, for three reasons:

1. **You write code you wouldn't know how to debug.** If Claude (via API) outputs a mediocre result, you don't know if it's your prompt or your Python code that's failing. In chat, you see immediately.

2. **You pay for nothing.** Iterating 100 times on a brief in chat costs you a few euros on your Claude.ai subscription. Iterating 100 times via API costs you the per-call rate, **and** you have to redeploy your code each time.

3. **You get discouraged.** An agent that works is gratifying. Code that crashes every 10 minutes at the start is demoralizing. The chat phase is your "easy" phase, which gives you the quick wins you need to keep going.

**Stay in chat until you have stability.** You'll know when to move.

---

## Memorable recap

> 1. Pick a **real task** you do at least 1×/week.
> 2. Write the **brief** (tutorial 03) and a **mini-CLAUDE.md** (simplified tutorial 04).
> 3. Routine: **new conversation, paste brief + context, work, save**.
> 4. When Claude is wrong → **modify the brief**, not just the conversation.
> 5. Evaluate after a week. If it works, that's your first agent. Stay at this level until you have stability.

---

## Going further

- **Tutorial 06 — When and why to move to the API?**: the signals that tell you it's time to automate.
- **Tutorial 07 — First API call**: your first Python script that does the same thing as your chat agent.

---

[← Back to summary](../README.md)
