> 🇬🇧 **English version**: [README.en.md](README.en.md)

# 02 — Qu'est-ce qu'un agent IA, vraiment ?

**Difficulté** : 🟢 Débutant  |  **Durée** : 20 min de lecture

> Le mot "agent" est utilisé pour tout et son contraire. Un chatbot, un assistant, un workflow no-code, un script Python qui appelle une API — tout ça se fait appeler "agent IA" en ce moment. Ce tuto coupe le bruit et te donne une définition précise et utilisable.

---

## Pourquoi ce tuto existe

Quand j'ai commencé, je voyais passer le mot "agent IA" partout. Sur LinkedIn, dans les pubs, dans les vidéos YouTube. Personne ne définissait jamais ce que ça voulait dire concrètement.

Au bout de quelques semaines, j'ai compris que **le même mot recouvre quatre réalités différentes**, et que c'est cette confusion qui fait que les débutants ne savent pas par où commencer. Si je te dis *"construis un agent"* et que tu penses à une chose alors que je pense à une autre, on perd du temps.

Ce tuto remet de l'ordre. Avec des exemples concrets, pour que tu saches **où tu veux aller**.

---

## Quatre niveaux que les gens appellent "agent"

### Niveau 1 — Le chatbot

Tu poses une question, le système répond. Une fois. Pas de mémoire entre les sessions, pas de rôle clair, pas d'objectif.

**Exemples** : Claude sur claude.ai sans contexte particulier. ChatGPT pour une question ponctuelle. Le widget de support sur un site qui répond aux questions fréquentes.

**Caractéristique** : c'est *transactionnel*. Question → réponse. Fin.

C'est utile, mais **ce n'est pas vraiment un agent**. C'est un correspondant à qui tu poses des questions.

### Niveau 2 — L'agent à rôle (chat structuré)

Tu donnes à Claude un **rôle précis** avec des règles et un format. Il ne répond plus en généraliste, il répond dans son rôle.

**Exemple concret** : tu colles à Claude un texte qui dit *"Tu es l'assistant de rédaction de mes CR médicaux. Voici tes règles..."*. À partir de là, dans la conversation, il joue ce rôle. Tu lui donnes tes notes brutes, il te sort un CR formaté selon tes règles. Tu ne lui redemandes pas comment faire — tu lui donnes la matière première et il applique.

**Caractéristique** : c'est *contextuel*. Le rôle persiste pendant toute la conversation. Tu n'as pas à réexpliquer.

**C'est déjà un agent**, dans le sens utile du terme. Et **tu peux le construire dès aujourd'hui, sans une ligne de code**. C'est exactement le sujet des tutos 03, 04 et 05 de ce repo.

### Niveau 3 — L'agent automatisé (code + API)

Tu transformes le rôle en **code Python qui tourne tout seul**. Plus besoin d'ouvrir une conversation, de copier-coller, d'attendre. Le code prend une entrée (un PDF qui arrive, une heure qui sonne, un message reçu), appelle Claude via l'API, traite la sortie, et passe à la suite.

**Exemple concret** : un script qui surveille un dossier `/incoming/`. Dès qu'un PDF arrive, il l'OCRise, demande à Claude d'identifier le type de document, classe le fichier, met à jour une base, et notifie sur WhatsApp. Tout ça sans intervention humaine.

**Caractéristique** : c'est *autonome*. L'agent tourne pendant que tu fais autre chose ou que tu dors.

**C'est l'objectif des Parties 2 et 3 de ce repo** (tutos 07 à 11). C'est ce qu'on construit avec Python + l'API Anthropic + éventuellement un MCP server.

### Niveau 4 — L'agent multi-outils avec décisions complexes

L'agent automatisé devient **agent qui décide**. On lui donne une boîte à outils (lire des fichiers, requêter une base, envoyer des messages, exécuter du code), et il choisit lui-même quels outils utiliser, dans quel ordre, pour atteindre un objectif.

**Exemple concret** : tu dis à l'agent *"fais-moi le point de la matinée"*. L'agent décide tout seul d'appeler ton outil de lecture des logs serveurs, puis ton outil de lecture de calendrier, puis ton outil de calcul des coûts API, puis il te formule une synthèse cohérente.

**Caractéristique** : c'est *agentique* au sens fort. L'agent choisit le chemin, pas toi.

**C'est l'horizon de la Partie 4 et au-delà** dans ce repo.

---

## Pourquoi cette progression a du sens

Beaucoup de débutants veulent commencer **directement au niveau 4**. C'est tentant — c'est ce qu'on voit dans les démos sur LinkedIn. Mais c'est presque toujours une erreur, pour trois raisons :

### Raison 1 — Tu ne sais pas encore ce que tu veux

Au niveau 4, l'agent décide. Encore faut-il que **tu** saches précisément quoi décider. Si tu n'as pas formulé tes règles, tes critères, tes contraintes (niveau 2), l'agent prend des décisions au pif et tu n'as aucune idée de pourquoi.

### Raison 2 — Tu ne sais pas diagnostiquer ce qui plante

Quand un agent automatisé multi-outils foire, tu as **dix sources possibles** : prompt mal écrit, outil qui crashe, donnée corrompue, modèle qui hallucine, code qui plante, API qui timeout, base qui répond mal, etc. Si tu n'as jamais maîtrisé le niveau 2, tu n'as pas le réflexe de poser la bonne hypothèse.

