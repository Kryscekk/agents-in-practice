# 02 — Ton premier MCP server (4 outils utiles)

**Difficulté** : 🟢 Débutant  |  **Durée** : 30 min

> Tu vas écrire un fichier Python qui expose 4 outils à Claude. Pas un "hello world" abstrait — quatre tools que tu vas vouloir garder.

---

## Ce qu'on construit

Un MCP server avec **4 outils** que Claude pourra appeler tout seul quand tu lui parles :

1. **`recent_errors(service, hours)`** — liste les erreurs récentes d'un service systemd (nginx, postgres, etc.)
2. **`git_status_all_projects()`** — état git de tous tes projets en un coup (branche, modifs, ahead/behind)
3. **`prochain_rdv(limite)`** — tes prochains rendez-vous depuis un fichier JSON local
4. **`cout_api_aujourd_hui()`** — combien tu as dépensé en API Anthropic aujourd'hui

Quand ce serveur est branché à Claude Desktop, tu peux dire : *"Claude, fais-moi le point de la matinée"* — et il appelle les 4 tools, formate un résumé, te donne tout en une réponse.

## Pourquoi ça change tout (par rapport au tuto #01)

Dans le tuto #01, tu **demandais** quelque chose à Claude. Ici, tu lui **donnes des outils** que lui décide d'utiliser quand c'est pertinent. C'est la vraie magie du protocole MCP : un agent qui sait *quand* appeler quel outil.

Concrètement :

| Tuto #01 | Tuto #02 (ici) |
|---|---|
| Tu poses une question, Claude répond depuis ses connaissances générales | Claude peut appeler tes propres fonctions Python pour répondre |
| L'échange tient en un appel API | Claude peut enchaîner plusieurs appels selon la situation |
| Tu pilotes tout en code | Tu pilotes en langage naturel, Claude pilote tes outils |

## MCP en 30 secondes

**MCP (Model Context Protocol)** est un standard créé par Anthropic en 2024 pour permettre à un LLM de découvrir et utiliser des outils externes — bases de données, APIs, scripts maison, n'importe quoi.

- Un **MCP server** est un programme que tu écris : il expose des outils (avec leurs descriptions et paramètres)
- Un **MCP client** (Claude Desktop, Claude.ai avec Custom Connectors, Cursor, etc.) découvre ces outils et les rend disponibles à l'agent
- Quand tu parles à l'agent, il **choisit lui-même** quand appeler quel outil

**FastMCP** est une bibliothèque Python qui rend l'écriture d'un MCP server triviale — c'est ce qu'on utilise.

## Pré-requis

