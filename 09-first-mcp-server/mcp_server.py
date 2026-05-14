"""
My first MCP server — 4 useful daily tools.
Mon premier MCP server — 4 outils utiles au quotidien.

To connect to Claude Desktop, see the README, section "Connect to Claude Desktop".
Pour brancher à Claude Desktop : voir le README, section "Connecter à Claude Desktop".
"""
from __future__ import annotations
import json
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

from fastmcp import FastMCP

# === Configuration ===
# Default paths — modifiable via env vars or by hand
HOME = Path.home()
AGENTS_DIR = HOME / ".agents"               # directory where your agents' data lives
AGENDA_FILE = AGENTS_DIR / "agenda.json"    # your appointments list
COSTS_FILE = AGENTS_DIR / "api_costs.jsonl" # append-only log of API calls
PROJECTS_DIR = HOME / "projects"            # your git repos

# Allowlist of systemd services we permit to inspect.
# Prevents Claude from listing logs of sensitive services like sshd.
ALLOWED_SERVICES = {"nginx", "postgresql", "mysql", "redis", "docker", "cron", "fail2ban"}


mcp = FastMCP("my-first-server")


@mcp.tool
def recent_errors(service: str, hours: int = 24) -> str:
    """Returns recent errors from a systemd service (Linux).

    Searches for ERROR/CRITICAL/EMERGENCY level lines in the systemd logs
    of the last N hours for the requested service.

    Args:
        service: service name (e.g. 'nginx', 'postgresql'). Must be in the allowlist.
        hours: search window in hours (1 to 168 = 1 week max).

    Returns:
        Text with the errors found, or a message if none.
    """
    if service not in ALLOWED_SERVICES:
        return (f"Service '{service}' not in allowlist. "
                f"Allowed: {', '.join(sorted(ALLOWED_SERVICES))}")

    hours = max(1, min(hours, 168))  # clamp between 1h and 1 week
    since = f"{hours}h ago"

    try:
        result = subprocess.run(
            ["journalctl", "-u", service, "--since", since,
             "-p", "err", "--no-pager", "-n", "50"],
            capture_output=True, text=True, timeout=10
        )
    except FileNotFoundError:
        return "journalctl not found. This tool requires Linux with systemd."
    except subprocess.TimeoutExpired:
        return "journalctl took too long to respond (>10s)."

    output = result.stdout.strip()
    if not output or "No entries" in output:
        return f"No errors for {service} in the last {hours} hours. ✓"

    return f"Errors for {service} (last {hours}h):\n\n{output}"


@mcp.tool
def git_status_all_projects(base_dir: str = "") -> str:
    """Reports git status for all your projects at once.

    Iterates over subfolders of base_dir that are git repos, and reports
    for each: current branch, modified uncommitted files, and number of
    commits ahead/behind compared to the remote.

    Args:
        base_dir: folder containing your repos. Default: ~/projects/

    Returns:
        Readable table of projects and their git state.
    """
    base = Path(base_dir) if base_dir else PROJECTS_DIR
    if not base.exists():
        return f"Folder {base} doesn't exist. Create it or pass another path via base_dir."

    lines = [f"Git status of your projects in {base}:\n"]
    repos_found = 0

    for sub in sorted(base.iterdir()):
        if not sub.is_dir() or not (sub / ".git").exists():
            continue
        repos_found += 1

        try:
            # current branch
            branch = subprocess.run(
                ["git", "-C", str(sub), "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True, text=True, timeout=5
            ).stdout.strip() or "(detached)"

            # modified files
            status = subprocess.run(
                ["git", "-C", str(sub), "status", "--porcelain"],
                capture_output=True, text=True, timeout=5
            ).stdout.strip()
            modifs = len([l for l in status.split("\n") if l.strip()])

            # ahead/behind
            try:
                tracking = subprocess.run(
                    ["git", "-C", str(sub), "rev-list", "--left-right", "--count",
                     f"{branch}...origin/{branch}"],
                    capture_output=True, text=True, timeout=5
                ).stdout.strip()
                ahead, behind = tracking.split("\t") if tracking else ("0", "0")
            except Exception:
                ahead, behind = "?", "?"

            state = "✓ clean" if modifs == 0 else f"⚠ {modifs} modified file(s)"
            lines.append(f"  • {sub.name:20s} [{branch}] {state} (↑{ahead} ↓{behind})")
        except Exception as e:
            lines.append(f"  • {sub.name}: error ({e})")

    if repos_found == 0:
        return f"No git repos found in {base}. Put your git projects there or pass base_dir."

    return "\n".join(lines)


@mcp.tool
def next_appointment(limit: int = 3) -> str:
    """Returns your next appointments.

    Reads ~/.agents/agenda.json (format: list of objects {datetime, title, location}).
    Filters those in the future, sorts, and returns the first N.

    Args:
        limit: number of next appointments to return (1 to 20).

    Returns:
        Readable list of next appointments, or message if agenda is empty / no future appointment.
    """
    if not AGENDA_FILE.exists():
        return (f"File {AGENDA_FILE} not found. "
                f"Copy the example file: cp examples/agenda.json ~/.agents/agenda.json")

    try:
        with open(AGENDA_FILE, encoding="utf-8") as f:
            appointments = json.load(f)
    except json.JSONDecodeError as e:
        return f"Agenda file malformed: {e}"

    limit = max(1, min(limit, 20))
    now = datetime.now(timezone.utc)
    future = []

    for appt in appointments:
        try:
            # Support both new (title/location) and legacy (titre/lieu) keys
            dt = datetime.fromisoformat(appt["datetime"].replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            if dt > now:
                title = appt.get("title", appt.get("titre", "(untitled)"))
                location = appt.get("location", appt.get("lieu", ""))
                future.append((dt, title, location))
        except (KeyError, ValueError):
            continue

    if not future:
        return "No upcoming appointments. Enjoy. 🌴"

    future.sort()
    lines = ["Your next appointments:\n"]
    for dt, title, location in future[:limit]:
        local = dt.astimezone()  # convert to local system time
        loc_str = f" — {location}" if location else ""
        lines.append(f"  • {local.strftime('%a %d %b %H:%M')}: {title}{loc_str}")

    return "\n".join(lines)


@mcp.tool
def api_cost_today() -> str:
    """Computes how much you've spent on the Anthropic API today.

    Reads ~/.agents/api_costs.jsonl (1 JSON line per API call, with timestamp
    and cost_usd fields). Filters today and sums.

    Returns:
        Summary: number of calls and total cost in $.
    """
    if not COSTS_FILE.exists():
        return (f"File {COSTS_FILE} not found. "
                f"Tutorial 12 teaches you to generate it. "
                f"For now: cp examples/api_costs.jsonl ~/.agents/api_costs.jsonl")

    today = datetime.now().date()
    calls = 0
    total_usd = 0.0

    with open(COSTS_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                ts = datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00"))
                if ts.date() == today:
                    calls += 1
                    total_usd += float(entry.get("cost_usd", 0))
            except (json.JSONDecodeError, KeyError, ValueError):
                continue

    if calls == 0:
        return "No API calls today (or example file to plug in). 💤"

    return f"Today: {calls} API call(s), total cost ${total_usd:.4f}"


if __name__ == "__main__":
    mcp.run()
