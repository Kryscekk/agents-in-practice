> 🇬🇧 **English version**: [README.en.md](README.en.md)

# 01 — Ton premier appel API Anthropic en Python

**Difficulté** : 🟢 Débutant  |  **Durée** : 15 min

> Tu vas écrire 10 lignes de Python qui parlent à Claude. Pas de framework, pas de magie. Juste un script qui marche.

---

## Ce qu'on va construire

Un script `main.py` qui :
1. Demande quelque chose à Claude (ex: *"explique-moi ce qu'est une API à un médecin de 50 ans"*)
2. Affiche la réponse dans le terminal
3. Te dit combien ça a coûté (oui, on commence direct par tracer les sous)

Quand ce script marche chez toi, **tu as fait 80% du chemin**. Tout le reste du repo, c'est des variations de ces 10 lignes.

## Ce qu'il te faut

- Python 3.10 ou plus récent (vérifie : `python3 --version`)
- Une clé API Anthropic. **Pas encore ?** [Crée-en une ici](https://console.anthropic.com/settings/keys) — gratuit, mais ajoute ~5$ de crédit après pour pouvoir vraiment l'utiliser (un appel coûte ~0,001$, tu vas pouvoir tester pendant longtemps avec 5$)
- 5 minutes d'attention

## Étape 1 — Installer la bibliothèque

Dans un terminal :

```bash
pip install anthropic
```

Si ça râle avec `error: externally-managed-environment` (Linux récent), utilise un venv :

```bash
python3 -m venv venv
source venv/bin/activate
pip install anthropic
```

## Étape 2 — Mettre ta clé API en variable d'environnement

**Ne jamais coller ta clé dans le code Python.** Elle finit sur GitHub, scannée, volée, et facturée.

Dans le même terminal :

```bash
export ANTHROPIC_API_KEY="sk-ant-api03-..."
```

(Remplace par ta vraie clé. Elle commence toujours par `sk-ant-`.)

Cette commande ne vaut que pour la session terminal courante. Pour rendre ça permanent, ajoute la ligne à la fin de ton `~/.bashrc` ou `~/.zshrc`.

## Étape 3 — Le code

Crée un fichier `main.py` à côté de ce README, avec le contenu suivant :

```python
"""
Mon premier appel API Anthropic.
Posons une question à Claude et affichons la réponse.
"""
import anthropic

# Le client lit automatiquement ANTHROPIC_API_KEY dans l'environnement
client = anthropic.Anthropic()

# La question qu'on pose à Claude
question = "Explique-moi en 3 phrases ce qu'est une API, à un médecin de 50 ans."

# L'appel — c'est ici que la magie se passe
reponse = client.messages.create(
    model="claude-haiku-4-5-20251001",  # modèle le moins cher pour démarrer
    max_tokens=300,                      # limite la longueur de la réponse
    messages=[
        {"role": "user", "content": question}
    ]
)

# Affiche la réponse
print("=== Question ===")
print(question)
print()
print("=== Réponse de Claude ===")
print(reponse.content[0].text)
print()

# Trace le coût (Haiku 4.5 = $1/MTok input, $5/MTok output)
cout = (reponse.usage.input_tokens * 1.0 + reponse.usage.output_tokens * 5.0) / 1_000_000
print(f"=== Coût ===")
print(f"Input : {reponse.usage.input_tokens} tokens")
print(f"Output : {reponse.usage.output_tokens} tokens")
print(f"Total : {cout:.6f} $ (environ {cout * 10:.4f} MAD)")
```

## Étape 4 — Lancer

```bash
python3 main.py
```

Tu devrais voir s'afficher :
- Ta question
- La réponse de Claude (3 phrases sur l'API)
- Le coût exact en dollars (et en dirhams, par habitude marocaine)

**Voilà. Tu viens de faire ton premier appel API.** Bienvenue dans le club.

## Ce que tu viens de faire, en clair

| Ligne | Ce que ça fait |
|---|---|
| `import anthropic` | Charge la bibliothèque officielle Anthropic en Python |
| `client = anthropic.Anthropic()` | Crée un "client" — une connexion vers l'API Anthropic. Il lit ta clé tout seul. |
| `client.messages.create(...)` | Envoie ta question. C'est UN appel HTTP qui va et revient. |
| `model="claude-haiku-4-5..."` | Quel modèle tu veux. Haiku 4.5 est le moins cher. Sonnet et Opus sont plus chers mais plus malins. |
| `max_tokens=300` | Limite max de la réponse, pour ne pas exploser le coût |
| `messages=[...]` | La conversation. Ici une seule question, mais tu peux mettre des dizaines de tours. |
| `reponse.content[0].text` | Le texte de la réponse de Claude |
| `reponse.usage.*` | Combien de tokens ont été consommés (et donc combien ça a coûté) |

## Erreurs courantes

### `anthropic.AuthenticationError`
Ta clé API n'est pas reconnue. Vérifie :
- Qu'elle est bien dans l'environnement : `echo $ANTHROPIC_API_KEY` doit afficher `sk-ant-...`
- Qu'elle n'a pas d'espace ou de retour à la ligne dans la valeur
- Qu'elle n'a pas été révoquée sur console.anthropic.com

### `anthropic.RateLimitError`
Trop d'appels en peu de temps, ou ton compte n'a pas assez de crédit. Va sur [console.anthropic.com](https://console.anthropic.com/) → Billing → ajoute du crédit.

### `ModuleNotFoundError: No module named 'anthropic'`
Le `pip install anthropic` n'a pas marché. Tu n'as peut-être pas activé ton venv (`source venv/bin/activate`), ou tu utilises un autre Python que celui où tu as installé.

## Pour aller plus loin

- **Change la question** : remplace la variable `question`, relance.
- **Change le modèle** : essaie `claude-sonnet-4-6` ou `claude-opus-4-7`. Compare les réponses et les coûts.
- **Ajoute un system prompt** : passe `system="Tu es un médecin urologue à Fès qui explique les choses simplement"` dans `client.messages.create(...)`.
- **Tente une vraie conversation** : appelle deux fois, en mettant la première réponse dans `messages` avec `role="assistant"`.

## Prochain tuto

[02 — Ton premier MCP server](../09-first-mcp-server/) : passer du script qu'on lance à la main à un agent que Claude peut piloter tout seul.
