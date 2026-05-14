> 🇫🇷 **Lire en français** : [README.md](README.md)

# 01 — How to talk to Claude so he understands you

**Difficulty**: 🟢 Beginner  |  **Time**: 20 min reading, 30 min practice

> The hardest thing with Claude isn't that he's incapable. It's that he makes silent assumptions about what you want. This tutorial gives you the five levers to make him stop assuming and do, exactly, what you need.

---

## Why this tutorial exists

At the start, I used Claude like a better Google. I typed a question, copied the answer, moved on. It worked for simple questions. For real work tasks, it was unpredictable.

One day I ask him to summarize a hospital discharge report. He gives me a summary. Next time, same kind of document, same question — he gives me a **completely different** summary, with sections I never asked for, leaving out what I actually needed.

I realized at that moment it wasn't Claude being fickle. It was me talking to him badly. I was handing him a text and the word *"summarize"*, expecting him to guess what *"summary"* meant to me at that specific moment.

This tutorial is what I wish I'd read that day.

---

## The problem, stated clearly

When you ask Claude a question, your brain **silently** provides lots of information that isn't in your message:

- *What's the context?* (who you are, why you're asking, what you'll do with it)
- *What are the constraints?* (length, tone, vocabulary, things to avoid)
- *What does a good answer look like?* (format, structure, example)
- *What are your hidden preferences?* (yes but not like that, yes but short, etc.)

Claude doesn't read your mind. If you don't give him this information, he invents it — and he invents **differently each time**. That's what creates the impression of inconsistency.

The solution: explicitly give him what your brain thinks is "obvious". Five main levers.

---

## Lever 1 — Give context

Not an encyclopedia. Just **three things**:

1. **Who you are** (or who you're writing for) — doctor, teacher, accountant, student, etc.
2. **Why you're asking** — a concrete case, not a theoretical exercise
3. **What you'll do with it** — print it, send it to a client, post it online

### Without context
> *"Explain VAT to me."*

Claude will give you a general lecture. You'll skim it and remember nothing.

### With context
> *"I'm an accountant and I need to explain how VAT works to a shopkeeper who's just started his sole-trader business in France. He has zero tax knowledge. Give me an explanation in plain language, with a worked example on a €100 product."*

The answer becomes useful, targeted, and you can copy it straight to your client.

---

## Lever 2 — Set the constraints

Without constraints, Claude averages out. An average answer for an average use. You don't want average — you want what serves you.

Typical constraints to give explicitly:

- **Length**: *"In 100 words maximum"* / *"In 3 paragraphs"* / *"In one A4 page"*
- **Tone**: *"Warm tone for a loyal client"* / *"Neutral administrative tone"* / *"Pedagogical tone for a beginner"*
- **Vocabulary**: *"Avoid jargon"* / *"High-school level"* / *"No medical jargon"*
- **What to avoid**: *"No bullet points"* / *"Don't include the conclusion"* / *"No mention of the competition"*

The more you set, the more predictable the answer becomes. **Inconsistency in answers almost always comes from absent constraints.**

---

## Lever 3 — Show an example

This is **the most powerful lever**, and the one beginners forget the most.

Instead of describing what you want, **show an example** of what you want.

### Abstract description
> *"Give me a structured summary of the document."*

Too vague. "Structured" means a thousand things. You'll get a random result.

### With concrete example
> *"Give me a summary of the document in this format:*
>
> ```
> ## Subject
> [one sentence]
>
> ## Main facts
> - [fact 1]
> - [fact 2]
> - [fact 3]
>
> ## Conclusion
> [two sentences maximum]
> ```
> *"*

Claude sees the template, he fills it. You know exactly what to expect.

This technique is so powerful that it's the foundation of **Tutorial 03: Building your first brief**.

---

## Lever 4 — Ask for step-by-step reasoning

When the task is complex (analysis, decision, comparison), ask Claude to **think before answering**, not just to produce a result.

### Without explicit reasoning
> *"Which is the best supplier between A, B, and C?"*

You get a quick answer that may be superficial.

### With step-by-step reasoning
> *"Which is the best supplier between A, B, and C, for my case (10 orders/month, delivery in Morocco, tight budget)?*
>
> *Think step by step:*
> *1. Which criteria matter for my case?*
> *2. How does each supplier rank on each criterion?*
> *3. What's your verdict, with two sentences of justification?*
> *"*

Claude takes the time to structure, you see his logic, you can correct him if you disagree with the reasoning.

---

## Lever 5 — Iterate, don't restart

When the answer isn't quite what you wanted, **don't close the conversation to reopen it**. Stay in the same conversation and correct:

- *"Redo it shorter."*
- *"Keep the structure but change the tone, I'm writing to a client not a colleague."*
- *"Good, except point 3 which is wrong. Here's the right info: XYZ. Redo it including that."*

Claude remembers the conversation and adjusts. You build your answer layer by layer.

**Only start from scratch if you change the subject entirely.** Otherwise, you lose your hard-won context.

---

## Full example: before / after

### Before — a vague message
> *"Help me draft a letter to a supplier who delivered defective equipment."*

You'll get a generic letter, probably too formal, that doesn't use the right commercial terms, and doesn't mention the details of your case.

### After — the 5 levers applied

> *"I run a medical practice in Fès. I ordered an ultrasound machine from a supplier last April. The abdominal probe that was delivered shows image distortion visible during normal use. My technician confirmed the defect. I want to write a formal complaint letter to get a free replacement, not a refund.*
>
> *Constraints:*
> *- Maximum one A4 page*
> *- Firm but courteous tone, I want to preserve the commercial relationship*
> *- No threat of legal proceedings at this stage*
> *- Standard commercial vocabulary, not legal*
>
> *Expected structure:*
> *1. Reminder of the order (date, reference)*
> *2. Description of the problem*
> *3. Technical finding*
> *4. Specific request (replacement within X weeks)*
> *5. Closing*
>
> *Think before drafting: what are the elements to highlight so they take my request seriously without feeling attacked?*
> *"*

You get a letter you can sign as-is, or almost.

**Difference in drafting time**: your original message is 15 words, the good one is 150 words. You spend 2 extra minutes. You save 20 minutes of editing afterwards.

---

## The "Claude should guess" trap

If you catch yourself thinking *"he should obviously understand that..."*, **that's the signal that you have information in your head that isn't in your message**. Put it in.

Typical examples:

- *"he should obviously understand I'm in a rush"* → add *"short answer, I don't have time"*
- *"he should obviously understand it's for my website"* → add *"content for my website, commercial tone"*
- *"he should obviously understand it's a joke"* → add *"humorous tone"*

Claude isn't mean. He does his best with what he has. If you give him more, he does better.

---

## How much context is too much?

Fair question. The honest answer: **rarely too much**.

As long as you give relevant info (who you are, for whom, constraints, format), you can write 500 words of context with no problem. Claude reads, integrates, adjusts.

The moment it becomes "too much" is when you drown the main instruction in parasitic context. *"Yesterday I saw my accountant, he was wearing a blue sweater, we talked about VAT and by the way he told me..."* — cut what isn't useful to the answer.

Simple test: for each sentence of context, ask yourself *"if I remove it, does the answer become less useful?"*. If no, remove.

---

## When to move to the next level?

When you catch yourself **rewriting the same context** in several different conversations — for example if you keep giving your medical situation, your commercial constraints, or the structure of your notes at every new conversation — that's the moment to structure it **once and for all**.

That's exactly the subject of the next tutorial.

---

## Memorable recap

> Five levers: **context** (who, why, what for), **constraints** (length, tone, vocabulary, things to avoid), **example** (show, don't describe), **step-by-step reasoning** (for complex tasks), **iterate** (stay in the conversation). If you find yourself thinking *"he should obviously understand"*, that's a sign you didn't write what you were thinking.

---

## Going further

- **Tutorial 02 — What is an AI agent, really?**: distinguish chatbot, role-based agent, automated agent. Understand what we call "agent" in this repo.
- **Tutorial 03 — Building your first brief**: when context becomes stable, formalize it into a reusable file.

---

[← Back to summary](../README.md)