### Raison 3 — Tu construis du fragile

Un agent qui tourne tout seul (niveau 3 ou 4) **doit** respecter les 4 piliers de la solidité (observabilité, fiabilité, sécurité, déploiement — c'est le tuto 08 du repo). Si tu commences direct au niveau 3 sans avoir compris ces piliers, tu construis un truc qui marche en démo et qui plante en silence le jour où tu n'es pas devant ton écran.

---

## La bonne progression — celle que j'ai vraiment suivie

```
Niveau 1  →  Niveau 2  →  Niveau 3  →  Niveau 4
chatbot      rôle structuré     agent code         agent multi-outils
                  ↓                  ↓                     ↓
            (tutos 03-05)      (tutos 06-12)        (tutos 09 et au-delà)
            sans code          avec Python          avec MCP/outils
```

**Niveau 1 → Niveau 2** : tu apprends à formaliser un rôle. C'est ce que tu fais avec un brief + un CLAUDE.md (tutos 03 et 04). **Tu peux le faire dès aujourd'hui, en chat, sans rien installer.**

**Niveau 2 → Niveau 3** : quand ton rôle est stable et que tu te surprends à le réutiliser tous les jours, tu le mets en code. C'est le passage à l'API (tutos 06 et 07). Tu écris ton premier script Python qui fait la même chose que ce que tu faisais en chat — mais automatiquement.

**Niveau 3 → Niveau 4** : quand ton code tourne bien et que tu veux que l'agent prenne des décisions complexes, tu lui donnes des outils via MCP (tuto 09). Là, tu deviens un orchestrateur d'agents — pas juste un exécutant.

---

## Concrètement, qu'est-ce qu'on appelle "agent" dans ce repo ?

Dans tous les tutos de ce repo, quand je dis "agent", je parle **au minimum d'un niveau 2** : Claude avec un rôle structuré, des règles, un format de sortie attendu. Pas un chatbot général.

À partir de la **Partie 2** (tuto 07), les "agents" sont du niveau 3 : du code Python qui tourne tout seul. C'est ce que les développeurs appellent souvent "agent" sans préciser.

À partir de la **Partie 3** (tuto 09), les agents peuvent **utiliser des outils** : MCP servers, appels HTTP, accès base. C'est le niveau 4 émergent.

---

## Faux amis et confusions à éviter

### "ChatGPT est un agent"
Non. C'est un chatbot (niveau 1) sur lequel tu peux construire un agent (niveau 2+). Le système d'instructions personnalisées d'OpenAI te permet de monter au niveau 2 sans code — c'est l'équivalent d'un brief.

### "Tout LLM appelé en boucle est un agent"
Pas forcément. Si tu mets Claude dans une boucle qui demande la même chose 100 fois, c'est **un script qui appelle 100 fois Claude**, pas un agent. Un agent au sens utile, c'est une boucle où le LLM **décide** quelque chose qui influence la prochaine itération.

### "Sans MCP, ce n'est pas un agent"
Faux. Tu peux avoir un excellent agent niveau 3 sans MCP, juste avec l'API et du code Python. MCP est utile quand tu veux que Claude pilote ton environnement (lire des fichiers, requêter une base, exécuter des commandes) **sans que tu aies à coder chaque interaction**.

### "Un workflow n8n/Make est un agent"
C'est un agent niveau 2-3 selon la complexité. Les outils no-code te permettent d'automatiser, mais ils ont leurs limites : moins de contrôle fin sur le prompt, traçabilité limitée, coût souvent plus élevé qu'un script Python. Pour des cas simples, c'est bien. Pour de la production sérieuse, le code reprend l'avantage.

---

## La question que tu dois te poser pour ton premier agent

Avant de te lancer, réponds honnêtement :

1. **À quel niveau je veux aller ?** (sois honnête : la plupart des cas utiles s'arrêtent au niveau 2 ou 3)
2. **Combien de temps je peux investir ?** (niveau 2 : quelques heures. Niveau 3 : quelques jours. Niveau 4 : quelques semaines.)
3. **Quel cas concret je veux résoudre ?** (pas "un agent IA en général". Un cas précis : *"automatiser mes CR de consultation"*, *"trier mes mails clients par catégorie"*, *"générer un rapport hebdo à partir de mes données"*.)

Si tu as ces trois réponses claires, tu sais par quel tuto commencer.

Si tu n'as pas encore de réponse, **commence par le tuto 03**. Choisis n'importe quelle tâche que tu fais régulièrement et qui te frustre, et formalise-la en brief. Tu apprendras énormément, sans risque, sans coût.

---

## Récap mémorisable

> Quatre niveaux : **chatbot** (général, sans rôle), **agent à rôle** (Claude avec un brief, en chat), **agent automatisé** (du code Python qui appelle l'API), **agent multi-outils** (l'agent choisit ses outils). Dans ce repo, "agent" = niveau 2 minimum. Tu progresses dans l'ordre — passer le niveau 2 sans le maîtriser, c'est construire du fragile.

---

## Pour aller plus loin

- **Tuto 03 — Construire ton premier brief** : monter au niveau 2 concrètement, sans code
- **Tuto 06 — Quand et pourquoi passer à l'API ?** : le bon moment pour passer au niveau 3

---

[← Retour au sommaire](../README.md)
