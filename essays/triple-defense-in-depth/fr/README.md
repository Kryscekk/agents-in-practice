# Gouvernance d'agents IA : comment j'ai construit une triple défense en profondeur pour mes agents en production

*Brouillon v0.1 — 2026-05-15*

---

## 1. Le moment PocketOS

Le 25 avril 2026, PocketOS — une SaaS éditrice de logiciels pour loueurs de voitures — a perdu l'intégralité de sa base de données de production. L'agent de codage IA responsable tournait sur Claude Opus 4.6, le modèle phare d'Anthropic à l'époque, intégré via Cursor. L'agent avait une tâche routinière dans un environnement de staging. Il a rencontré une incohérence d'identifiants. Il a décidé, de sa propre initiative, de « régler » le problème en supprimant un volume Railway. Il a trouvé un token d'API dans un fichier sans rapport avec sa tâche, l'a utilisé pour exécuter une seule mutation GraphQL, et la base de production a disparu.

Ça a pris 9 secondes.

Railway stockait les backups niveau-volume dans le même volume que les données. Quand le volume a été effacé, les backups l'ont été aussi. Le backup le plus récent récupérable datait de trois mois.

Quand le fondateur Jer Crane a demandé au modèle ce qui s'était passé, la réponse ressemblait à une confession :

> « NEVER FUCKING GUESS! — and that's exactly what I did. I guessed instead of verifying. I ran a destructive action without being asked. I didn't understand what I was doing before doing it. »

Le post de Crane sur X a fait 6,5 millions de vues. Pas parce qu'on s'étonne qu'un modèle de langage parte en vrille, mais parce que dans ce cas précis, **les garde-fous n'existaient pas**. Le token utilisé avait été créé pour gérer des noms de domaine, mais l'API GraphQL de Railway accordait à chaque token des permissions étendues à toutes les opérations, y compris destructrices. Pas de confirmation pour `volumeDelete`. Aucun code déterministe entre le raisonnement du modèle et l'appel destructeur.

Ce n'est pas une histoire d'IA devenue folle. C'est une histoire d'**architecture manquante**. L'agent était la cause directe. La cause réelle était une chaîne de choix de conception qui ont laissé une seule décision du modèle atteindre un endpoint destructeur sans rien entre les deux.

C'est de cette chaîne que je veux parler — parce que je fais aussi tourner des agents IA en production, et ce que j'ai passé deux ans à construire, c'est essentiellement une pile de barrières qui rendent un PocketOS-en-9-secondes structurellement impossible.

---

## 2. Pourquoi ça compte pour les domaines hors-code

Je ne fais pas d'agents de codage. Je suis urologue au Maroc et j'ai appris Python tout seul parce qu'aucun logiciel à acheter ne correspondait à comment je travaille. Le code que je fais tourner en prod — environ 104 000 lignes, sur un seul VPS à 5€/mois — supporte quatre systèmes : une plateforme d'automatisation pour mon cabinet médical, un système de raisonnement spécialisé qui produit des estimations de valeur fondamentale pour environ 75 entreprises cotées, un tracker de finances personnelles, et un labo R&D. C'est le système de raisonnement financier qui est le plus pertinent ici, à cause de ce que font vraiment ses agents.

Quand mes agents échouent, ils n'effacent rien. Ils produisent **des scores faux**. Une entreprise mal classée reçoit une estimation de valeur trompeuse. L'estimation déclenche un signal d'achat ou de vente. Le signal est lu. Du capital est alloué sur une fausse prémisse. Des mois plus tard, la position s'est aggravée en perte qu'on ne peut pas retracer à un bug unique, parce que les données étaient techniquement correctes — seule l'interprétation était fausse.

Dans les agents de codage, le dégât est instantané. Dans les agents de raisonnement, le dégât est une **trajectoire**.

Cette distinction compte parce que la conversation actuelle sur la sécurité des agents est dominée par des incidents type PocketOS. Les correctifs que les éditeurs s'empressent de livrer — confirmations avant opérations destructrices, tokens scopés, sandboxing — sont de vraies améliorations pour cette classe de risque. Mais ils n'adressent pas la classe plus lente, plus dure : l'agent qui n'a rien écrit de dangereux dans une base mais qui a quand même empoisonné le puits parce que ce qu'il a écrit était une recommandation construite sur un raisonnement insuffisant.

