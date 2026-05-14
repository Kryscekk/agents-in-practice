# 08 — Les 4 piliers d'un agent solide

**Difficulté** : 🟡 Intermédiaire  |  **Durée** : 45 min de lecture, semaines d'application

> Un script qui marche une fois n'est pas un agent. Un agent, c'est du code qui tourne **24 heures sur 24, sept jours sur sept, sans toi**, qui doit survivre aux erreurs, ne pas exposer tes secrets, redémarrer tout seul après une panne, et te laisser une trace de tout ce qu'il a fait. Ces quatre exigences ne sont pas négociables — chacune est un **pilier**.

---

## Pourquoi ce tuto existe

J'ai écrit mon premier agent Python en avril 2026. Il faisait deux choses : lire un PDF, envoyer un message Telegram. Il marchait. Une fois.

La deuxième fois, le PDF était mal scanné, l'agent a crashé. Pas de trace. Pas de notification. Le patient n'a jamais eu son rendez-vous.

C'est ce jour-là que j'ai compris qu'un agent qui marche en démo n'est pas un agent. Un agent c'est ce qui tient quand tu n'es pas là.

J'ai écrit dans la docstring de mon prochain agent ces quatre mots : **Observabilité, Fiabilité, Sécurité, Déploiement**. Depuis, je n'ai pas livré un seul agent en production sans qu'il satisfasse les quatre. Aujourd'hui j'en ai une vingtaine qui tournent 24/7 sur le même serveur, qui gèrent mon cabinet médical et plusieurs systèmes métier. Aucun n'a planté silencieusement depuis des mois.

Voici ces quatre piliers, expliqués avec le code Python qui les incarne, tiré directement de mon système en production (anonymisé pour ne pas exposer des données patient).

---

## Pilier 1 — Observabilité

> **Tu dois pouvoir savoir, sans interroger personne : ce qu'a fait l'agent, quand, en combien de temps, et combien ça t'a coûté.**

Un agent observable, c'est un agent qui te répond à trois questions à n'importe quel moment :
1. *Qu'est-ce que tu as fait dans la dernière heure ?*
2. *Combien de temps ça t'a pris ?*
3. *Combien j'ai dépensé en API ?*

Si tu ne peux pas répondre à ces trois questions en ouvrant un fichier, l'agent n'est pas observable, et tu vas le découvrir au pire moment.

### Ce qu'il faut

- **Un logger structuré, partagé entre tous tes agents.** Pas `print()`. Pas `logging.basicConfig()`. Un vrai logger avec rotation, niveaux, et idéalement format JSON pour pouvoir grep / filter facilement.
- **Une mesure de durée systématique** sur chaque opération importante.
- **Un cost tracker** qui logge chaque appel API (modèle, tokens input, tokens output, coût en $).
- **Des audit logs métier append-only** pour les actions importantes (notifier un user, modifier une donnée, etc.).

### Le code — un logger réutilisable

```python
# shared/logger.py
import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

def get_logger(nom: str, niveau=logging.INFO) -> logging.Logger:
    """Crée un logger structuré qui écrit dans logs/{nom}.log avec rotation."""
    logger = logging.getLogger(nom)
    if logger.handlers:
        return logger  # déjà configuré, on évite les doubles handlers
    
    logger.setLevel(niveau)
    fmt = logging.Formatter(
        '%(asctime)s | %(levelname)-7s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Fichier avec rotation (10 MB × 5 = 50 MB max par agent)
    fh = RotatingFileHandler(
        os.path.join(LOG_DIR, f'{nom}.log'),
        maxBytes=10 * 1024 * 1024, backupCount=5, encoding='utf-8'
    )
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    
    # Stdout aussi pour systemd journal
    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    logger.addHandler(sh)
    
    return logger
```

### Le pattern de mesure de durée

Dans chacun de mes agents, **chaque opération principale est encadrée** par un démarrage marqué et une fin avec durée :

