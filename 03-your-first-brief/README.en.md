> 🇫🇷 **Lire en français** : [README.md](README.md)

# 03 — Building your first brief

**Difficulty**: 🟢 Beginner  |  **Time**: 30 min reading, 1h practice

> Before code, before the API, before tools: **the brief**. A markdown file that defines how Claude should think for a specific task. It's the most powerful and most forgotten invention in my method.

---

## Why this tutorial exists

If you've been using Claude for a while, you've probably had this frustration: you ask the same thing twice, a month apart, and you get **completely different** answers. Not because Claude is fickle — because **you** gave him different context each time.

I had this frustration so many times on my stock analysis work that I ended up writing a file. A markdown file that tells Claude *"this is how you should think, these are your rules, this is what you must produce as output"*. I called it a **brief**.

When I start a work session, I paste this brief in as the first message. Claude takes its role. All my briefs follow the same structure, and it has become my best tool — long before code, long before the API.

Today I have 7 briefs in production on one of my projects (one per "agent": extractor, classifier, valuator, validator, etc.), and dozens of one-off briefs I use when I need them.

---

## What is a brief?

A brief is **a document that defines a role for Claude**. With:

- **a clear role** (what do you have to do?)
- **a fundamental principle** (the absolute golden rule)
- **rules** (what we do, what we don't)
- **a process** (the steps to follow, in order)
- **an output format** (what a good answer looks like)

It's the same logic as a client brief at an agency or a job description: you frame what you expect so as not to fall into vagueness.

**What a brief is NOT**:
- A long API manual
- A 5-word magical prompt
- A description of Claude itself

It's a **business role** that Claude is going to take on.

---

## The standard brief structure

Here's the structure I use in every one of my briefs, without exception:

```markdown
# Brief — Agent X

> Role: (ONE sentence saying what you must do)
> File: (optional — which code file implements this, if applicable)

## Fundamental principle

(The absolute golden rule. One to three sentences. The idea that prevails over everything.)

## Rules

1. (First non-negotiable rule)
2. (Second rule)
3. (...)

## Process

### 1. (First step)
Description of what you do at this step.

### 2. (Second step)
...

## Output format

(Precise description of what you must produce. With an example if possible.)
```

Five sections, always in this order. It's short (often 50-150 lines) and readable in one glance.

---

## Why this structure works

### "Role" — the identity
One sentence. *"You are the agent that extracts financial data from PDFs."* That's what lets Claude position itself. Not three paragraphs — one sentence.

### "Fundamental principle" — the rule that overrides others
This is the sentence Claude must keep in mind if it forgets everything else. Example from my real extraction brief:

> *"The PDF is an official primary source — same reliability as a database value. If the PDF gives a figure directly, use it as-is. Do not recompute it."*

It's one sentence, but it prevents 80% of the errors I was seeing before. The fundamental principle is your **keystone**.

### "Rules" — the non-negotiables
Numbered list, short sentences, imperative or prohibition forms. Example:

```markdown
1. Always read the full file BEFORE answering.
2. If a figure is ambiguous, DO NOT guess — ask for confirmation.
3. NEVER invent a missing data point.
4. One source of truth per section, explicitly cited.
```

The capitals on **NEVER** and **BEFORE** are not shouting: they're visual markers that help Claude (and you on review) see what's not up for discussion.

### "Process" — the ordered steps
Not a flat list, a **sequence**. *"First 1, then 2, then 3."* If you can number them, number them.

```markdown
### 1. Identify the document period

Look for in the PDF: annual, H1, Q1/Q2/Q3/Q4. Criteria:
- "Annual report" → annual
- "H1 results release" → H1
- "Q1 release" → Q1

### 2. Read the structured data

Prioritize summary statements (income statement) over press releases.
In case of divergence, audited figures prevail.

### 3. Compute what's missing

If EPS not shown: EPS = NPAT × 1000 / NbShares.

### 4. Save to database
...
```

Claude executes better when it knows *where it is* in the sequence.

### "Output format" — the concrete example
The most forgotten section by beginners. You must show Claude **what a good answer looks like**.

Bad output format: *"Give me a structured summary."*

Good output format:

```markdown
## Output format

```
Ticker: ATW
Period: annual 2025
Source: atw_annual_report_2025.pdf

EPS      : 49.48 MAD/share
DPS      : 22.00 MAD/share
NPAT     : 10,643 MMAD
NbShares : 215,140 K shares

Notes: (free text, max 3 lines)
```
```

Claude sees the exact template, conforms to it. No need to repeat in chat *"give me a summary with these fields"* — it's in the brief.

---

## A complete, anonymized example

Here's a brief I use for an assistant that helps me prepare medical consultation reports. **Anonymized and simplified** for this tutorial:

```markdown
# Brief — CR Assistant (consultation report)

> Role: Write a consultation report from my raw notes.

## Fundamental principle

The report must **exactly reflect** what I wrote, without adding anything, without inventing anything, without extrapolating a pathology absent from my notes. If information is missing, the report says "not specified" — it doesn't guess.

## Rules

1. NEVER invent a diagnosis, medication, or additional examination.
2. NEVER assume a comorbidity or history absent from the notes.
3. If an abbreviation is ambiguous, ask before translating it.
4. Always preserve chronology: complaint → exam → diag → plan.
5. The language is neutral medical French. No specialist jargon if the recipient is a generalist.

## Process

### 1. Read my notes in full

Before writing the first line, read ALL the notes I gave you. Spot the main elements: reason for consultation, clinical exam, conclusion, plan.

### 2. Identify missing elements

If a standard CR section doesn't appear in my notes (e.g. no biological exam mentioned), you mark "not specified" — you don't invent.

### 3. Structure in the standard order

1. Identity (from the header I give you)
2. Reason for consultation (one sentence)
3. History (only mentioned items)
4. Clinical exam
5. Additional exams (results if present)
6. Conclusion / Diagnosis
7. Plan
8. Next appointment

### 4. Write while respecting the tone

Short sentences, active voice, medical but not specialist vocabulary, no personal opinion.

## Output format

```
CONSULTATION REPORT

Patient: [Last name First name]
Date   : [DD/MM/YYYY]

Reason:
[one sentence]

History:
- [bullet list, "none" if empty]

Clinical exam:
[paragraph]

Additional exams:
[paragraph or "not specified"]

Conclusion:
[1-2 sentences]

Plan:
1. [...]
2. [...]

Next appointment:
[date or "to be scheduled"]
```

No signature, no stamp — I handle that myself on printing.
```

This brief is **~60 lines**. I paste it at the start of each session, give it my notes, get a coherent CR every time.

**Compare with**: *"Claude, give me a report from these notes."* See the difference?

---

## How to build **your first brief**

Pick a task you do often with Claude where you're not satisfied with the current result. Examples by job:

| Job | Typical task |
|---|---|
| Lawyer | Summarize a case-law decision in a precise format |
| Accountant | Categorize bank transactions according to your chart of accounts |
| Teacher | Prepare a course sheet from an official program |
| Marketer | Write a LinkedIn post in your company's tone |
| Dev | Review a PR according to precise rules (security, perf, conventions) |
| Doctor | Prepare a referral letter to a colleague |

Now follow these 5 steps (~30 minutes total):

### Step 1 — Note your current frustration (5 min)

Answer in writing: *"What is wrong with Claude's current answers on this task?"*

Be concrete. Not *"it's not good"*. Rather *"it forgets to mention the decision date"* or *"it uses too much jargon for my clients"*.

### Step 2 — Write the fundamental principle (5 min)

One to three sentences. **The principle that must override all rules.**

Examples:
- *"The summary must be max 200 words and include the date, jurisdiction, and ruling."*
- *"NEVER categorize a transaction without certainty. Prefer 'to classify manually' over an error."*

### Step 3 — List your rules (10 min)

5 to 10 rules max, numbered, imperative or prohibition. **Don't exceed 10.** Beyond that, Claude starts forgetting the first ones.

### Step 4 — Describe the process (5 min)

3 to 6 steps. *First, then, next...*

### Step 5 — Give an output example (5 min)

This is the most powerful step. Put a **precise example** in the brief of what you expect as an answer. Not an abstract description — a real example, in a code block.

---

## How to use your brief

Save it as a `brief_xxx.md` file somewhere in your documents.

At the start of a new Claude conversation, copy-paste the content as the first message, with an intro sentence:

> *"Here is the brief for agent X. Read it in full, confirm you understood it, and wait for my instructions."*

Claude answers: *"Brief received, I'm ready to...".* From this moment, its answers follow the rules, the process, and the output format.

If you notice a rule is poorly worded or a case is missing — modify the brief on your disk. The brief is **living**: it evolves with your practice.

---

## Common pitfalls

### Pitfall 1 — The 5-line brief
*"You are a legal expert. Answer well."* That's a prompt, not a brief. If you can't write 30 lines, it means you don't yet know precisely what you want. Think first.

### Pitfall 2 — The encyclopedic brief
500 lines. Claude will read the start and the end, forget the middle. **Stay under 200 lines.** If you need more, you have several distinct roles — make several briefs.

### Pitfall 3 — Contradictory rules
*"Be concise"* + *"Detail each point thoroughly"*. Claude will choose as best it can, and you'll be frustrated. Read your rules out loud and look for contradictions.

### Pitfall 4 — No output format
Without an explicit template, Claude improvises. Always include a concrete example of the expected output.

### Pitfall 5 — The theoretical brief
You describe concepts instead of instructions. Bad: *"Rigor is important."* Good: *"Cite the source of each figure, format `[source: page X]`."*

---

## Going further

- **Tutorial 04 — A CLAUDE.md for your project** (🇬🇧 [README.en.md](../04-claude-md/README.en.md) when available): extends the brief to the whole project, so Claude knows your technical context without re-explanation each session.
- **Tutorial 05 — Your first agent in chat (no code)**: combines a brief + a CLAUDE.md to make a real usable agent, without a single line of Python.

---

## Memorable recap

> Five sections, in this order: **Role** (1 sentence), **Fundamental principle** (1-3 sentences), **Rules** (5-10 numbered), **Process** (3-6 steps), **Output format** (with concrete example). Under 200 lines. Living.

---

[← Back to summary](../README.md)