C'est vrai aussi pour l'IA médicale, juridique, conseil patrimonial, due-diligence. Le danger n'est pas un moment d'action catastrophique unique. C'est la dérive cumulative de sorties conséquentes qui paraissent toutes correctes prises isolément.

Les patterns décrits dans la suite de cet article ont été construits pour ce deuxième type de risque. Ils gèrent aussi la classe PocketOS, presque comme effet de bord — parce qu'une fois qu'il devient impossible au modèle d'agir unilatéralement, les deux types sont couverts. Mais le problème que je voulais résoudre à l'origine n'était pas « et si le modèle effaçait ma base ». C'était « et si le modèle donnait une réponse confiante mais fausse que personne n'attrape pendant trois mois ».

La structure a trois couches. Aucune n'est nouvelle prise isolément. La combinaison, appliquée à des contextes hors-code, c'est ce que je n'ai pas trouvé écrit ailleurs.

Les trois couches :

- **Isolation horizontale** — quatre instances Claude séparées, avec des rôles, des permissions et des zones d'impact différents.
- **Ordonnancement vertical** — une machine à états bloquante qui rend physiquement impossible le lancement d'une phase avant ses prérequis.
- **Traçabilité longitudinale** — chaque appel au modèle, chaque décision intermédiaire, chaque cross-check stocké de manière à rendre la chaîne entière auditable des mois plus tard.

Je vais les détailler dans cet ordre, avec le vrai code que je fais tourner en prod. Je serai aussi honnête sur les cas où ce pattern est du sur-ingénierie, sur les outils existants (Langfuse, pytransitions, les sous-agents Claude Code) qui en font des morceaux mieux que moi, et sur les endroits où l'architecture repose sur de la discipline humaine qu'aucun code ne peut faire respecter.

---

## 3. Couche 1 — Isolation horizontale : quatre instances Claude aux zones d'impact différentes

La première couche, c'est de découper « l'agent IA » en plusieurs processus indépendants, chacun avec sa propre session Claude, chacun avec un périmètre d'action nettement différent.

En production en ce moment, quatre instances Claude tournent en parallèle :

| Instance | Processus | Périmètre | Peut écrire en base ? |
|---|---|---|---|
| **1. Claude conversationnel** | Web/mobile Anthropic + mes serveurs MCP | Architecture, revue de code, validation, décision | Non. Ne produit jamais d'avis sur une entreprise particulière. N'écrit nulle part. |
| **2. Claude Code** | Utilisateur Linux dédié, terminal uniquement | Exécution lourde : refactos, batchs, écriture de fichiers dans son sandbox | Non. Ne push jamais un commit Git. N'écrit jamais dans la base de production. |
| **3. Claude bot Telegram** | Daemon Python long-running, clé API séparée | Interface conversationnelle : lit du langage naturel, choisit des tools, renvoie des réponses formatées | Non. A exactement 13 tools en lecture seule et 2 tools admin. **Aucun tool d'écriture sur les tables métier n'existe.** |
| **4. Claude agent pipeline** | Sous-processus instancié par phase, clé API séparée | Le vrai travail de raisonnement : classifier, estimer Ke et croissance, calculer la juste valeur, valider | **Non, encore une fois.** Chaque agent produit du JSON strict via `tool_use`. Python parse ce JSON, exécute des `assert` sur chaque champ, et seulement après ça écrit en base. |

Le même fait tient dans les quatre lignes : **aucune instance Claude n'écrit directement dans une table de production**. Les écritures sont faites par du code Python déterministe, après validation du JSON.

Ça paraît évident. Ça ne l'est pas. Dans l'architecture PocketOS, l'agent Cursor pouvait composer une commande `curl`, trouver un token dans un fichier, et appeler l'endpoint GraphQL de Railway. Le chemin entre le raisonnement du modèle et l'endpoint destructeur passait par zéro ligne de code validant. Juste un shell. C'est ça, le défaut d'architecture.

Le découpage en quatre instances me donne aussi une propriété à laquelle je tiens plus que prévu : **un rayon d'impact borné si une instance se comporte mal**.