```python
log = get_logger("watchdog_pec")

def traiter_document(chemin_pdf):
    fichier = os.path.basename(chemin_pdf)
    t_start = time.time()
    log.info(f"=== Traitement: {fichier} ===")
    
    try:
        # ... pipeline complet ...
        log.info(f"=== Fin: {fichier} ({time.time() - t_start:.1f}s) ===")
    except Exception as e:
        log.error(f"=== Échec: {fichier} ({time.time() - t_start:.1f}s) ===", exc_info=True)
```

Trois jours plus tard, quand tu te demandes pourquoi tel traitement est lent, `grep "=== Fin:" logs/watchdog_pec.log | awk` te donne la distribution.

### Le cost tracker — la pièce la plus sous-estimée

```python
# shared/cost_tracker.py
import json
import os
from datetime import datetime, timezone

COSTS_FILE = os.path.expanduser("~/.agents/api_costs.jsonl")
os.makedirs(os.path.dirname(COSTS_FILE), exist_ok=True)

PRICING = {
    # USD par million de tokens (en mai 2026)
    "claude-opus-4-7":      {"input": 15.00, "output": 75.00},
    "claude-sonnet-4-6":    {"input":  3.00, "output": 15.00},
    "claude-haiku-4-5":     {"input":  0.80, "output":  4.00},
}

def log_usage(logger, response, agent_name: str = ""):
    """Enregistre le coût d'un appel Anthropic. response = objet response.usage du SDK."""
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

Appelé après chaque réponse Anthropic :

```python
response = client.messages.create(model=..., messages=...)
log_usage(log, response, agent_name="watchdog_pec")
```

Résultat : un fichier `~/.agents/api_costs.jsonl` qui te dit combien tu as dépensé, par agent, par jour. Tu peux le grep en 2 secondes. Le tuto **#12 Cost Tracker** détaille comment l'exploiter.

### Les audit logs métier

Pour les actions qui touchent à la vraie vie (notifications, modifications de DB, transitions d'état), un log technique ne suffit pas. Il faut un **audit log append-only** dédié à l'action métier :

```python
import json
from datetime import datetime

NOTIFICATIONS_LOG = "logs/notifications.jsonl"

def envoyer_notification(destinataire: str, message: str):
    # ... envoi réel ...
    
    with open(NOTIFICATIONS_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps({
            "timestamp": datetime.now().isoformat(),
            "destinataire": destinataire,
            "message_first_80": message[:80],
            "succes": True,
        }, ensure_ascii=False) + "\n")
```

Append-only veut dire : tu ajoutes des lignes, tu ne modifies jamais. C'est ton **journal médico-légal** : 6 mois plus tard, si on te demande *"as-tu bien envoyé cette notification ce jour-là ?"*, tu as la trace.

### Test d'observabilité

Pose-toi cette question, sincèrement : *"Si quelqu'un me demande maintenant combien mon agent a coûté hier, combien de temps il a pris à traiter le PDF de M. X, et à quelle heure il a envoyé telle notification — puis-je répondre en moins de 30 secondes ?"*

Si oui, pilier 1 ✓. Si non, tu as un script, pas un agent.

---

## Pilier 2 — Fiabilité

> **L'agent doit survivre aux erreurs : appel API qui plante, fichier corrompu, réseau coupé, donnée manquante. Ne jamais corrompre l'état, toujours laisser une trace, et toujours pouvoir reprendre.**

Un agent fragile, c'est un agent qui plante au premier événement non prévu et laisse ses fichiers dans un état ambigu. Un agent fiable, c'est l'inverse : peu importe ce qui se passe, l'état final est propre et explicable.

### Ce qu'il faut

- **Retry exponentiel** sur les appels réseau (API Anthropic, HTTP externe, DB distante)
- **try/except** sur chaque opération qui peut échouer, avec **`exc_info=True`** pour avoir la stack trace dans les logs
- **try/finally** au niveau du pipeline pour garantir le nettoyage même en cas de crash
- **Copie avant action** : ne jamais transformer un fichier sans avoir sa copie originale au chaud
- **Anti-écrasement** : si tu écris un fichier, jamais en silence par-dessus un existant

### Le retry exponentiel

```python
# shared/api_utils.py
import time
import anthropic

