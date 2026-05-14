> 🇫🇷 **Lire en français** : [README.md](README.md)

# 09 — Your first MCP server (4 useful tools)

**Difficulty**: 🟢 Beginner  |  **Time**: 30 min

> You're going to write a Python file that exposes 4 tools to Claude. Not an abstract "hello world" — four tools you'll want to keep.

---

## What we're building

An MCP server with **4 tools** Claude can call on his own when you talk to him:

1. **`recent_errors(service, hours)`** — lists recent errors for a systemd service (nginx, postgres, etc.)
2. **`git_status_all_projects()`** — git state of all your projects at a glance (branch, modifications, ahead/behind)
3. **`next_appointment(limit)`** — your next appointments from a local JSON file
4. **`api_cost_today()`** — how much you've spent on Anthropic API today

When this server is connected to Claude Desktop, you can say: *"Claude, give me the morning briefing"* — and he calls the 4 tools, formats a summary, gives you everything in one answer.

## Why this changes everything (compared to tutorial 07)

In tutorial 07, you **asked** Claude something. Here, you **give him tools** that he decides to use when relevant. That's the real magic of the MCP protocol: an agent that knows *when* to call which tool.

Concretely:

| Tutorial 07 | Tutorial 09 (here) |
|---|---|
| You ask a question, Claude answers from his general knowledge | Claude can call your own Python functions to answer |
| The exchange fits in one API call | Claude can chain several calls depending on the situation |
| You drive everything in code | You drive in natural language, Claude drives your tools |

## MCP in 30 seconds

**MCP (Model Context Protocol)** is a standard created by Anthropic in 2024 to let an LLM discover and use external tools — databases, APIs, homemade scripts, anything.

- An **MCP server** is a program you write: it exposes tools (with their descriptions and parameters)
- An **MCP client** (Claude Desktop, Claude.ai with Custom Connectors, Cursor, etc.) discovers these tools and makes them available to the agent
- When you talk to the agent, it **decides on its own** when to call which tool

**FastMCP** is a Python library that makes writing an MCP server trivial — that's what we use.

## Prerequisites