- Si Claude conversationnel hallucine une juste valeur pendant une discussion, l'hallucination reste dans notre chat. Elle n'atteint jamais la base.
- Si Claude Code se fait jailbreaker ou social-engineer pour lancer `rm -rf`, le pire qu'il puisse faire, c'est détruire son propre sandbox. Le code de prod vit ailleurs.
- Si le bot Telegram est compromis par une injection de prompt dans un message, il a 13 tools en lecture seule à abuser — et un quatorzième qui déclenche un pipeline. Pas de tool pour écrire dans `scores`, pas de tool pour écrire dans `score_model`, pas de tool pour écrire dans `agent_*_state`. Ces tables n'existent simplement pas dans son monde.
- Si un agent du pipeline — celui le plus directement connecté aux écritures — renvoie un score faux, le validateur Python exécute des `assert` sur chaque champ. L'assertion échoue, l'agent est marqué `FAILED`, et la sortie fautive ne sera jamais commitée.

Voici le registry réel des tools du bot Telegram, abrégé et anonymisé :

```python
TOOLS = [
    {"name": "get_entity",      "description": "Read a single entity's full record."},
    {"name": "list_by_signal",  "description": "List entities matching a given signal level."},
    {"name": "list_by_category","description": "List entities in a given category."},
    {"name": "get_watchlist",   "description": "Return the current opportunity watchlist."},
    {"name": "get_overview",    "description": "High-level distribution of signals."},
    {"name": "get_known_issues","description": "List methodological issues currently flagged."},
    # ... 7 more read-only tools

    # The ONLY two action tools — neither writes to business tables:
    {"name": "configure_model", "description": "Admin: change which Claude model an agent uses."},
    {"name": "trigger_analysis","description": "Spawn an isolated analysis subprocess. Returns immediately."},
]
```

Le code de dispatching qui résout chaque appel à une fonction Python autorisée est juste un dictionnaire. Si Claude tente d'appeler un tool absent de ce dictionnaire, il reçoit en retour `{"error": "Unknown tool"}` et continue sa conversation comme si la fonction n'existait pas. Ce qui est exactement le cas, d'ailleurs.

**Le bot peut être jailbreaké, manipulé socialement, ou simplement halluciner — et il ne peut toujours pas écrire dans la base. Pas parce qu'on lui demande de ne pas le faire. Parce que le tool n'existe pas.**

---

## 4. Couche 2 — Ordonnancement vertical : la machine à états qui refuse de sauter une étape

L'isolation horizontale règle la question « qui peut faire quoi ». Elle ne règle pas « dans quel ordre ». C'est le rôle de la deuxième couche.

Un pipeline de raisonnement n'est pas une suite d'appels indépendants. C'est une chaîne où chaque étape dépend de la précédente. Si le classifieur n'a pas tourné, l'estimateur n'a rien sur quoi travailler. Si l'estimateur a sauté une étape, le calcul de juste valeur opère sur du n'importe quoi. Si le validateur tourne avant qu'il n'y ait rien à valider, on obtient un « approuvé avec confiance » sur du vide.

Le fix intuitif, c'est « l'orchestrateur appelle les agents dans l'ordre ». Ça marche jusqu'au jour où l'orchestrateur a un bug, ou jusqu'au jour où quelqu'un appelle une méthode directement pour débogguer, ou jusqu'au jour où un retry partiel redémarre au milieu sans rétablir le contexte. Donc j'ai rendu **impossible** le saut de phase, en faisant respecter l'ordre dans la classe elle-même.

La classe pipeline a douze états séquentiels :

```
init → loaded → analyzed → characterized → contextualized
     → classified → ke_set → g_set → estimated
     → valued → checked → written
```

Chaque méthode déclare l'état requis et l'état vers lequel elle avance. Si l'état actuel ne correspond pas, Python crashe. Voici tout le mécanisme d'enforcement, cinq lignes :

```python
def _advance_state(self, required, next_state):
    """Verify the required state(s) and advance."""
    allowed = (required,) if isinstance(required, str) else required
    if self.state not in allowed:
        raise AssertionError(
            f"State required: {allowed}, current state: {self.state}"
        )
    self.state = next_state
```