def call_with_retry(client, max_retries=5, **kwargs):
    """Appelle l'API Anthropic avec retry exponentiel sur rate limit / erreur transitoire."""
    delay = 2.0
    for tentative in range(max_retries):
        try:
            return client.messages.create(**kwargs)
        except anthropic.RateLimitError:
            if tentative == max_retries - 1:
                raise
            time.sleep(delay)
            delay *= 2  # 2, 4, 8, 16, 32 secondes
        except anthropic.APIConnectionError:
            if tentative == max_retries - 1:
                raise
            time.sleep(delay)
            delay *= 2
        except anthropic.APIStatusError as e:
            # 500/503 transitoires : retry. 4xx : on remonte.
            if e.status_code >= 500 and tentative < max_retries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            raise
```

Appelé partout :

```python
response = call_with_retry(
    client,
    model="claude-haiku-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}],
)
```

Tu écris le retry une fois, tu le réutilises dans tous tes agents. Le jour où Anthropic a une panne de 30 secondes, ton agent attend et reprend, au lieu de mourir.

### Le pattern try/finally au pipeline

C'est **la pièce qui fait la différence** entre un agent jetable et un agent prod. Imagine que ton agent traite un fichier `nouveau_scan.pdf` dans `/incoming/`. Si le pipeline crashe au milieu, le fichier reste dans `/incoming/` et **sera retraité indéfiniment** au prochain redémarrage du watcher.

Solution : un wrapper qui garantit le déplacement vers `/echecs/` quoi qu'il arrive.

```python
def traiter_document(chemin_pdf):
    """Wrapper avec try/finally garantit que le fichier sort de /incoming/
    même si une exception non gérée remonte avant un déplacement explicite."""
    fichier = os.path.basename(chemin_pdf)
    try:
        return _traiter_document_impl(chemin_pdf)
    except Exception as e:
        log.error(f"Exception non gérée: {e}", exc_info=True)
    finally:
        # Quoi qu'il arrive, le fichier ne reste pas dans /incoming/
        if os.path.exists(chemin_pdf):
            try:
                os.makedirs(DOSSIER_ECHECS, exist_ok=True)
                dest = os.path.join(DOSSIER_ECHECS, fichier)
                # Gérer le cas d'un homonyme déjà dans /echecs/
                if os.path.exists(dest):
                    base, ext = os.path.splitext(fichier)
                    dest = os.path.join(DOSSIER_ECHECS, f"{base}_{int(time.time())}{ext}")
                shutil.move(chemin_pdf, dest)
                log.warning(f"Fichier déplacé vers /echecs : {dest}")
            except Exception as e2:
                log.error(f"Impossible de déplacer vers /echecs : {e2}")
```

Quand `_traiter_document_impl()` plante n'importe où à l'intérieur, le `finally` garantit que `/incoming/` est libéré. La prochaine arrivée de fichier ne sera pas bloquée.

### Copie avant action

Si ton agent transforme un fichier (OCR, conversion, renommage), **copie l'original ailleurs avant de toucher à quoi que ce soit** :

```python
copie_archive = os.path.join(DOSSIER_ARCHIVE, fichier)
try:
    shutil.copy2(chemin_pdf, copie_archive)  # copy2 préserve les timestamps
except Exception as e:
    log.error(f"Copie archive impossible : {e}")
    return  # on n'avance pas sans archive
```

Un jour ton agent va corrompre un fichier — bug, exception au milieu d'une écriture, disque plein. Sans copie, le fichier original est perdu. Avec copie, tu repars.

### Anti-écrasement silencieux

Si tu génères des fichiers de sortie, **ne jamais écraser un existant**. Ajoute un suffixe :

```python
def _nom_unique(base_nom: str, dossier: str) -> str:
    """Si base_nom existe déjà, ajoute _2, _3, ... jusqu'à trouver libre."""
    chemin = os.path.join(dossier, base_nom)
    if not os.path.exists(chemin):
        return chemin
    racine, ext = os.path.splitext(base_nom)
    for i in range(2, 100):
        nom_test = f"{racine}_{i}{ext}"
        chemin_test = os.path.join(dossier, nom_test)
        if not os.path.exists(chemin_test):
            log.warning(f"Conflit : {base_nom} existe déjà, utilise {nom_test}")
            return chemin_test
    raise RuntimeError(f"Plus de 100 conflits pour {base_nom}")
