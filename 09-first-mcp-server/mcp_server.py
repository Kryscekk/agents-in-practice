"""
Mon premier MCP server — 4 outils utiles au quotidien.

Lance :
    python3 mcp_server.py

Pour brancher à Claude Desktop : voir le README, section "Connecter à Claude Desktop".
"""
from __future__ import annotations
import json
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

from fastmcp import FastMCP

# === Configuration ===
# Chemins par défaut — modifiables via variables d'environnement ou à la main
HOME = Path.home()
AGENTS_DIR = HOME / ".agents"               # dossier où vivent les données de tes agents
AGENDA_FILE = AGENTS_DIR / "agenda.json"    # ta liste de rdv
COSTS_FILE = AGENTS_DIR / "api_costs.jsonl" # log append-only des appels API
PROJETS_DIR = HOME / "projets"              # tes repos git

# Allowlist de services systemd qu'on autorise à inspecter
# (évite que Claude liste les logs de services sensibles type sshd)
SERVICES_AUTORISES = {"nginx", "postgresql", "mysql", "redis", "docker", "cron", "fail2ban"}


mcp = FastMCP("mon-premier-serveur")


@mcp.tool
def recent_errors(service: str, hours: int = 24) -> str:
    """Retourne les erreurs récentes d'un service systemd (Linux).
    
    Cherche les lignes de niveau ERROR/CRITICAL/EMERGENCY dans les logs systemd
    des dernières N heures pour le service demandé.
    
    Args:
        service: nom du service (ex: 'nginx', 'postgresql'). Doit être dans l'allowlist.
        hours: fenêtre de recherche en heures (1 à 168 = 1 semaine max).
    
    Returns:
        Texte avec les erreurs trouvées, ou message si rien.
    """
    if service not in SERVICES_AUTORISES:
        return (f"Service '{service}' pas dans l'allowlist. "
                f"Autorisés : {', '.join(sorted(SERVICES_AUTORISES))}")
    
    hours = max(1, min(hours, 168))  # borne entre 1h et 1 semaine
    since = f"{hours}h ago"
    
    try:
        result = subprocess.run(
            ["journalctl", "-u", service, "--since", since,
             "-p", "err", "--no-pager", "-n", "50"],
            capture_output=True, text=True, timeout=10
        )
    except FileNotFoundError:
        return "journalctl introuvable. Ce tool nécessite Linux avec systemd."
    except subprocess.TimeoutExpired:
        return "journalctl a mis trop de temps à répondre (>10s)."
    
    output = result.stdout.strip()
    if not output or "No entries" in output:
        return f"Aucune erreur pour {service} sur les {hours} dernières heures. ✓"
    
    return f"Erreurs {service} (dernières {hours}h) :\n\n{output}"