Et voici à quoi ça ressemble en usage, dans la méthode qui calcule la juste valeur :

```python
def compute_fair_value(self, multiple: float, justification: str) -> float:
    self._advance_state('estimated', 'valued')   # crash si pas dans 'estimated'
    self._assert_justif(justification, threshold=30)
    # ... logique métier
```

Le pattern est uniforme sur les douze phases. Chaque méthode commence par `self._advance_state(...)`. Chaque méthode valide ses arguments avant de faire quoi que ce soit. **Il n'existe aucun chemin dans le code qui te laisse appeler `compute_fair_value` avant que l'entreprise n'ait été classifiée.** Python lève `AssertionError`, la pile d'appels remonte.

C'est volontairement minimal. Il existe des bibliothèques Python de machine à états mature — `pytransitions` est l'évidente, avec dix ans d'existence, des décorateurs, des callbacks, des hooks, des conditions, des state-charts hiérarchiques. Pour la plupart des cas où on veut vraiment une machine à états, ces libs sont meilleures que ce que j'ai. Elles donnent de la composabilité, des régions parallèles, des états historiques. Choses utiles.

Je ne les ai pas utilisées parce que pour ce pipeline, les exigences sont étroites :

- Pas de transitions en arrière. Une fois une phase faite, on ne défait pas ; on lance une nouvelle analyse.
- Pas de branches conditionnelles. L'ordre est le même pour toutes les entreprises.
- La persistance doit être custom de toute façon, parce que je veux pouvoir reprendre après un crash sans repayer les appels à l'API Claude qui ont déjà réussi.

Une vérification de cinq lignes qui vit à l'intérieur de chaque méthode est plus lisible qu'un diagramme de transitions dans un autre fichier. Quand tu lis `compute_fair_value`, tu vois immédiatement quel état elle exige, en ligne 1. Tu n'as pas à sauter dans une table de transitions ailleurs pour le savoir.

Je ne prétends pas que c'est le bon choix pour tout projet. Je dis que la bonne quantité de framework pour un pipeline strictement linéaire, c'est à peu près zéro.

### Le détail de la reprise après crash

Chaque phase, après avoir réussi, écrit son état dans une table SQLite dédiée par agent. Le schéma est le même pour les six agents du pipeline :

```sql
CREATE TABLE agent_<role>_state (
    entity_id     TEXT PRIMARY KEY,
    status        TEXT NOT NULL,    -- NEW | RUNNING | DONE | FAILED
    started_at    TEXT,
    error_message TEXT
    -- ... champs métier spécifiques à cet agent
);
```

Trois helpers gèrent la mécanique :

```python
def mark_running(db_path, table, entity_id):
    # idempotent: INSERT OR IGNORE puis UPDATE status='RUNNING'

def mark_failed(db_path, table, entity_id, error):
    # UPDATE status='FAILED', error_message=tronqué

def read_status(db_path, table, entity_id) -> Optional[str]:
    # retourne 'DONE' | 'RUNNING' | 'FAILED' | 'NEW' | None
```

Si une analyse crashe en cours de route — coupure de courant, OOM, panne réseau pendant un appel à l'API Claude — le run suivant lit `read_status` pour chaque agent et saute ceux déjà marqués `DONE`. Seuls les agents échoués ou incomplets re-tournent. Ça économise de l'argent réel : chaque phase, c'est un ou deux appels à Claude Opus, et sur un portefeuille de 75 entreprises, ça additionne.

Ça veut aussi dire que la machine à états n'est pas qu'une vérification in-memory. C'est un enregistrement durable de ce que le système a et n'a pas fait, que je peux interroger des mois plus tard quand je veux savoir « est-ce que le validateur a vraiment tourné pour cette entreprise ce jour-là, ou est-ce qu'on a sauté ? »

Tu ne sautes pas une phase. Python crashe. Et quand le monde crashe autour de Python, les tables SQLite se souviennent d'où on en était.

---

## 5. Couche 3 — Traçabilité longitudinale : chaque décision est enregistrée

Les deux premières couches te disent ce que le système peut faire et dans quel ordre. Elles ne te disent pas, après coup, ce qu'il a vraiment fait. C'est le rôle de la troisième couche.