```

Sans ça : un jour deux fichiers arrivent quasi simultanément avec le même nom généré, le second écrase le premier sans rien dire, tu as perdu une donnée.

### Test de fiabilité

Lance ton agent, puis pendant qu'il traite, **arrache le câble réseau**. Ou tue le processus en cours d'exécution avec `kill -9`. Ou supprime un fichier qu'il est en train de lire.

Au prochain démarrage : est-ce que l'état est récupérable ? Est-ce que tu vois dans les logs ce qui a planté et où ? Est-ce qu'il y a un fichier orphelin quelque part qui va bloquer le prochain traitement ?

Si oui, pilier 2 ✓.

---

## Pilier 3 — Sécurité

> **Aucun secret en clair dans le code. Aucune décision irréversible sans validation. Allowlist plutôt que blocklist. Et plus encore : l'agent ne doit jamais deviner ce qu'il ne sait pas.**

La sécurité c'est moins glamour que les deux autres piliers, mais c'est ce qui te protège de fuiter ta clé API sur GitHub, de fracasser ta DB de prod avec un `DELETE` mal placé, ou de notifier le mauvais patient.

### Les règles non négociables

#### 1. Les secrets vivent dans `.env`, jamais dans le code

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
    raise RuntimeError("ANTHROPIC_KEY manquante dans .env")
```

Et dans le `.gitignore` :
```
.env
.env.*
*.key
```

Le `.env` est `chmod 600` (lisible uniquement par toi). Tu pousses sur GitHub un `.env.example` avec les noms des variables mais sans valeurs.

#### 2. SQL paramétrée toujours

**Jamais ça** :
```python
conn.execute(f"SELECT * FROM patients WHERE nom = '{nom}'")  # injection 💀
```

**Toujours ça** :
```python
conn.execute("SELECT * FROM patients WHERE nom = ?", (nom,))  # safe ✓
```

C'est trivial à respecter, mais le coût d'un oubli unique peut être énorme.

#### 3. Allowlist, jamais blocklist

Si ton agent peut appeler une fonction système (genre `journalctl -u <service>`), **liste explicitement les services autorisés** :

```python
SERVICES_AUTORISES = {"nginx", "postgresql", "mysql", "redis", "docker", "cron"}

def recent_errors(service: str, hours: int = 24) -> str:
    if service not in SERVICES_AUTORISES:
        return f"Service '{service}' refusé. Autorisés : {sorted(SERVICES_AUTORISES)}"
    # ... appel journalctl ...
```

L'agent ne peut **jamais** appeler `journalctl -u sshd` même si on lui demande. Tu n'as pas à anticiper toutes les façons malveillantes — tu n'autorises que ce qui est légitime.

#### 4. L'agent ne décide pas seul quand il y a ambiguïté

Cas vécu : un patient avec un nom courant, l'OCR donne juste "Mohamed" sans prénom de famille. Sept patients matchent. **L'agent ne tranche pas.** Il notifie l'humain :

```python
def matcher_patient(nom: str, prenom: str = "") -> tuple[int, str] | tuple[None, None]:
    candidats = chercher_dans_db(nom)
    
    if not candidats:
        return None, None
    
    if prenom:
        # Match exact mot-entier (pas substring)
        matchs = [c for c in candidats if _prenom_match_exact(prenom, c.nom_complet)]
        if len(matchs) == 1:
            return matchs[0].id, matchs[0].nom_complet
        if len(matchs) > 1:
            # AMBIGU : notifier humain, ne PAS deviner
            notifier_ambiguite(nom, prenom, matchs)
            return None, None
    
    if len(candidats) == 1:
        return candidats[0].id, candidats[0].nom_complet
    
    # Plusieurs candidats sans prénom pour départager : on n'invente pas
    notifier_ambiguite(nom, prenom, candidats)
    return None, None
```