@mcp.tool
def git_status_all_projects(base_dir: str = "") -> str:
    """Donne l'état git de tous tes projets en une fois.
    
    Itère sur les sous-dossiers de base_dir qui sont des repos git, et reporte
    pour chacun : branche courante, fichiers modifiés non-commités, et nombre
    de commits ahead/behind par rapport au remote.
    
    Args:
        base_dir: dossier qui contient tes repos. Défaut : ~/projets/
    
    Returns:
        Tableau lisible des projets et leur état git.
    """
    base = Path(base_dir) if base_dir else PROJETS_DIR
    if not base.exists():
        return f"Dossier {base} n'existe pas. Crée-le ou passe un autre chemin via base_dir."
    
    lignes = [f"État git de tes projets dans {base} :\n"]
    repos_trouves = 0
    
    for sub in sorted(base.iterdir()):
        if not sub.is_dir() or not (sub / ".git").exists():
            continue
        repos_trouves += 1
        
        try:
            # branche courante
            branche = subprocess.run(
                ["git", "-C", str(sub), "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True, text=True, timeout=5
            ).stdout.strip() or "(detached)"
            
            # fichiers modifiés
            status = subprocess.run(
                ["git", "-C", str(sub), "status", "--porcelain"],
                capture_output=True, text=True, timeout=5
            ).stdout.strip()
            modifs = len([l for l in status.split("\n") if l.strip()])
            
            # ahead/behind
            try:
                tracking = subprocess.run(
                    ["git", "-C", str(sub), "rev-list", "--left-right", "--count",
                     f"{branche}...origin/{branche}"],
                    capture_output=True, text=True, timeout=5
                ).stdout.strip()
                ahead, behind = tracking.split("\t") if tracking else ("0", "0")
            except Exception:
                ahead, behind = "?", "?"
            
            etat = "✓ clean" if modifs == 0 else f"⚠ {modifs} fichier(s) modifié(s)"
            lignes.append(f"  • {sub.name:20s} [{branche}] {etat} (↑{ahead} ↓{behind})")
        except Exception as e:
            lignes.append(f"  • {sub.name}: erreur ({e})")
    
    if repos_trouves == 0:
        return f"Aucun repo git trouvé dans {base}. Mets tes projets git dans ce dossier ou passe base_dir."
    
    return "\n".join(lignes)


@mcp.tool
def prochain_rdv(limite: int = 3) -> str:
    """Retourne tes prochains rendez-vous.
    
    Lit ~/.agents/agenda.json (format : liste d'objets {datetime, titre, lieu}).
    Filtre ceux dans le futur, trie, et retourne les N premiers.
    
    Args:
        limite: nombre de prochains rdv à retourner (1 à 20).
    
    Returns:
        Liste lisible des prochains rdv, ou message si agenda vide / pas de rdv futur.
    """
    if not AGENDA_FILE.exists():
        return (f"Fichier {AGENDA_FILE} introuvable. "
                f"Copie le fichier exemple : cp exemples/agenda.json ~/.agents/agenda.json")
    
    try:
        with open(AGENDA_FILE, encoding="utf-8") as f:
            rdv_list = json.load(f)
    except json.JSONDecodeError as e:
        return f"Fichier agenda mal formé : {e}"
    
    limite = max(1, min(limite, 20))
    maintenant = datetime.now(timezone.utc)
    futurs = []
    
    for rdv in rdv_list:
        try:
            dt = datetime.fromisoformat(rdv["datetime"].replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            if dt > maintenant:
                futurs.append((dt, rdv.get("titre", "(sans titre)"), rdv.get("lieu", "")))
        except (KeyError, ValueError):
            continue
    
    if not futurs:
        return "Pas de rendez-vous à venir. Profite. 🌴"
    
    futurs.sort()
    lignes = ["Tes prochains rendez-vous :\n"]
    for dt, titre, lieu in futurs[:limite]:
        local = dt.astimezone()  # convertit en heure locale système
        lieu_str = f" — {lieu}" if lieu else ""
        lignes.append(f"  • {local.strftime('%a %d %b %H:%M')} : {titre}{lieu_str}")
    
    return "\n".join(lignes)


@mcp.tool
def cout_api_aujourd_hui() -> str:
    """Calcule combien tu as dépensé en API Anthropic aujourd'hui.
    
    Lit ~/.agents/api_costs.jsonl (1 ligne JSON par appel API, avec champs
    timestamp et cost_usd). Filtre la journée en cours et somme.
    
    Returns:
        Résumé : nombre d'appels, coût total en $ et MAD approximatif.
    """
    if not COSTS_FILE.exists():
        return (f"Fichier {COSTS_FILE} introuvable. "
                f"Le tuto #05 t'apprend à le générer. "
                f"En attendant : cp exemples/api_costs.jsonl ~/.agents/api_costs.jsonl")
    
    aujourdhui = datetime.now().date()
    appels = 0
    total_usd = 0.0
    
    with open(COSTS_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                ts = datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00"))
                if ts.date() == aujourdhui:
                    appels += 1
                    total_usd += float(entry.get("cost_usd", 0))
            except (json.JSONDecodeError, KeyError, ValueError):
                continue
    
    if appels == 0:
        return "Aucun appel API aujourd'hui (ou fichier exemple à brancher). 💤"
    
    total_mad = total_usd * 10  # approximation grossière USD→MAD
    return (f"Aujourd'hui : {appels} appel(s) API, "
            f"coût total {total_usd:.4f} $ "
            f"(≈ {total_mad:.3f} MAD)")


if __name__ == "__main__":
    mcp.run()