Chaque appel à Claude dans ce système écrit une ligne dans une table `claude_calls` :

```sql
CREATE TABLE claude_calls (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    ts             TEXT NOT NULL DEFAULT (datetime('now')),
    agent_name     TEXT NOT NULL,    -- 'classifier', 'estimator', 'valuator', 'validator'...
    entity_id      TEXT,
    trace_id       TEXT,             -- groupe les retries d'un même appel logique
    batch_id       TEXT,             -- groupe tous les appels d'une analyse complète
    model          TEXT NOT NULL,
    input_tokens   INTEGER DEFAULT 0,
    output_tokens  INTEGER DEFAULT 0,
    cache_read     INTEGER DEFAULT 0,
    cache_write    INTEGER DEFAULT 0,
    duration_ms    INTEGER DEFAULT 0,
    cost_usd       REAL DEFAULT 0.0,
    stop_reason    TEXT,
    attempt        INTEGER DEFAULT 1,
    error_message  TEXT
);

CREATE INDEX idx_claude_calls_entity   ON claude_calls(entity_id);
CREATE INDEX idx_claude_calls_trace_id ON claude_calls(trace_id);
CREATE INDEX idx_claude_calls_batch_id ON claude_calls(batch_id);
```

L'insertion arrive à la toute fin du wrapper d'appel Claude, succès ou échec. Si l'appel a renvoyé un résultat, ce résultat a déjà été parsé et validé ; la ligne entre avec `stop_reason='end_turn'`. Si l'appel a échoué à la validation ou a levé une exception, la ligne entre quand même, avec `error_message` rempli. Rien ne passe à travers.

À cette heure, il y a **532 lignes** dans `claude_calls`, couvrant **75 entreprises** et **6 batches d'analyses complètes**. C'est la piste d'audit.

La table compagne est `decisions`, qui contient le résultat final de chaque analyse — l'explication narrative, pas juste le chiffre :

```sql
CREATE TABLE decisions (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_id      TEXT NOT NULL,
    decision_date  TEXT NOT NULL,
    score          REAL,
    market_value   REAL,
    signal         TEXT,
    method         TEXT,
    multiple_used  REAL,
    earnings_used  REAL,
    discount_rate  REAL,
    growth_rate    REAL,
    confidence     TEXT,
    reasoning      TEXT NOT NULL,   -- narrative justification
    cross_checks   TEXT,            -- JSON: alternative methods + deltas
    sources        TEXT
);
```

Le champ `cross_checks` est la partie à laquelle je ne pourrais pas renoncer. Pour chaque juste valeur que le système produit, il ne stocke pas juste le chiffre — il stocke le résultat des méthodes de valorisation alternatives et les écarts entre elles. Une ligne typique ressemble à ça (anonymisée) :

```
entity_id:     "Company X"
score:         780.0
method:        "multiple × earnings"
signal:        "🟢 BUY"
confidence:    "Medium"
cross_checks:  "DDM = 629 DH | implicit PER = 692.0x | broker consensus = 884 DH | gap_to_consensus = -11.7%"
```

Cette seule ligne me dit : la méthode primaire a sorti 780, le modèle DDM a sorti 629, le PER implicite du marché est anormalement élevé (692x — le marché paie une croissance qu'on n'extrapole pas), et le consensus des grands brokers est à 884, soit 11,7% au-dessus de nous. Si quelqu'un me demande dans six mois pourquoi on a dit « acheter à 780 » alors que le marché s'est effondré à 600, je peux retrouver la ligne exacte, voir les cross-checks, et reconstituer ce qu'on savait et ce qu'on ne savait pas à cette date.

Les réévaluations sont **ajoutées**, pas écrasées. Company X a cinq lignes dans `decisions` sur avril : 795 (`Buy`, conviction haute), puis 884 (`Strong Buy`, conviction moyenne), puis encore 884, puis 806, puis 780 aujourd'hui. Chaque ligne porte ses propres `cross_checks` et son propre `reasoning` narratif. L'historique est la table.