**Règle d'or** : *"Les enregistrements dans la base sont des gens. On ne devine jamais."* Si tu travailles avec des données qui ont un impact réel (médicales, financières, juridiques), ce pilier est plus important que les trois autres réunis.

#### 5. Le `.env.example` documente, le `.env` exécute

Dans ton repo Git :

```bash
# .env.example (commité, public)
ANTHROPIC_KEY=sk-ant-...
TELEGRAM_TOKEN=...
DB_PATH=data/agent.db
```

Sur ta machine :
```bash
cp .env.example .env
# édite .env avec tes vraies valeurs
chmod 600 .env
```

Quelqu'un qui clone ton repo voit la liste des variables nécessaires sans jamais voir tes valeurs.

### Test de sécurité

Trois questions :

1. *Si je `cat .env`, mes clés API sont-elles dedans ? (Réponse correcte : oui. Si elles sont ailleurs aussi, problème.)*
2. *Si je `git grep -i "sk-ant\|TOKEN\|password"` dans tout mon historique, j'ai des hits ? (Réponse correcte : non.)*
3. *Si quelqu'un envoie à mon agent une demande ambiguë (deux patients possibles), il devine ou il me notifie ?*

Trois oui-non-oui = pilier 3 ✓.

---

## Pilier 4 — Déploiement

> **L'agent tourne 24 heures sur 24 sans surveillance. Il redémarre tout seul après une panne. Tu vois son état en un coup d'œil. Tu peux le mettre à jour sans le casser.**

Un agent qu'il faut lancer à la main dans un terminal `tmux` n'est pas déployé. Il faut un mécanisme système qui :
- Le démarre au boot du serveur
- Le redémarre s'il crashe
- Te laisse voir son état et ses logs
- Te permet de le mettre à jour sans le casser

Sur Linux moderne, ça s'appelle **systemd**. Et c'est le sujet exact du tuto #10.

### Le minimum vital : un service systemd

Crée `/etc/systemd/system/mon-agent.service` :

```ini
[Unit]
Description=Mon agent qui surveille les nouveaux scans
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/projets/mon-agent
ExecStart=/usr/bin/python3 watchdog.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

Active-le :

```bash
sudo systemctl daemon-reload
sudo systemctl enable mon-agent.service
sudo systemctl start mon-agent.service
```

Vérifie qu'il tourne :

```bash
sudo systemctl status mon-agent.service
journalctl -u mon-agent.service -f  # logs temps réel
```

Maintenant ton agent :
- Démarre automatiquement au boot du serveur
- Redémarre dans les 10 secondes s'il crashe (`Restart=always`)
- Ses logs vont dans `journalctl`
- Tu le redémarres avec `systemctl restart mon-agent`

### Le health check — superviser tes agents

Quand tu as 7 agents qui tournent en parallèle, tu n'as pas envie d'aller checker chaque service systemd à la main. Tu veux un seul appel qui te dit *tout va bien* ou *X a un problème*.

```python
# shared/health.py
import subprocess
import shutil
from datetime import datetime, timedelta
from pathlib import Path