- Python 3.10+
- **Claude Desktop** installé ([download](https://claude.ai/download)) — pour Mac ou Windows
- Linux/macOS pour le tool `recent_errors` (utilise `journalctl`). Sur Windows, ce tool retournera un message d'erreur poli, les 3 autres marchent.
- Avoir suivi le tuto #01 (recommandé)

⚠️ **iPhone/web ?** Claude Desktop sur Mac/Windows accepte les MCP servers locaux (stdio). Pour piloter le même serveur depuis ton iPhone ou Claude.ai en web, il faut l'exposer en HTTPS public — c'est exactement le sujet du tuto #03.

## Étape 1 — Installer

Depuis le dossier `09-first-mcp-server/` (ce dossier) :

```bash
pip install -r requirements.txt
```

(ou `pip install fastmcp`)

## Étape 2 — Préparer les fichiers de données

Le serveur lit deux fichiers locaux (pour `prochain_rdv` et `cout_api_aujourd_hui`). Copie les exemples fournis :

```bash
mkdir -p ~/.agents
cp exemples/agenda.json ~/.agents/agenda.json
cp exemples/api_costs.jsonl ~/.agents/api_costs.jsonl
```

Tu peux modifier ces fichiers avec tes propres données ensuite.

## Étape 3 — Tester le serveur en local

Avant de le brancher à Claude, on teste avec **MCP Inspector**, un outil officiel Anthropic. Installe-le et lance-le :

```bash
npx @modelcontextprotocol/inspector python3 mcp_server.py
```

Une page web s'ouvre dans ton navigateur sur `http://localhost:6274/`. Tu y vois tes 4 tools, tu peux les exécuter à la main avec des paramètres, et voir leur réponse.

**Teste les 4 tools manuellement** :
- `recent_errors` avec `service="nginx"` et `hours=24`
- `git_status_all_projects` (laisse `base_dir` vide pour défaut)
- `prochain_rdv` avec `limite=3`
- `cout_api_aujourd_hui` (pas de paramètres)

Si tout répond sans erreur, **passe à l'étape 4**. Si une erreur, va voir la section "Erreurs courantes" plus bas.

## Étape 4 — Connecter à Claude Desktop

Édite le fichier de config de Claude Desktop :

**Mac** : `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows** : `%APPDATA%\Claude\claude_desktop_config.json`

Ajoute (ou complète si le fichier existe déjà) :

```json
{
  "mcpServers": {
    "mon-premier-serveur": {
      "command": "python3",
      "args": [
        "/CHEMIN/ABSOLU/VERS/agents-en-pratique/09-first-mcp-server/mcp_server.py"
      ]
    }
  }
}
```

⚠️ Remplace `/CHEMIN/ABSOLU/...` par le vrai chemin chez toi. Sur Mac, ça commence souvent par `/Users/ton-nom/...`. Sur Windows, par `C:\\Users\\...`.

**Redémarre complètement Claude Desktop** (quitte l'app, relance).

## Étape 5 — Le moment magique

Ouvre une nouvelle conversation dans Claude Desktop. En bas de l'éditeur de message, tu devrais voir une icône d'outils — clique dessus, tu verras `mon-premier-serveur` avec 4 outils listés.

Maintenant, demande à Claude :

> *"Fais-moi le point de la matinée : as-tu eu des erreurs sur nginx ces dernières 24h ? État de mes projets git ? Mes prochains rdv ? Combien j'ai dépensé en API aujourd'hui ?"*

Tu vas voir Claude appeler les 4 tools un par un, lire les résultats, et te synthétiser tout en un seul message. **C'est ça l'effet wow.**

Autres exemples à essayer :

- *"Y a-t-il des erreurs PostgreSQL en ce moment ?"* → il appelle `recent_errors("postgresql", 1)`
- *"Quel est mon prochain rdv ?"* → il appelle `prochain_rdv(1)`
- *"Tu peux me sortir l'état git du repo MASI ?"* → il appelle `git_status_all_projects()` et filtre la réponse pour toi

## Ce que tu viens de faire, en clair

| Concept | Ce que ça veut dire |
|---|---|
| `FastMCP("mon-premier-serveur")` | Crée un serveur MCP nommé. Le nom est ce que Claude voit dans son UI. |
| `@mcp.tool` | Décorateur qui transforme une fonction Python en outil exposé à Claude. |
| Type hints (`str`, `int = 24`) | Claude utilise les types pour valider et comprendre les paramètres. |
| Docstring | **Le truc le plus important** : Claude lit la docstring pour décider quand appeler le tool. Sois clair et précis. |
| `mcp.run()` | Démarre le serveur en mode stdio (entrée/sortie standard), le mode utilisé par Claude Desktop. |

## Sécurité — pourquoi `SERVICES_AUTORISES`

Tu remarqueras dans le code une **allowlist** :

```python
SERVICES_AUTORISES = {"nginx", "postgresql", "mysql", "redis", "docker", "cron", "fail2ban"}
```

C'est intentionnel. Sans cette liste, Claude pourrait théoriquement appeler `recent_errors("sshd", ...)` ou `recent_errors("system", ...)` et exposer des infos sensibles que tu ne veux pas voir partir dans une conversation. La règle générale : **tout paramètre qui ressemble à un nom de ressource doit passer par une allowlist ou un filtre explicite**.

Même principe avec `base_dir` dans `git_status_all_projects` : on n'autorise pas n'importe quel chemin, on prend un défaut sain (`~/projets/`).

## Erreurs courantes

### `ModuleNotFoundError: No module named 'fastmcp'`
`pip install fastmcp` n'a pas été fait dans le bon environnement Python. Si tu utilises un venv, active-le d'abord. Vérifie avec `python3 -c "import fastmcp; print(fastmcp.__version__)"`.

### Le tool `recent_errors` retourne *"journalctl introuvable"*
Tu es sur Windows ou Mac (pas de systemd). Les 3 autres tools marchent. Pour le tester, utilise un VPS Linux (Hetzner CX22 à 5€/mois — c'est sur celui-là que je tourne).

### `git_status_all_projects` ne trouve rien
Tu n'as pas de dossier `~/projets/` ou il est vide de repos git. Passe un autre chemin : `git_status_all_projects(base_dir="/Users/toi/Code")`.

### Claude Desktop ne voit pas le serveur après redémarrage
Vérifie 3 choses :
1. Le **chemin absolu** dans le JSON est correct (essaie `ls /CHEMIN/ABSOLU/...` dans un terminal)
2. Le JSON est **valide** (utilise [jsonlint.com](https://jsonlint.com/) pour vérifier)
3. Tu as bien **quitté complètement** Claude Desktop avant de relancer (pas juste fermé la fenêtre)

### Le tool retourne une erreur Python brute
Regarde les logs de Claude Desktop :
- Mac : `~/Library/Logs/Claude/`
- Windows : `%APPDATA%\Claude\logs\`

## Pour aller plus loin

- **Branche tes vraies données** : remplace `~/.agents/agenda.json` par un export iCal de ton vrai calendrier, ou écris un petit script qui synchronise. Le repo MASI peut aussi écrire dans `~/.agents/api_costs.jsonl` en temps réel.
- **Ajoute un 5e tool** : par exemple `disk_usage(path)` qui retourne l'espace libre sur un point de montage. Bonne pratique : copie une fonction existante, modifie-la.
- **Sécurise plus** : ajoute un argument `dry_run=True` par défaut sur les tools qui pourraient modifier des choses (mais ici on est tous en lecture seule, donc pas nécessaire).

## Prochain tuto

[**03 — Faire tourner ton agent 24/7 avec systemd**](../10-systemd-for-your-agent/) : on prend ce MCP server et on le rend accessible **depuis ton iPhone, depuis n'importe où** — service systemd + nginx + HTTPS. C'est la suite logique.