Je ne prétends pas que c'est sophistiqué. Langfuse a un setup beaucoup plus mature — tracing multi-turn, versioning de prompts, LLM-as-judge, A/B testing de prompts, dashboards de coût, instrumentation OpenTelemetry. Si tu construis sérieusement des agents en prod et que tu n'as pas encore d'observabilité, installe `langfuse` et instrumente chaque appel Claude avant de faire quoi que ce soit d'autre. C'est gratuit en self-host et ça fait plus que ce que je viens de décrire.

Ce que j'ai, c'est la piste de provenance minimale viable, intégrée directement dans la base métier plutôt que dans un service d'observabilité séparé. Le compromis : moins joli, moins de richesse de querying, moins d'outillage standard. Le gain : quand je lance la même requête SQL que celle qui produit le rapport visible par l'utilisateur, j'ai accès complet au raisonnement qui a produit chaque chiffre, dans la même requête, dans la même base. Pas de second système à maintenir vivant.

---

## 6. Le pattern critique : Claude ne touche jamais la base

Tout ce qui précède dans les trois sections d'avant repose sur une seule règle : **l'API Claude n'écrit jamais dans la base de production, ni directement ni indirectement**. Elle produit du JSON. Python parse le JSON, exécute des assertions sur chaque champ, et seulement ensuite commit.

Cette phrase en italique fait une ligne. C'est aussi celle que je défendrais le plus fermement contre la tentation de la relâcher.

Voici le flux, du début à la fin, quand le pipeline demande à Claude de classifier une entreprise :

1. Python construit le prompt et le schéma `tool_use` pour le classifieur.
2. Claude renvoie un objet JSON avec des champs comme `profile_primary`, `profile_secondary`, `thesis`, `justification`.
3. Python valide que `profile_primary` est dans la liste autorisée (lève `AssertionError` sinon), que `profile_secondary` est autorisé et compatible avec `profile_primary` (aucune paire interdite, lève sinon), que la justification fait au moins 30 caractères de texte plein, que la combinaison des deux profils n'est pas dans une liste de blocage hard-codée venant du document méthodologique.
4. Seulement après que toutes les assertions sont passées, Python exécute le SQL `INSERT INTO agent_classifier_state ...` avec les valeurs.

Si une assertion échoue, l'agent est marqué `FAILED`, le message d'erreur est loggé, et **aucune ligne n'est écrite dans la table métier**. Le pipeline n'essaie pas de « récupérer et écrire une version dégradée ». Il refuse de persister quoi que ce soit qui n'est pas passé la barrière.

Contraste avec PocketOS. Le raisonnement de l'agent Cursor a produit « je devrais appeler `volumeDelete` avec ce token ». Cette décision est devenue un appel `curl`. L'appel `curl` a atteint l'endpoint GraphQL de Railway. L'endpoint s'est exécuté. À chaque étape de cette chaîne, l'action destructrice était à une couche d'indirection plus proche de se produire. À aucune étape un code déterministe n'a refusé de traduire l'intention du modèle en action.

L'industrie de la sécurité a un nom pour cette distinction.

Les **soft guardrails** sont probabilistes — system prompts, project rules, « NEVER DELETE PRODUCTION DATA » écrit en majuscules. Ils dépendent de la décision du modèle de leur obéir. Le modèle peut les outrepasser lui-même s'il se convainc que ce cas particulier est une exception. PocketOS avait des soft guardrails. La configuration projet de Crane disait littéralement « NEVER FUCKING GUESS ». Le modèle a guessed quand même et s'est excusé après.

Les **hard boundaries** sont déterministes. Elles vivent en dehors de la boucle de raisonnement du modèle. Elles rendent certains résultats structurellement impossibles, indépendamment de ce que le modèle décide. Le modèle pourrait être parfait ou halluciner ; la hard boundary s'en fiche, parce qu'elle ne demande rien au modèle.

Ce que j'ai décrit plus haut — tools en lecture seule, absence de tool destructeur, assertions de machine à états, validateurs JSON avant persistance — c'est une pile de hard boundaries. Le modèle peut décider qu'il veut écrire une juste valeur de 9999 sans justification. La décision n'a pas d'implémentation. Python ne laisse pas passer l'assertion. Aucune ligne n'est écrite. Le modèle a atteint le mur.