def health_check() -> dict:
    """Vérifie l'état du système. Renvoyé en JSON ou affiché par CLI."""
    services = ["mon-agent.service", "mon-dashboard.service"]
    
    results = {"timestamp": datetime.now().isoformat(), "checks": []}
    
    # 1. Services systemd
    for svc in services:
        r = subprocess.run(["systemctl", "is-active", svc], capture_output=True, text=True)
        results["checks"].append({
            "type": "service",
            "name": svc,
            "ok": r.stdout.strip() == "active",
            "status": r.stdout.strip(),
        })
    
    # 2. Disque
    total, used, free = shutil.disk_usage("/")
    pct = used / total * 100
    results["checks"].append({
        "type": "disk",
        "name": "/",
        "ok": pct < 85,
        "percent_used": round(pct, 1),
    })
    
    # 3. Logs récents — pas d'ERROR dans la dernière heure ?
    log_file = Path("logs/mon-agent.log")
    if log_file.exists():
        try:
            with open(log_file) as f:
                lines = f.readlines()[-500:]  # 500 dernières lignes
            une_heure = (datetime.now() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M")
            errors_recentes = sum(1 for l in lines if "ERROR" in l and l[:16] >= une_heure)
            results["checks"].append({
                "type": "log_errors_1h",
                "name": "mon-agent",
                "ok": errors_recentes < 5,
                "count": errors_recentes,
            })
        except Exception:
            pass
    
    results["overall_ok"] = all(c["ok"] for c in results["checks"])
    return results
```

Un cron toutes les 15 min qui appelle ça et te notifie sur Telegram si `overall_ok` est `False`. Tu sais que **quelque chose ne va pas** dans la minute, sans surveiller.

### La règle de redéploiement

Quand tu modifies le code d'un agent en cours de fonctionnement, **redémarre toujours le service** :

```bash
git pull
sudo systemctl restart mon-agent.service
sudo systemctl status mon-agent.service  # vérif 5s après
```

C'est tellement courant que je l'ai automatisé : un script `cabredeploy` qui fait `git pull && systemctl restart && status`. Tape la commande, vérifie 5 secondes plus tard que c'est `active (running)`, c'est fini.

### Test de déploiement

Trois épreuves :

1. *Reboot le serveur (`sudo reboot`). Au retour, ton agent tourne-t-il sans rien faire ?*
2. *Tue le processus de ton agent (`pkill -9`). Il redémarre tout seul dans les 10 secondes ?*
3. *Tu peux lire ses logs des dernières 24h sans te connecter au serveur en SSH (via le MCP, via un dashboard, via Telegram) ?*

Trois oui = pilier 4 ✓.

---

## Mettre les quatre piliers ensemble

Voilà un squelette minimal qui réunit les quatre, sur un agent qui fait juste *"toutes les 5 min, regarde s'il y a un nouveau fichier dans `/incoming/`, traite-le, range-le"*. C'est volontairement minimal, mais chaque pilier est là.

```python
# mon_agent.py
"""
Agent de traitement de fichiers.
Les 4 piliers : logs structurés (1), retry + try/finally (2),
secrets en .env + allowlist (3), tourne via systemd (4).
"""
import os
import sys
import time
import shutil
from pathlib import Path
from dotenv import load_dotenv

# Pilier 3 — secrets
ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(ENV_PATH)
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TYPES_AUTORISES = {".pdf", ".jpg", ".png"}  # allowlist

# Pilier 1 — logger
from shared.logger import get_logger
log = get_logger("mon_agent")

# Pilier 2 — retry réutilisable
from shared.api_utils import call_with_retry

INCOMING = Path("/incoming")
ARCHIVE = Path("/archive")
ECHECS = Path("/echecs")
for d in (ARCHIVE, ECHECS):
    d.mkdir(exist_ok=True)


def traiter_fichier(chemin: Path):
    """Pipeline d'un fichier. Pilier 2 : try/finally garantit le déplacement."""
    t_start = time.time()
    log.info(f"=== Traitement: {chemin.name} ===")
    
    try:
        # Pilier 3 : allowlist
        if chemin.suffix.lower() not in TYPES_AUTORISES:
            raise ValueError(f"Extension non autorisée : {chemin.suffix}")
        
        # Pilier 2 : copie avant action
        archive = ARCHIVE / chemin.name
        shutil.copy2(chemin, archive)
        
        # ... ici le vrai traitement (OCR, appel API, etc.) ...
        # Si on appelle une API : call_with_retry(...) du pilier 2
        
        # Pilier 1 : durée
        log.info(f"=== Fin: {chemin.name} ({time.time() - t_start:.1f}s) ===")
        chemin.unlink()  # on supprime l'original (la copie est dans ARCHIVE)
    
    except Exception as e:
        log.error(f"Exception : {e}", exc_info=True)
    finally:
        # Pilier 2 : quoi qu'il arrive, on ne laisse pas le fichier dans INCOMING
        if chemin.exists():
            shutil.move(str(chemin), str(ECHECS / chemin.name))
            log.warning(f"Déplacé vers /echecs : {chemin.name}")


def boucle_principale():
    """Pilier 4 : ce code tourne en boucle, lancé par systemd."""
    log.info("Démarrage de l'agent")
    while True:
        try:
            for f in INCOMING.glob("*"):
                if f.is_file():
                    traiter_fichier(f)
        except Exception as e:
            log.error(f"Erreur boucle principale : {e}", exc_info=True)
        time.sleep(60)  # une vérif par minute


if __name__ == "__main__":
    boucle_principale()
```

Avec le service systemd associé en `/etc/systemd/system/mon-agent.service`, ce code tourne en production. Pas du toy code — du code qui résiste.

---

## Comment les quatre piliers se renforcent mutuellement

C'est important de comprendre que **ce ne sont pas quatre listes indépendantes**, mais quatre angles d'une même exigence : *"cet agent doit pouvoir vivre sans moi"*.

| Pilier | Sans lui | Avec lui |
|---|---|---|
| 1 Observabilité | Tu ne sais pas ce qui s'est passé | Tu vois tout dans `logs/` et `~/.agents/api_costs.jsonl` |
| 2 Fiabilité | Un crash perd l'état, le fichier reste coincé | L'état est récupérable, le fichier va dans `/echecs/` |
| 3 Sécurité | Clé API sur GitHub, mauvais patient notifié | `.env` chmod 600, allowlist, notif humaine sur ambigu |
| 4 Déploiement | Tu dois relancer à la main après chaque reboot | `systemctl restart`, ça repart tout seul, health check |

Le pilier 1 te donne **les preuves** que les 2/3/4 fonctionnent. Le pilier 2 te permet **de durer**. Le pilier 3 te permet **de durer sans risque**. Le pilier 4 te permet **de durer sans surveillance**.

Si tu enlèves un seul des quatre, ton agent vit jusqu'à la prochaine vraie panne — pas plus.

---

## Erreurs courantes

### "J'aurais dû mettre des logs"
Le passé. La première fois que tu te dis ça, ajoute le logger **avant** de fixer le bug. La prochaine fois sera plus facile.

### "Mon agent a tourné toute la nuit mais je ne sais pas s'il a fait son travail"
Logs de durée + cost tracker manquants. Au minimum, à chaque fin d'opération : `log.info(f"=== Fin: {item} ({duree:.1f}s) ===")`.

### "Mon agent crashe en silence quand X arrive"
`except: pass` quelque part. Cherche-les avec `grep -rn "except.*: pass" .` et remplace par `except Exception as e: log.error(..., exc_info=True)`.

### "J'ai poussé ma clé API sur GitHub"
- Révoque la clé immédiatement sur [console.anthropic.com](https://console.anthropic.com)
- Crée une nouvelle clé, mets-la en `.env`, ajoute `.env` au `.gitignore`
- Si le repo est public et la fuite récente : envisage de purger l'historique (delete + recreate du repo, c'est plus rapide que `git filter-repo`)

### "Mon service ne démarre pas après reboot"
Tu as oublié `systemctl enable mon-agent.service`. Le `start` lance maintenant. Le `enable` met dans le startup.

---

## Pour aller plus loin

- **Tuto #10 systemd** : approfondit le pilier 4 (services, timers, drop-in, sandboxing)
- **Tuto #12 Cost Tracker** : approfondit le pilier 1 (analyser le `.jsonl`, alertes, courbes)
- **Tuto #13 SQLite locked** : approfondit le pilier 2 (concurrence DB, WAL mode)

---

## Récap mémorisable

> **Observable, fiable, sécurisé, déployé.** Quatre adjectifs. Si ton agent les remplit, il vit. Sinon, il survit jusqu'à la prochaine panne.

---

[← Retour au sommaire](../README.md)
