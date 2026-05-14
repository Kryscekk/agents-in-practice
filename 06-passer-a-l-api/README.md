# 06 — Quand et pourquoi passer à l'API ?

**Difficulté** : 🟢 Débutant  |  **Durée** : 15 min de lecture

> Tu as un agent en chat qui marche. La question maintenant n'est plus *"comment faire mieux ?"* — c'est *"est-ce le bon moment pour automatiser ?"*. Ce tuto te donne les sept signaux qui répondent à cette question, et te prépare à la décision la plus structurante de ton parcours.

---

## Pourquoi ce tuto existe

J'ai vu trop de gens (et je m'inclus) passer à l'API trop tôt. Le résultat est toujours le même : tu te retrouves à déboguer du code Python pour un cas que tu maîtrisais à peine en chat. Tu perds une semaine à régler des problèmes techniques qui n'auraient pas existé si tu étais resté en chat.

À l'inverse, j'ai vu des gens rester en chat **trop longtemps** alors que leurs cas méritaient clairement de l'automatisation. Ils continuent à copier-coller manuellement leurs briefs deux fois par jour, et perdent au total plus de temps que ce que l'API leur ferait économiser.

Ce tuto te donne les **sept signaux concrets** qui te disent que c'est le bon moment. Si tu en coches 4 ou plus, vas-y. Si tu en coches 2 ou moins, attends.

---

## Les sept signaux qui disent "passe à l'API"

### Signal 1 — Tu fais la même tâche tous les jours, manuellement

Si tu te retrouves à copier-coller ton brief, à recoller un mail, à attendre la réponse, à exécuter l'action suggérée — **plusieurs fois par jour, tous les jours** — c'est mécanique. Du code peut faire ce truc à ta place.

Test : *"Cette semaine, combien de fois j'ai fait cette tâche manuellement ?"*. Si la réponse est **plus de 5 fois**, signal coché.

### Signal 2 — Tu veux que ça tourne pendant que tu dors (ou que tu consultes, ou que tu manges)

Certaines tâches sont **déclenchées par des événements** : un mail arrive, un fichier apparaît, une heure sonne, une donnée change. Si tu attends que ces événements se produisent pour traiter à la main, tu **perds** l'événement quand tu n'es pas devant ton écran.

Exemple typique : un scan de document qui arrive sur ton serveur à 14h pendant ta consultation de l'après-midi. Tu le verras à 19h, traité à 20h, envoyé à 21h. Si c'était automatique, ça serait fait à 14h01, et le client aurait sa réponse 6 heures plus tôt.

Test : *"Est-ce que ma latence de traitement humain me coûte quelque chose ?"*. Si oui (clients qui attendent, opportunités manquées, énervement de mes interlocuteurs), signal coché.

### Signal 3 — Tu veux intégrer à un autre système

Tu veux que le résultat de ton agent **arrive directement** dans ton CRM, ton agenda, ta base de données, ton outil de gestion de projet, ton bot WhatsApp. **Tu ne veux plus copier-coller.**

En chat, tu copies-colles à la main. En code, tu écris une fois la connexion et c'est fait pour toujours.

Test : *"Est-ce que je rêve d'un bouton magique qui prendrait la sortie de Claude et l'enverrait directement ailleurs ?"*. Si oui, signal coché.

### Signal 4 — Tu veux tracer les coûts précisément

En chat (Claude.ai abonnement), tu paies un forfait. Tu ne sais pas combien chaque tâche te coûte vraiment. Pour une utilisation perso, c'est OK.

