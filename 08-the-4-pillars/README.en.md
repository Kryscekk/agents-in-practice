> 🇫🇷 **Lire en français** : [README.md](README.md)

# 08 — The 4 pillars of a production-grade AI agent

**Difficulty**: 🟡 Intermediate  |  **Time**: 45 min reading, weeks of practice

> A script that works once is not an agent. An agent is code that runs **24 hours a day, seven days a week, without you** — code that must survive errors, protect your secrets, restart itself after a crash, and leave you a trace of everything it did. These four requirements are non-negotiable. Each one is a **pillar**.

---

## Table of contents

1. [Why this tutorial exists](#why-this-tutorial-exists)
2. [Pillar 1 — Observability](#pillar-1--observability)
3. [Pillar 2 — Reliability](#pillar-2--reliability)
4. [Pillar 3 — Security](#pillar-3--security)
5. [Pillar 4 — Deployment](#pillar-4--deployment)
6. [Putting the four pillars together](#putting-the-four-pillars-together)
7. [How the four pillars reinforce each other](#how-the-four-pillars-reinforce-each-other)
8. [Common mistakes](#common-mistakes)
9. [Further reading](#further-reading)
10. [Memorable recap](#memorable-recap)

---

## Why this tutorial exists

I wrote my first Python agent in April 2026. It did two things: read a PDF, send a Telegram message. It worked. Once.

The second time, the PDF was poorly scanned. The agent crashed. No trace. No notification. The patient never got their appointment.

That's the day I understood: an agent that works in demo is not an agent. An agent is what holds up when you're not around.

I wrote four words in the docstring of my next agent: **Observability, Reliability, Security, Deployment.** Since then, I haven't shipped a single agent to production without all four. Today I run about twenty 24/7, on the same server — handling my medical practice and several business systems. None has silently crashed for months.

Here are those four pillars, explained with the Python code that incarnates them, taken directly from my production system (anonymized so as not to expose patient data).

---

## Pillar 1 — Observability

> **You must be able to know, without asking anyone: what the agent did, when, how long it took, and how much it cost you.**

An observable agent answers three questions at any moment:
1. *What did you do in the last hour?*
2. *How long did it take you?*
3. *How much did I spend on API calls?*

If you can't answer these three questions by opening a file, the agent isn't observable — and you'll find out at the worst possible moment.

### What you need

- **A structured logger, shared across all your agents.** Not `print()`. Not `logging.basicConfig()`. A real logger with rotation, levels, ideally JSON format so you can grep / filter easily.
- **Systematic duration measurement** on every important operation.
- **A cost tracker** that logs every API call (model, input tokens, output tokens, cost in $).
- **Append-only business audit logs** for important actions (user notifications, data changes, etc.).

### The code — a reusable logger

```python
# shared/logger.py
import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

def get_logger(name: str, level=logging.INFO) -> logging.Logger:
    """Creates a structured logger that writes to logs/{name}.log with rotation."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # already configured, avoid duplicate handlers
    
    logger.setLevel(level)
    fmt = logging.Formatter(
        '%(asctime)s | %(levelname)-7s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Rotated file (10 MB × 5 = 50 MB max per agent)
    fh = RotatingFileHandler(
        os.path.join(LOG_DIR, f'{name}.log'),
        maxBytes=10 * 1024 * 1024, backupCount=5, encoding='utf-8'
    )
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    
    # stdout too, for systemd journal
    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    logger.addHandler(sh)
    
    return logger
```

### The duration-measurement pattern

In every one of my agents, **each main operation is bracketed** by a marked start and an end with duration:

```python
log = get_logger("watchdog_pec")

def process_document(pdf_path):
    filename = os.path.basename(pdf_path)
    t_start = time.time()
    log.info(f"=== Processing: {filename} ===")
    
    try:
        # ... full pipeline ...
        log.info(f"=== Done: {filename} ({time.time() - t_start:.1f}s) ===")
    except Exception as e:
        log.error(f"=== Failed: {filename} ({time.time() - t_start:.1f}s) ===", exc_info=True)
```

Three days later, when you wonder why a certain process is slow, `grep "=== Done:" logs/watchdog_pec.log | awk` gives you the distribution.

### The cost tracker — the most underrated piece

```python
# shared/cost_tracker.py
import json
import os
from datetime import datetime, timezone

COSTS_FILE = os.path.expanduser("~/.agents/api_costs.jsonl")
os.makedirs(os.path.dirname(COSTS_FILE), exist_ok=True)

PRICING = {
    # USD per million tokens (as of May 2026)
    "claude-opus-4-7":      {"input": 15.00, "output": 75.00},
    "claude-sonnet-4-6":    {"input":  3.00, "output": 15.00},
    "claude-haiku-4-5":     {"input":  0.80, "output":  4.00},
}

def log_usage(logger, response, agent_name: str = ""):
    """Records the cost of an Anthropic API call. response = SDK response object."""
    model = getattr(response, "model", "unknown")
    usage = getattr(response, "usage", None)
    if not usage:
        return
    
    p = PRICING.get(model, {"input": 0, "output": 0})
    cost = (usage.input_tokens * p["input"] + usage.output_tokens * p["output"]) / 1_000_000
    
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agent": agent_name or logger.name,
        "model": model,
        "input_tokens": usage.input_tokens,
        "output_tokens": usage.output_tokens,
        "cost_usd": round(cost, 6),
    }
    with open(COSTS_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    
    logger.info(f"💰 {model}: {usage.input_tokens}↓ + {usage.output_tokens}↑ = ${cost:.4f}")
```

Called after every Anthropic response:

```python
response = client.messages.create(model=..., messages=...)
log_usage(log, response, agent_name="watchdog_pec")
```

Result: a `~/.agents/api_costs.jsonl` file telling you how much you've spent, per agent, per day. You can grep it in 2 seconds. Tutorial **#12 Cost Tracker** details how to exploit it.

### Business audit logs

For actions that touch real life (notifications, DB changes, state transitions), a technical log is not enough. You need a **dedicated append-only audit log** for the business action:

```python
import json
from datetime import datetime

NOTIFICATIONS_LOG = "logs/notifications.jsonl"

def send_notification(recipient: str, message: str):
    # ... actual send ...
    
    with open(NOTIFICATIONS_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps({
            "timestamp": datetime.now().isoformat(),
            "recipient": recipient,
            "message_first_80": message[:80],
            "success": True,
        }, ensure_ascii=False) + "\n")
```

Append-only means: you add lines, never modify them. This is your **medico-legal journal**: 6 months later, if someone asks *"did you actually send this notification that day?"*, you have the trace.

### Observability test

Ask yourself honestly: *"If someone asks me right now how much my agent cost yesterday, how long it took to process Mr. X's PDF, and at what time it sent such-and-such notification — can I answer in under 30 seconds?"*

If yes, Pillar 1 ✓. If no, you have a script, not an agent.

---

## Pillar 2 — Reliability

> **The agent must survive errors: failing API call, corrupted file, broken network, missing data. Never corrupt state, always leave a trace, always be able to resume.**

A fragile agent is one that crashes on the first unforeseen event and leaves its files in an ambiguous state. A reliable agent is the opposite: no matter what happens, the final state is clean and explainable.

### What you need

- **Exponential retry** on network calls (Anthropic API, external HTTP, remote DB)
- **try/except** on every operation that can fail, with **`exc_info=True`** to get the stack trace in the logs
- **try/finally** at the pipeline level to guarantee cleanup even on crash
- **Copy before action**: never transform a file without having its copy safely stored
- **Anti-overwrite**: if you write a file, never silently overwrite an existing one

### Exponential retry

```python
# shared/api_utils.py
import time
import anthropic

def call_with_retry(client, max_retries=5, **kwargs):
    """Call the Anthropic API with exponential retry on rate limit / transient errors."""
    delay = 2.0
    for attempt in range(max_retries):
        try:
            return client.messages.create(**kwargs)
        except anthropic.RateLimitError:
            if attempt == max_retries - 1:
                raise
            time.sleep(delay)
            delay *= 2  # 2, 4, 8, 16, 32 seconds
        except anthropic.APIConnectionError:
            if attempt == max_retries - 1:
                raise
            time.sleep(delay)
            delay *= 2
        except anthropic.APIStatusError as e:
            # 500/503 transient: retry. 4xx: re-raise.
            if e.status_code >= 500 and attempt < max_retries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            raise
```

Used everywhere:

```python
response = call_with_retry(
    client,
    model="claude-haiku-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}],
)
```

You write the retry once, you reuse it in all your agents. The day Anthropic has a 30-second outage, your agent waits and resumes instead of dying.

### The pipeline try/finally pattern

This is **the piece that makes the difference** between a throwaway agent and a production agent. Imagine your agent processes a `new_scan.pdf` file in `/incoming/`. If the pipeline crashes mid-way, the file stays in `/incoming/` and **will be reprocessed indefinitely** on the next watcher restart.

Solution: a wrapper that guarantees the move to `/failed/` no matter what.

```python
def process_document(pdf_path):
    """Wrapper with try/finally ensures the file leaves /incoming/
    even if an unhandled exception propagates before an explicit move."""
    filename = os.path.basename(pdf_path)
    try:
        return _process_document_impl(pdf_path)
    except Exception as e:
        log.error(f"Unhandled exception: {e}", exc_info=True)
    finally:
        # No matter what, the file doesn't stay in /incoming/
        if os.path.exists(pdf_path):
            try:
                os.makedirs(FAILED_DIR, exist_ok=True)
                dest = os.path.join(FAILED_DIR, filename)
                # Handle the case of an already-existing homonym in /failed/
                if os.path.exists(dest):
                    base, ext = os.path.splitext(filename)
                    dest = os.path.join(FAILED_DIR, f"{base}_{int(time.time())}{ext}")
                shutil.move(pdf_path, dest)
                log.warning(f"File moved to /failed: {dest}")
            except Exception as e2:
                log.error(f"Could not move to /failed: {e2}")
```

When `_process_document_impl()` crashes anywhere inside, the `finally` guarantees that `/incoming/` is released. The next file arrival won't be blocked.

### Copy before action

If your agent transforms a file (OCR, conversion, rename), **copy the original elsewhere before touching anything**:

```python
archive_copy = os.path.join(ARCHIVE_DIR, filename)
try:
    shutil.copy2(pdf_path, archive_copy)  # copy2 preserves timestamps
except Exception as e:
    log.error(f"Archive copy failed: {e}")
    return  # we don't proceed without an archive
```

One day your agent will corrupt a file — bug, exception mid-write, full disk. Without a copy, the original file is lost. With a copy, you start over.

### Anti-silent-overwrite

If you generate output files, **never overwrite an existing one**. Append a suffix:

```python
def _unique_name(base_name: str, directory: str) -> str:
    """If base_name exists, append _2, _3, ... until free."""
    path = os.path.join(directory, base_name)
    if not os.path.exists(path):
        return path
    root, ext = os.path.splitext(base_name)
    for i in range(2, 100):
        candidate = f"{root}_{i}{ext}"
        candidate_path = os.path.join(directory, candidate)
        if not os.path.exists(candidate_path):
            log.warning(f"Conflict: {base_name} exists, using {candidate}")
            return candidate_path
    raise RuntimeError(f"More than 100 conflicts for {base_name}")
```

Without this: one day two files arrive nearly simultaneously with the same generated name, the second one silently overwrites the first, you've lost data.

### Reliability test

Launch your agent, then while it processes, **pull the network cable**. Or kill the running process with `kill -9`. Or delete a file it's reading.

On the next start: is the state recoverable? Do you see in the logs what crashed and where? Is there an orphan file somewhere that will block the next process?

If yes, Pillar 2 ✓.

---

## Pillar 3 — Security

> **No secrets in code in clear text. No irreversible decisions without validation. Allowlist over blocklist. And further: the agent must never guess what it doesn't know.**

Security is less glamorous than the other two pillars, but it's what protects you from leaking your API key on GitHub, from wrecking your prod DB with a misplaced `DELETE`, or from notifying the wrong patient.

### Non-negotiable rules

#### 1. Secrets live in `.env`, never in code

```python
# shared/config.py
from dotenv import load_dotenv
import os

ENV_PATH = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(ENV_PATH)

ANTHROPIC_KEY = os.environ.get("ANTHROPIC_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
DB_PATH = os.environ.get("DB_PATH", "data/agent.db")

if not ANTHROPIC_KEY:
    raise RuntimeError("ANTHROPIC_KEY missing in .env")
```

And in `.gitignore`:
```
.env
.env.*
*.key
```

The `.env` is `chmod 600` (readable only by you). You push to GitHub a `.env.example` with variable names but no values.

#### 2. Parameterized SQL, always

**Never this**:
```python
conn.execute(f"SELECT * FROM patients WHERE name = '{name}'")  # injection 💀
```

**Always this**:
```python
conn.execute("SELECT * FROM patients WHERE name = ?", (name,))  # safe ✓
```

Trivial to respect, but the cost of a single oversight can be huge.

#### 3. Allowlist, never blocklist

If your agent can call a system function (e.g. `journalctl -u <service>`), **list the authorized services explicitly**:

```python
ALLOWED_SERVICES = {"nginx", "postgresql", "mysql", "redis", "docker", "cron"}

def recent_errors(service: str, hours: int = 24) -> str:
    if service not in ALLOWED_SERVICES:
        return f"Service '{service}' refused. Allowed: {sorted(ALLOWED_SERVICES)}"
    # ... journalctl call ...
```

The agent can **never** call `journalctl -u sshd` even when asked to. You don't have to anticipate every malicious path — you only authorize what's legitimate.

#### 4. The agent doesn't decide alone when ambiguous

Real case: a patient with a common name, OCR gives just "Mohamed" without a family name. Seven patients match. **The agent doesn't choose.** It notifies the human:

```python
def match_patient(last_name: str, first_name: str = "") -> tuple[int, str] | tuple[None, None]:
    candidates = search_in_db(last_name)
    
    if not candidates:
        return None, None
    
    if first_name:
        # Exact word match (not substring)
        matches = [c for c in candidates if _exact_word_match(first_name, c.full_name)]
        if len(matches) == 1:
            return matches[0].id, matches[0].full_name
        if len(matches) > 1:
            # AMBIGUOUS: notify human, do NOT guess
            notify_ambiguity(last_name, first_name, matches)
            return None, None
    
    if len(candidates) == 1:
        return candidates[0].id, candidates[0].full_name
    
    # Multiple candidates without first name to disambiguate: we don't invent
    notify_ambiguity(last_name, first_name, candidates)
    return None, None
```

**Golden rule**: *"Records in the database are people. We never guess."* If you work with data that has real-world impact (medical, financial, legal), this pillar matters more than the other three combined.

#### 5. `.env.example` documents, `.env` executes

In your Git repo:

```bash
# .env.example (committed, public)
ANTHROPIC_KEY=sk-ant-...
TELEGRAM_TOKEN=...
DB_PATH=data/agent.db
```

On your machine:
```bash
cp .env.example .env
# edit .env with your actual values
chmod 600 .env
```

Someone who clones your repo sees the list of needed variables without ever seeing your values.

### Security test

Three questions:

1. *If I `cat .env`, are my API keys in it? (Correct answer: yes. If they're also elsewhere, problem.)*
2. *If I `git grep -i "sk-ant\|TOKEN\|password"` in all my history, do I get hits? (Correct answer: no.)*
3. *If someone sends my agent an ambiguous request (two possible patients), does it guess or does it notify me?*

Yes / No / Yes = Pillar 3 ✓.

---

## Pillar 4 — Deployment

> **The agent runs 24 hours a day without supervision. It restarts itself after a crash. You see its state at a glance. You can update it without breaking it.**

An agent you have to launch by hand in a `tmux` terminal isn't deployed. You need a system mechanism that:
- Starts it at server boot
- Restarts it if it crashes
- Lets you see its state and logs
- Lets you update it without breaking it

On modern Linux, that's **systemd**. And that's exactly the topic of tutorial #10.

### The bare minimum: a systemd service

Create `/etc/systemd/system/my-agent.service`:

```ini
[Unit]
Description=My agent watching new scans
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/projects/my-agent
ExecStart=/usr/bin/python3 watchdog.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

Enable it:

```bash
sudo systemctl daemon-reload
sudo systemctl enable my-agent.service
sudo systemctl start my-agent.service
```

Verify it's running:

```bash
sudo systemctl status my-agent.service
journalctl -u my-agent.service -f  # live logs
```

Now your agent:
- Starts automatically at server boot
- Restarts within 10 seconds if it crashes (`Restart=always`)
- Its logs go to `journalctl`
- You restart it with `systemctl restart my-agent`

### The health check — supervising your agents

When you have 7 agents running in parallel, you don't want to check each systemd service by hand. You want a single call telling you *everything's fine* or *X has a problem*.

```python
# shared/health.py
import subprocess
import shutil
from datetime import datetime, timedelta
from pathlib import Path

def health_check() -> dict:
    """Check system state. Returned as JSON or shown via CLI."""
    services = ["my-agent.service", "my-dashboard.service"]
    
    results = {"timestamp": datetime.now().isoformat(), "checks": []}
    
    # 1. systemd services
    for svc in services:
        r = subprocess.run(["systemctl", "is-active", svc], capture_output=True, text=True)
        results["checks"].append({
            "type": "service",
            "name": svc,
            "ok": r.stdout.strip() == "active",
            "status": r.stdout.strip(),
        })
    
    # 2. Disk
    total, used, free = shutil.disk_usage("/")
    pct = used / total * 100
    results["checks"].append({
        "type": "disk",
        "name": "/",
        "ok": pct < 85,
        "percent_used": round(pct, 1),
    })
    
    # 3. Recent logs — no ERROR in the last hour?
    log_file = Path("logs/my-agent.log")
    if log_file.exists():
        try:
            with open(log_file) as f:
                lines = f.readlines()[-500:]  # last 500 lines
            one_hour = (datetime.now() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M")
            recent_errors = sum(1 for l in lines if "ERROR" in l and l[:16] >= one_hour)
            results["checks"].append({
                "type": "log_errors_1h",
                "name": "my-agent",
                "ok": recent_errors < 5,
                "count": recent_errors,
            })
        except Exception:
            pass
    
    results["overall_ok"] = all(c["ok"] for c in results["checks"])
    return results
```

A cron every 15 min calling this and notifying you on Telegram if `overall_ok` is `False`. You know **something's wrong** within the minute, without supervising.

### The redeploy rule

When you modify an agent's code while it's running, **always restart the service**:

```bash
git pull
sudo systemctl restart my-agent.service
sudo systemctl status my-agent.service  # check 5s later
```

So common I've automated it: a `redeploy` script that does `git pull && systemctl restart && status`. Type the command, check 5 seconds later that it's `active (running)`, done.

### Deployment test

Three trials:

1. *Reboot the server (`sudo reboot`). On return, does your agent run without you doing anything?*
2. *Kill your agent process (`pkill -9`). Does it restart on its own within 10 seconds?*
3. *Can you read its logs from the last 24h without SSH-ing into the server (via MCP, a dashboard, Telegram)?*

Three yeses = Pillar 4 ✓.

---

## Putting the four pillars together

Here's a minimal skeleton uniting all four, on an agent that just does *"every 5 min, check if there's a new file in `/incoming/`, process it, file it away"*. Deliberately minimal, but every pillar is there.

```python
# my_agent.py
"""
File-processing agent.
The 4 pillars: structured logs (1), retry + try/finally (2),
secrets in .env + allowlist (3), runs via systemd (4).
"""
import os
import sys
import time
import shutil
from pathlib import Path
from dotenv import load_dotenv

# Pillar 3 — secrets
ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(ENV_PATH)
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
ALLOWED_TYPES = {".pdf", ".jpg", ".png"}  # allowlist

# Pillar 1 — logger
from shared.logger import get_logger
log = get_logger("my_agent")

# Pillar 2 — reusable retry
from shared.api_utils import call_with_retry

INCOMING = Path("/incoming")
ARCHIVE = Path("/archive")
FAILED = Path("/failed")
for d in (ARCHIVE, FAILED):
    d.mkdir(exist_ok=True)


def process_file(path: Path):
    """File pipeline. Pillar 2: try/finally guarantees the move."""
    t_start = time.time()
    log.info(f"=== Processing: {path.name} ===")
    
    try:
        # Pillar 3: allowlist
        if path.suffix.lower() not in ALLOWED_TYPES:
            raise ValueError(f"Extension not allowed: {path.suffix}")
        
        # Pillar 2: copy before action
        archive = ARCHIVE / path.name
        shutil.copy2(path, archive)
        
        # ... actual processing here (OCR, API call, etc.) ...
        # If calling an API: call_with_retry(...) from Pillar 2
        
        # Pillar 1: duration
        log.info(f"=== Done: {path.name} ({time.time() - t_start:.1f}s) ===")
        path.unlink()  # delete the original (the copy is in ARCHIVE)
    
    except Exception as e:
        log.error(f"Exception: {e}", exc_info=True)
    finally:
        # Pillar 2: no matter what, don't leave the file in INCOMING
        if path.exists():
            shutil.move(str(path), str(FAILED / path.name))
            log.warning(f"Moved to /failed: {path.name}")


def main_loop():
    """Pillar 4: this code runs in a loop, launched by systemd."""
    log.info("Agent starting")
    while True:
        try:
            for f in INCOMING.glob("*"):
                if f.is_file():
                    process_file(f)
        except Exception as e:
            log.error(f"Main loop error: {e}", exc_info=True)
        time.sleep(60)  # one check per minute


if __name__ == "__main__":
    main_loop()
```

With the matching systemd service at `/etc/systemd/system/my-agent.service`, this code runs in production. Not toy code — code that holds.

---

## How the four pillars reinforce each other

It's important to understand that **these aren't four independent lists**, but four angles of the same demand: *"this agent must be able to live without me"*.

| Pillar | Without | With |
|---|---|---|
| 1 Observability | You don't know what happened | You see everything in `logs/` and `~/.agents/api_costs.jsonl` |
| 2 Reliability | A crash loses state, file stays stuck | State is recoverable, file goes to `/failed/` |
| 3 Security | API key on GitHub, wrong patient notified | `.env` chmod 600, allowlist, human notification on ambiguity |
| 4 Deployment | You must restart by hand after every reboot | `systemctl restart`, comes back up, health check |

Pillar 1 gives you **the proof** that 2/3/4 work. Pillar 2 lets you **last**. Pillar 3 lets you **last without risk**. Pillar 4 lets you **last without supervision**.

If you remove any one of the four, your agent lives until the next real outage — no longer.

---

## Common mistakes

### "I should have put logs"
The past. The first time you say this, add the logger **before** fixing the bug. Next time will be easier.

### "My agent ran all night but I don't know if it did its job"
Missing duration logs + cost tracker. At minimum, at the end of each operation: `log.info(f"=== Done: {item} ({duration:.1f}s) ===")`.

### "My agent silently crashes when X happens"
`except: pass` somewhere. Hunt them with `grep -rn "except.*: pass" .` and replace with `except Exception as e: log.error(..., exc_info=True)`.

### "I pushed my API key to GitHub"
- Revoke the key immediately on [console.anthropic.com](https://console.anthropic.com)
- Create a new key, put it in `.env`, add `.env` to `.gitignore`
- If the repo is public and the leak is recent: consider purging the history (delete + recreate the repo, faster than `git filter-repo`)

### "My service doesn't start after reboot"
You forgot `systemctl enable my-agent.service`. `start` launches now. `enable` adds it to startup.

---

## Further reading

- **Tutorial #10 systemd**: deepens Pillar 4 (services, timers, drop-in, sandboxing)
- **Tutorial #12 Cost Tracker**: deepens Pillar 1 (analyzing the `.jsonl`, alerts, graphs)
- **Tutorial #13 SQLite locked**: deepens Pillar 2 (DB concurrency, WAL mode)

---

## Memorable recap

> **Observable, reliable, secure, deployed.** Four adjectives. If your agent meets them, it lives. Otherwise, it survives until the next outage.

---

[← Back to summary](../README.md)
