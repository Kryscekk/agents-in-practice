> 🇫🇷 **Lire en français** : [README.md](README.md)

# 07 — Your first Anthropic API call in Python

**Difficulty**: 🟢 Beginner  |  **Time**: 15 min

> You're going to write 10 lines of Python that talk to Claude. No framework, no magic. Just a script that works.

---

## What we're building

A `main.py` script that:
1. Asks Claude something (e.g. *"explain what an API is to a 50-year-old doctor"*)
2. Prints the answer to the terminal
3. Tells you how much it cost (yes, we start directly by tracking the pennies)

When this script works on your machine, **you're 80% of the way there**. Everything else in the repo is just variations on these 10 lines.

## What you need

- Python 3.10 or newer (check: `python3 --version`)
- An Anthropic API key. **Don't have one yet?** [Create one here](https://console.anthropic.com/settings/keys) — free, but add ~$5 of credit afterwards so you can really use it (one call costs ~$0.001, you'll be able to test for a long time with $5)
- 5 minutes of attention

## Step 1 — Install the library

In a terminal:

```bash
pip install anthropic
```

If it complains with `error: externally-managed-environment` (recent Linux), use a venv:

```bash
python3 -m venv venv
source venv/bin/activate
pip install anthropic
```

## Step 2 — Put your API key in an environment variable

**Never paste your key into Python code.** It ends up on GitHub, scanned, stolen, and billed.

In the same terminal:

```bash
export ANTHROPIC_API_KEY="sk-ant-api03-..."
```

(Replace with your real key. It always starts with `sk-ant-`.)

This command only applies to the current terminal session. To make it permanent, add the line to the end of your `~/.bashrc` or `~/.zshrc`.

## Step 3 — The code

Create a `main.py` file next to this README, with the following content:

```python
"""
My first Anthropic API call.
Let's ask Claude a question and print the answer.
"""
import anthropic

# The client reads ANTHROPIC_API_KEY from the environment automatically
client = anthropic.Anthropic()

# The question we're asking Claude
question = "Explain in 3 sentences what an API is, to a 50-year-old doctor."

# The call — this is where the magic happens
response = client.messages.create(
    model="claude-haiku-4-5-20251001",  # cheapest model to start
    max_tokens=300,                      # limit the response length
    messages=[
        {"role": "user", "content": question}
    ]
)

# Print the answer
print("=== Question ===")
print(question)
print()
print("=== Claude's answer ===")
print(response.content[0].text)
print()

# Track the cost (Haiku 4.5 = $1/MTok input, $5/MTok output)
cost = (response.usage.input_tokens * 1.0 + response.usage.output_tokens * 5.0) / 1_000_000
print(f"=== Cost ===")
print(f"Input : {response.usage.input_tokens} tokens")
print(f"Output : {response.usage.output_tokens} tokens")
print(f"Total : ${cost:.6f}")
```

## Step 4 — Run it

```bash
python3 main.py
```

You should see displayed:
- Your question
- Claude's answer (3 sentences about APIs)
- The exact cost in dollars

**That's it. You just made your first API call.** Welcome to the club.

## What you just did, plainly

| Line | What it does |
|---|---|
| `import anthropic` | Loads the official Anthropic library in Python |
| `client = anthropic.Anthropic()` | Creates a "client" — a connection to the Anthropic API. It reads your key by itself. |
| `client.messages.create(...)` | Sends your question. It's ONE HTTP call that goes and comes back. |
| `model="claude-haiku-4-5..."` | Which model you want. Haiku 4.5 is the cheapest. Sonnet and Opus are more expensive but smarter. |
| `max_tokens=300` | Max limit of the response, to avoid blowing up the cost |
| `messages=[...]` | The conversation. Here a single question, but you can put dozens of turns. |
| `response.content[0].text` | The text of Claude's answer |
| `response.usage.*` | How many tokens were consumed (and therefore how much it cost) |

## Common errors

### `anthropic.AuthenticationError`
Your API key isn't recognized. Check:
- That it's properly in the environment: `echo $ANTHROPIC_API_KEY` must show `sk-ant-...`
- That it has no space or newline in the value
- That it hasn't been revoked on console.anthropic.com

### `anthropic.RateLimitError`
Too many calls in too little time, or your account doesn't have enough credit. Go to [console.anthropic.com](https://console.anthropic.com/) → Billing → add credit.

### `ModuleNotFoundError: No module named 'anthropic'`
The `pip install anthropic` didn't work. You may not have activated your venv (`source venv/bin/activate`), or you're using a different Python than the one you installed it for.

## Going further

- **Change the question**: replace the `question` variable, rerun.
- **Change the model**: try `claude-sonnet-4-6` or `claude-opus-4-7`. Compare the answers and the costs.
- **Add a system prompt**: pass `system="You are a urologist in Fès who explains things simply"` in `client.messages.create(...)`.
- **Try a real conversation**: call twice, putting the first response in `messages` with `role="assistant"`.

## Next tutorial

[09 — Your first MCP server](../09-first-mcp-server/): move from a script you run by hand to an agent Claude can drive on its own.