Dès que tu veux **vendre** ton agent à des clients, **mesurer la rentabilité** d'un workflow, **optimiser** le rapport coût/qualité (Haiku vs Sonnet vs Opus), il te faut le code. L'API te donne un coût précis pour chaque appel — entrée, sortie, modèle. Tu peux logger tout ça (et c'est exactement le tuto 12 sur le cost tracker).

Test : *"Est-ce que quelqu'un d'autre que moi va utiliser cet agent, ou est-ce que je veux savoir précisément combien il me coûte ?"*. Si oui, signal coché.

### Signal 5 — Tu veux versionner ta méthode (pour de vrai)

En chat, tu as un dossier avec tes briefs en `.md`. Si tu modifies un brief par erreur, tu perds la version précédente (sauf si tu fais tes sauvegardes à la main, ce que personne ne fait vraiment).

En code, tu mets tes briefs dans un repo Git. Chaque modification est tracée, chaque version est récupérable, tu peux faire des branches pour expérimenter sans casser ta version qui marche.

Test : *"Mon brief actuel est-il un actif que je ne veux pas perdre ?"*. Si oui, signal coché.

### Signal 6 — Tu fais déjà du code (même un peu)

Si tu as déjà bidouillé du Python (même 100 lignes), si tu sais ce qu'est un terminal, si tu as déjà installé une bibliothèque avec `pip`, **passer à l'API te coûtera quelques jours, pas quelques semaines**.

Si tu n'as **jamais** touché à du code, l'investissement est plus lourd — mais pas insurmontable. Le tuto 07 est conçu pour qu'un débutant complet puisse y arriver.

Test : *"Suis-je capable d'ouvrir un terminal et de taper `python3 --version` sans paniquer ?"*. Si oui, signal coché.

### Signal 7 — Ton brief est stable depuis au moins 2 semaines

Le pire serait de coder un agent et de devoir refactorer ton code à chaque fois que tu modifies une règle. Avant de passer à l'API, ton brief doit être **stable**. Pas figé pour l'éternité — mais pas en train de changer toutes les 48h non plus.

Test : *"Sur les 2 dernières semaines, combien de fois ai-je modifié mon brief de façon substantielle ?"*. Si la réponse est **0 ou 1**, signal coché. Si c'est **3+**, ton brief n'est pas prêt.

---

## Le score

- **5 à 7 signaux cochés** → passe à l'API. Tuto 07 maintenant.
- **3 à 4 signaux cochés** → cas limite. Si tu as du temps et que tu es à l'aise techniquement, vas-y. Sinon, reste en chat encore un peu.
- **0 à 2 signaux cochés** → reste en chat. Renforce ton brief, élargis tes cas couverts, mesure ce qui marche. Reviens à ce tuto dans 2-3 semaines.

---

## Ce que tu gagnes en passant à l'API

### Autonomie temporelle
L'agent tourne pendant que tu dors. Il traite ce qui arrive. Tu te réveilles avec le travail fait.

### Intégration
L'agent envoie directement les résultats où tu veux : ta base de données, ton CRM, ton bot Telegram/WhatsApp, ton dashboard.

### Précision des coûts
Chaque appel API est tracé : modèle, tokens entrée, tokens sortie, coût exact en dollars. Tu peux optimiser ton budget API.

### Versioning et reproductibilité
Ton code et tes briefs vivent dans un repo Git. Tu peux revenir en arrière, comparer, partager.

### Composition
Tu peux faire **plusieurs agents qui collaborent**. Le premier classifie un document, le deuxième l'extrait, le troisième stocke en base, le quatrième notifie le client. C'est le sujet des Parties 3 et 4 du repo.

### Tests automatiques
Tu peux écrire des tests qui passent toute ta journée à vérifier que tes agents répondent correctement sur des cas connus. Si une mise à jour du modèle change un comportement, tu le sais tout de suite.

---

## Ce que tu perds (et qu'il faut savoir)

### La beauté de l'interface chat
Claude.ai a une interface très bien faite. L'historique, la mise en forme, les artefacts, la recherche dans tes conversations. L'API te donne du brut. Si tu veux une belle UI, tu dois la construire toi-même (ou utiliser des outils tiers).

### La gratuité du forfait
Claude.ai Pro à 20 €/mois, c'est une utilisation pratiquement illimitée pour la plupart des gens. L'API est facturée à l'usage. Pour un petit volume, tu paieras moins. Pour un gros volume, tu paieras potentiellement plus, mais avec un coût mesurable et optimisable.

### La simplicité du démarrage
En chat, tu copies-colles et c'est parti. En code, tu installes Python, tu obtiens une clé API, tu écris ton premier `requirements.txt`, tu déboguent ton premier `import`. **C'est une marche réelle** — mais une seule, après laquelle tout devient plus fluide.

### La main mise sur l'évaluation
En chat, tu vois immédiatement si la réponse est bonne ou mauvaise. Tu peux dire *"refais en plus court"* et ajuster. En code, tu dois te construire des outils pour évaluer la qualité de tes sorties (logs, métriques, exemples de référence). C'est un travail réel mais nécessaire — et c'est exactement le sujet du pilier "Observabilité" du tuto 08.

---

## Les conditions préalables pour le tuto 07

Si tu décides de passer à l'API, vérifie que tu as :

### Côté logiciel
- **Python 3.10 ou plus récent** installé sur ta machine (`python3 --version` doit afficher 3.10+)
- **pip** installé (vient avec Python normalement)
- **Un éditeur de texte** correct : VS Code, Sublime, ou même un simple éditeur — pas Word

### Côté compte
- **Un compte Anthropic** sur [console.anthropic.com](https://console.anthropic.com) (gratuit)
- **Une clé API** créée depuis ce compte (5 crédits gratuits offerts pour démarrer, ensuite tu mets ta carte)
- **Quelques euros de crédit** pour pouvoir lancer tes premiers appels (5 € de crédit te donnent des milliers d'appels avec Haiku)

### Côté connaissance
- Tu as fait le tuto 05 et tu as un agent en chat qui marche
- Tu sais ouvrir un terminal (Mac : Terminal, Windows : PowerShell ou WSL, Linux : tu sais déjà)
- Tu sais ce qu'est un fichier `.py` et un fichier `.env`

Si une case te manque, prends 30 minutes pour la combler avant d'attaquer le tuto 07.

---

## Le mauvais raisonnement à éviter

> *"Je vais passer à l'API parce que c'est plus pro."*

Pas le bon critère. Tu vas y passer parce que **les sept signaux** te disent que c'est le bon moment. Pas parce que ça fait plus sérieux sur LinkedIn.

> *"Je vais passer à l'API parce qu'en chat je dois copier-coller."*

Si c'est ton seul critère, peut-être que tu peux automatiser **juste le copier-coller** avec un raccourci clavier ou un script simple, et continuer à utiliser Claude.ai. L'API est une décision plus lourde que de réduire un copier-coller.

> *"Je vais passer à l'API parce que tout le monde le fait."*

L'autre piège. Personne ne sait combien de gens utilisent Claude **uniquement** en chat et en sont très contents. Tu ne dois rien à la mode.

---

## Le bon raisonnement

Ton agent en chat te fait gagner du temps. Tu as quantifié combien. Tu sens qu'il y a un palier supplémentaire que tu pourrais franchir **pour un investissement raisonnable**. Tu en as l'envie. Tu en as les pré-requis.

**Alors tu y vas.**

C'est ce qu'on fait au tuto suivant.

---

## Récap mémorisable

> Sept signaux : **tâche quotidienne**, **événements pendant ton absence**, **intégration avec d'autres outils**, **traçage des coûts**, **versioning de la méthode**, **à l'aise avec du code**, **brief stable depuis 2 semaines**. 5 cochés ou plus → tuto 07. 2 ou moins → reste en chat et reviens dans 3 semaines.

---

## Pour aller plus loin

- **Tuto 07 — Premier appel API Anthropic** : ton premier script Python qui fait le même travail que ton agent en chat.
- **Tuto 08 — Les 4 piliers d'un agent solide** : à lire en parallèle de tes premiers développements. C'est le manifeste qui distingue un agent jetable d'un agent qui tient en prod.

---

[← Retour au sommaire](../README.md)