C'est la partie que je construirais en premier si je redémarrais. Tout le reste — observabilité, traçabilité, choix de modèle par agent — c'est du confort. Le mur entre Claude et la base, c'est l'architecture.

---

## 7. Comparaison honnête avec les solutions existantes

Je veux passer une section à être honnête sur ce que ce pattern est et n'est pas, parce que j'ai lu trop de posts d'ingénierie qui présentent le choix de l'auteur comme évidemment meilleur que les alternatives. Il l'est rarement.

**Les sous-agents Claude Code** sont l'analogue officiel le plus proche de ce que j'ai construit. Anthropic les livre dans Claude Code : chaque sous-agent a son propre system prompt, sa propre liste de tools, ses propres permissions, et un Claude parent délègue le travail dedans une seule session. Pour des agents qui ont besoin de déléguer à l'intérieur d'un workflow de codage — explorer la base, lancer des tests, proposer un patch — les sous-agents sont excellents. Ils donnent la plupart des bénéfices d'isolation sans faire tourner quatre processus séparés.

Ce que les sous-agents ne donnent pas, c'est **l'isolation à travers des sessions, des processus, des clés API**. Les quatre instances que j'ai décrites ne sont pas des sous-agents-d'un-parent. Ce sont quatre clients Claude entièrement indépendants, tournant sur des horaires différents, avec des credentials différents, parlant à des tools différents, sur des utilisateurs Linux différents. Le bot Telegram continue à tourner pendant qu'aucune analyse n'est en cours. Les agents du pipeline n'existent que pour la durée d'une analyse. Claude conversationnel n'est au courant ni de l'un ni de l'autre. Pas de session partagée, pas de contexte partagé, pas de parent qui pourrait coordonner un contournement.

Si tes agents n'ont besoin de coordonner que dans une seule session, les sous-agents sont plus simples et probablement suffisants. Si tu as besoin d'agents long-running, indépendamment schedulés, authentifiés différemment, le pattern de cet article est plus proche de ce que tu veux.

**Langfuse** est le stack d'observabilité open-source pour applications LLM, environ 19 000 étoiles sur GitHub, licence MIT, self-hostable. Il donne du tracing multi-turn, du versioning de prompts, de l'évaluation LLM-as-judge, du tracking de coût, de l'instrumentation OpenTelemetry, de l'A/B testing, et une UI qui bat mes requêtes SQL à plate couture. Les tables `claude_calls` et `decisions` que j'ai décrites sont un tout petit sous-ensemble de ce que fait déjà Langfuse, avec moins d'ergonomie.

Ce que Langfuse ne remplace pas, c'est la partie **isolation et restriction de tools**. Langfuse observe ; il ne contraint pas. Si ton bot a un tool `delete_company`, Langfuse va docilement logger que le modèle l'a appelé et ce qui s'est passé. Le travail de hard boundary — s'assurer que ce tool n'existe pas en premier lieu — c'est ton job, indépendamment du stack d'observabilité.

La recommandation honnête : installe Langfuse, instrumente chaque appel Claude. Utilise le pattern de cet article pour le travail de permissions et de machine à états. Ils sont complémentaires, pas concurrents.

**pytransitions et python-statemachine** sont les bibliothèques Python de machines à états mature. Pour des machines avec transitions arrière, états hiérarchiques, régions parallèles, ou chaînes de callbacks complexes, elles sont meilleures que ce que j'ai. Le `_advance_state` de cinq lignes ne marche que parce que mon pipeline est strictement linéaire sans backtracking. Si ton agent de raisonnement a une boucle `RESEARCH ↔ DRAFT ↔ REVIEW`, tu veux une vraie lib FSM.

**Les Guardrails Railway post-PocketOS** ont ajouté des délais de confirmation avant les opérations API destructrices. C'est un soft guardrail dans la terminologie de cet article — l'action destructrice est toujours possible, juste retardée. Le vrai fix, c'est le scoping de tokens, que Railway n'offre toujours pas pour les comptes personnels en mai 2026. Si tu intègres un agent IA avec n'importe quel provider d'infra, vérifie quel scoping l'API supporte vraiment avant de te reposer sur des guardrails ajoutés après un incident.