- Python 3.10+
- **Claude Desktop** installed ([download](https://claude.ai/download)) — for Mac or Windows
- Linux/macOS for the `recent_errors` tool (uses `journalctl`). On Windows, this tool will return a polite error message, the other 3 work.
- Having followed tutorial 07 (recommended)

⚠️ **iPhone/web?** Claude Desktop on Mac/Windows accepts local MCP servers (stdio). To drive the same server from your iPhone or Claude.ai on the web, you must expose it over public HTTPS — that's exactly the subject of tutorial 10.

## Step 1 — Install

From the `09-first-mcp-server/` folder (this folder):

```bash
pip install -r requirements.txt
```

(or `pip install fastmcp`)

## Step 2 — Prepare the data files

The server reads two local files (for `next_appointment` and `api_cost_today`). Copy the provided examples:

```bash
mkdir -p ~/.agents
cp examples/agenda.json ~/.agents/agenda.json
cp examples/api_costs.jsonl ~/.agents/api_costs.jsonl
```

You can modify these files with your own data afterwards.

## Step 3 — Test the server locally

Before plugging it into Claude, we test with **MCP Inspector**, an official Anthropic tool. Install it and run it:

```bash
npx @modelcontextprotocol/inspector python3 mcp_server.py
```

A web page opens in your browser at `http://localhost:6274/`. You see your 4 tools, you can run them by hand with parameters, and see their answer.

**Test the 4 tools manually**:
- `recent_errors` with `service="nginx"` and `hours=24`
- `git_status_all_projects` (leave `base_dir` empty for default)
- `next_appointment` with `limit=3`
- `api_cost_today` (no parameters)

If everything answers without error, **move to step 4**. If there's an error, see the "Common errors" section below.

## Step 4 — Connect to Claude Desktop

Edit the Claude Desktop config file:

**Mac**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add (or complete if the file already exists):

```json
{
  "mcpServers": {
    "my-first-server": {
      "command": "python3",
      "args": [
        "/ABSOLUTE/PATH/TO/agents-in-practice/09-first-mcp-server/mcp_server.py"
      ]
    }
  }
}
```

⚠️ Replace `/ABSOLUTE/PATH/...` with the real path on your machine. On Mac, it often starts with `/Users/your-name/...`. On Windows, with `C:\\Users\\...`.

**Restart Claude Desktop completely** (quit the app, relaunch).

## Step 5 — The magic moment

Open a new conversation in Claude Desktop. At the bottom of the message editor, you should see a tools icon — click it, you'll see `my-first-server` with 4 tools listed.

Now, ask Claude:

> *"Give me the morning rundown: any errors on nginx in the last 24h? State of my git projects? My next appointments? How much did I spend on the API today?"*

You'll watch Claude call the 4 tools one by one, read the results, and synthesize everything in a single message. **That's the wow effect.**

Other examples to try:

- *"Are there any PostgreSQL errors right now?"* → he calls `recent_errors("postgresql", 1)`
- *"What's my next appointment?"* → he calls `next_appointment(1)`
- *"Can you give me the git state of the MASI repo?"* → he calls `git_status_all_projects()` and filters the answer for you

## What you just did, plainly

| Concept | What it means |
|---|---|
| `FastMCP("my-first-server")` | Creates a named MCP server. The name is what Claude sees in his UI. |
| `@mcp.tool` | Decorator that turns a Python function into a tool exposed to Claude. |
| Type hints (`str`, `int = 24`) | Claude uses the types to validate and understand the parameters. |
| Docstring | **The most important thing**: Claude reads the docstring to decide when to call the tool. Be clear and precise. |
| `mcp.run()` | Starts the server in stdio mode (standard input/output), the mode used by Claude Desktop. |

## Security — why `ALLOWED_SERVICES`

You'll notice in the code an **allowlist**:

```python
ALLOWED_SERVICES = {"nginx", "postgresql", "mysql", "redis", "docker", "cron", "fail2ban"}
```

This is intentional. Without this list, Claude could theoretically call `recent_errors("sshd", ...)` or `recent_errors("system", ...)` and expose sensitive info you don't want flowing into a conversation. The general rule: **any parameter that looks like a resource name must go through an allowlist or an explicit filter**.

Same principle with `base_dir` in `git_status_all_projects`: we don't authorize any path, we take a safe default (`~/projects/`).

## Common errors

### `ModuleNotFoundError: No module named 'fastmcp'`
`pip install fastmcp` wasn't done in the right Python environment. If you use a venv, activate it first. Check with `python3 -c "import fastmcp; print(fastmcp.__version__)"`.

### The `recent_errors` tool returns *"journalctl not found"*
You're on Windows or Mac (no systemd). The other 3 tools work. To test it, use a Linux VPS (Hetzner CX22 at 5€/month — that's what I run on).

### `git_status_all_projects` finds nothing
You don't have a `~/projects/` folder or it's empty of git repos. Pass a different path: `git_status_all_projects(base_dir="/Users/you/Code")`.

### Claude Desktop doesn't see the server after restart
Check 3 things:
1. The **absolute path** in the JSON is correct (try `ls /ABSOLUTE/PATH/...` in a terminal)
2. The JSON is **valid** (use [jsonlint.com](https://jsonlint.com/) to check)
3. You **fully quit** Claude Desktop before relaunching (not just closed the window)

### The tool returns a raw Python error
Look at Claude Desktop logs:
- Mac: `~/Library/Logs/Claude/`
- Windows: `%APPDATA%\Claude\logs\`

## Going further

- **Plug in your real data**: replace `~/.agents/agenda.json` with an iCal export of your real calendar, or write a small script that syncs. A separate project can also write to `~/.agents/api_costs.jsonl` in real time.
- **Add a 5th tool**: e.g. `disk_usage(path)` that returns free space on a mount point. Good practice: copy an existing function, modify it.
- **Secure more**: add a default `dry_run=True` argument on tools that could modify things (but here we're all read-only, so not necessary).

## Next tutorial

[**10 — Run your agent 24/7 with systemd**](../10-systemd-for-your-agent/): we take this MCP server and make it accessible **from your iPhone, from anywhere** — systemd service + nginx + HTTPS. It's the logical next step.