**Le papier CoSAI Agentic Identity and Access Management** (mars 2026) pose les principes que ce pattern implémente concrètement : pas de privilège permanent, accès just-in-time scopé, couche de gouvernance en dehors de la boucle de raisonnement de l'agent. À lire si tu veux le cadrage formel plutôt que ma version.

---

## 8. Là où ce pattern est du sur-ingénierie

Un pattern qui résout le mauvais problème est pire qu'aucun pattern. Donc :

- **Agents de codage faisant des petits refactos.** Tu n'as pas besoin de quatre instances Claude. Tu as besoin d'un sandbox et d'une revue de code. Claude Code avec ses listes de permissions allow/deny par défaut suffit.

- **Side-projects et MVP.** Le coût de construire cette architecture dès le jour 1 est largement supérieur au coût d'un incident sur un système qui n'a pas encore de vrais utilisateurs. Construis le produit d'abord. Ajoute le mur autour de Claude après la première fois où un truc a mal tourné, ou après la première fois où la donnée d'un client aurait pu mal tourner.

- **Agents single-shot.** Un agent qui répond à une question et disparaît ne bénéficie pas de l'isolation multi-instances ; il n'y a rien à isoler. La machine à états et la traçabilité restent bon marché à garder, mais le découpage horizontal est overkill.

- **Tu n'as pas vraiment de données privilégiées.** Si le pire cas dans ton système, c'est « le bot renvoie une réponse périmée », tu résous le mauvais problème avec ça. C'est de l'invalidation de cache, pas de la gouvernance d'agents.

Il y a aussi deux limites du pattern lui-même que je veux rendre explicites.

D'abord, **la discipline humaine est irréductible**. Toute la pile au-dessus repose sur l'hypothèse que les quatre instances Claude ont vraiment des credentials séparés, des clés API séparées, des frontières de processus séparées. Si un mainteneur met la même `ANTHROPIC_API_KEY` dans les quatre fichiers `.env`, l'isolation est illusoire. Le pattern est appliqué par la configuration, pas par le type-checking de Python. Aucune garantie à la compilation.

Ensuite, **c'est de la défense en profondeur, pas de la vérification formelle**. Ça rend les accidents moins probables et contenus quand ils arrivent. Ça ne les rend pas impossibles. Un bug dans le validateur Python — disons une assertion qui ne vérifie pas vraiment ce que je croyais — laisserait silencieusement passer une valeur fausse. Je lance des tests sur les validateurs. Je les relis attentivement. Je ne prétendrais quand même pas que le système est prouvable safe. C'est une pile de barrières pratiques, pas une preuve de sécurité.

Si tu construis quelque chose où « probablement safe » ne suffit pas — dispositifs médicaux qui agissent sur des sorties IA, armes autonomes, quoi que ce soit qui touche un réseau électrique — ce pattern est nécessaire mais pas suffisant. Tu as aussi besoin de méthodes formelles, de redondance, et d'une organisation capable d'absorber une panne vérifiée-impossible. Rien de tout ça n'est dans le scope ici.

---

## 9. Récap

Trois couches entre Claude et une base de production qui contient quelque chose que je ne peux pas me permettre de perdre :

1. **Isolation horizontale.** Quatre instances Claude. Credentials différents, processus différents, tools différents. Celle qui parle aux utilisateurs n'a pas le tool pour écrire les données. Celle qui écrit les données n'a aucun contact avec les utilisateurs.

2. **Ordonnancement vertical.** Une machine à états bloquante à douze phases séquentielles. Les méthodes refusent de tourner hors d'ordre. Python crashe quand l'état est faux. SQLite se souvient d'où on en était après le crash.

3. **Traçabilité longitudinale.** Chaque appel Claude enregistré avec son coût, ses tokens, son batch_id, son trace_id, son message d'erreur. Chaque décision stockée avec ses cross-checks et son raisonnement narratif. Des mois plus tard, la chaîne reste lisible.

PocketOS a perdu sa base en 9 secondes parce que rien dans le chemin n'était déterministe. L'agent a décidé, le curl a tourné, l'API a exécuté. Aucun code déterministe entre.

**Le modèle peut être parfait. C'est le middleware qui compte. Construis le middleware déterministe en premier. Le modèle, c'est la partie facile.**
