# 04 — Un CLAUDE.md pour ton projet

**Difficulté** : 🟢 Débutant  |  **Durée** : 30 min de lecture, 1h de pratique

> Si ton brief définit **un rôle**, ton `CLAUDE.md` définit **le contexte du projet entier**. C'est le document que Claude lit en premier au début de chaque session, pour comprendre où il est, ce qui existe déjà, et quelles sont les règles techniques de la maison.

---

## Pourquoi ce tuto existe

Au début, à chaque nouvelle session Claude, je passais 10 minutes à lui réexpliquer mon projet : *"j'ai un cabinet médical, le serveur est sur Hetzner, j'utilise SQLite, mes patients sont stockés dans la table X, attention il y a un piège sur la colonne Y..."*. Dix minutes. À chaque session. Pour qu'il oublie tout à la session suivante.

Puis j'ai écrit un fichier `CLAUDE.md` à la racine du projet. Sept sections, lisible en 2 minutes. Maintenant je commence chaque session en disant : *"Lis le CLAUDE.md à la racine, puis attends."* Et on démarre directement sur du concret.

Ce simple fichier a transformé ma productivité avec Claude. Et il a un autre avantage caché : **il m'oblige à formaliser mon propre projet.** Beaucoup de bugs ont été évités juste parce que j'ai dû *écrire noir sur blanc* les pièges de ma base de données.

---

## Brief vs CLAUDE.md — la différence

| | Brief | CLAUDE.md |
|---|---|---|
| **Portée** | Une tâche, un rôle | Un projet entier |
| **Quand utilisé** | Au début d'une session sur ce rôle | Au début de TOUTE session sur ce projet |
| **Contenu** | Règles, processus, format | Architecture, structure, pièges, règles techniques |
| **Localisation** | Quelque part dans tes notes | À la racine du repo (`./CLAUDE.md`) |
| **Évolution** | Stable, change rarement | Vivant, mis à jour à chaque session importante |

Le brief dit *"voici comment tu dois penser pour CE rôle"*. Le CLAUDE.md dit *"voici ce que tu dois savoir sur CE projet, quel que soit le rôle"*.

Tu peux avoir un brief sans CLAUDE.md (pour un truc one-shot). Tu peux aussi avoir un CLAUDE.md sans brief (pour un projet où tu n'as pas formalisé de rôles). Mais sur un vrai projet long-terme, tu auras les deux.

---

## La structure type d'un CLAUDE.md

Sept sections, dans l'ordre où Claude va les lire et en aura besoin :

```markdown
# [Nom du projet] — Contexte

## Architecture
(L'infra : serveur, OS, langages, services externes)

## Structure
(L'arbre des dossiers + ce que contient chaque dossier important)

## Services
(Ce qui tourne : crons, services systemd, bots, watchers)

## Base de données
(Tables, colonnes principales, pièges et gotchas)

## Pipeline métier
(Le flux principal : entrée → étapes → sortie)

## Règles de code
(Les conventions non négociables sur CE projet)

## Sécurité
(Réseau, secrets, accès)
```

C'est ma structure standard, héritée de l'expérience. Tu peux ajouter des sections au besoin, mais ne supprime pas une des sept — elles répondent toutes à une question que Claude se pose à un moment ou un autre.

---

## Pourquoi ces sept sections (et dans cet ordre)

### "Architecture" — *où on est*
Claude doit savoir s'il parle à du Python 3.10 sur Mac ou du Python 3.12 sur Ubuntu, si la DB est SQLite local ou PostgreSQL distant, s'il y a un reverse proxy. Sans ça, il propose des commandes qui ne marchent pas chez toi.

Exemple :
```markdown
## Architecture
- Serveur Linux Ubuntu 24.04, hostname `monserveur`
- Python 3.12, SQLite 3.45, nginx en reverse proxy port 443
- Anthropic API : Sonnet par défaut, Opus pour les analyses lourdes
- Telegram bots pour les notifications
```

### "Structure" — *où sont les choses*
Un arbre commenté. Claude n'a pas besoin de tout l'arbre — il a besoin des dossiers importants avec **ce qu'on y trouve**.

Exemple :
```markdown
## Structure
```
mon-projet/
├── agents/          # logique métier, un dossier par agent
│   ├── pec/         # gestion des dossiers d'assurance
│   ├── rdv/         # planification des rendez-vous
│   └── workflow/    # orchestration des agents
├── shared/          # code partagé (logger, db, notifier)
├── data/            # base SQLite
├── ui/              # dashboard Flask
└── cron/            # scripts à lancer en cron
```
```

Pas tout l'arbre — les dossiers qu'on va effectivement toucher.

### "Services" — *ce qui tourne déjà*
Quand Claude propose *"lance un cron à 20h"*, il faut qu'il sache si tu en as déjà un, et où il est. La section liste tes services systemd, tes crons existants, tes bots.

```markdown
## Services
- `mon-agent.service` — watcher principal, démarre au boot
- `mon-dashboard.service` — Flask port 5555
- Crons :
  - 20h : workflow principal (`scripts/workflow.sh`)
  - 8h L-S : rapport quotidien Telegram
  - 2h : backup DB
```

### "Base de données" — *où sont stockées tes vraies données*
**C'est la section la plus précieuse**, parce que c'est là que sont les **pièges**. Liste les tables principales, les colonnes utiles, et **surtout les gotchas**.

```markdown
## Base de données (data/mon-projet.db)

Tables principales :
- `patients` (id, nom, prenom, date_naissance, telephone)
- `consultations` (id, patient_id, date, motif, notes)
- `rdv` (id, patient_id, date_rdv, statut, source)

ATTENTION aux noms de colonnes (erreurs historiques) :
- `alertes_preop` (PAS "examens" — erreur classique)
- `medicaments_notes` (PAS "medicaments")
- `motiff` à double-f (typo héritée d'une vieille API externe, ne PAS corriger)
```

Ces 5 lignes valent des heures de débogage à Claude. À chaque fois que tu corriges Claude *"non, la colonne s'appelle X pas Y"*, ajoute-le ici.

### "Pipeline métier" — *le flux principal*
Tu dois pouvoir expliquer en 5-10 étapes ce qui se passe entre une entrée (un patient appelle, un fichier arrive, une heure sonne) et une sortie (une notification, un PDF, une donnée stockée).

```markdown
## Pipeline PEC (Prise En Charge assurance)

1. Le patient passe en consultation, je note un acte en attente d'accord assurance.
2. Le workflow 20h détecte les nouveaux actes (analyseur clinique).
3. Quand l'assistante scanne les pièces, le watcher OCRise et classifie.
4. Quand toutes les pièces obligatoires sont là, génération d'un PDF assemblé.
5. Notification WhatsApp + transition du patient vers "envoyé à l'assurance".
6. Validation manuelle de l'envoi par moi (le système ne décide jamais seul).
```

Ce paragraphe résume **des semaines de travail** en 6 lignes. C'est ce qui permet à Claude de comprendre le **pourquoi** d'une demande.

### "Règles de code" — *les conventions de la maison*
Court, percutant, à l'impératif.

```markdown
## Règles de code
- Toujours lire le fichier complet AVANT de le modifier
- Backup automatique avant écriture (via le helper `write_with_backup`)
- Ne JAMAIS modifier `.env`
- Tester après chaque modification : `python3 -m py_compile`
- Un chantier à la fois, consolidation avant expansion
- Pour les opérations métier, passer par les services `shared/services/`
- 159 pytests doivent passer avant tout commit majeur
```

7 règles, 7 lignes. C'est ce qui distingue ton code d'un code générique.

### "Sécurité" — *les contraintes externes*
```markdown
## Sécurité
- UFW actif, seuls 22, 80, 443 ouverts
- `.env` est chmod 600
- Pas d'API key dans le code, jamais
- Accès distant uniquement via WireGuard (10.0.0.x)
```

Pour que Claude ne te suggère pas *"ouvre le port 5432 pour PostgreSQL"* sur un serveur où c'est non négociable.

---

## Un exemple complet, anonymisé

```markdown
# Mon-Cabinet — Contexte projet

## Architecture
- Serveur Linux à 5€/mois, Ubuntu 24.04
- Python 3.12, SQLite 3.45, nginx 1.24
- Anthropic API : Sonnet par défaut, Haiku pour les bots Telegram
- 2 bots Telegram (assistant + scanner CIN)
- Calendrier Google synchronisé

## Structure
```
mon-cabinet/
├── agents/          # un dossier par agent
│   ├── assistant/   # bot Telegram principal
│   ├── pec/         # dossiers d'assurance
│   ├── rdv/         # rendez-vous
│   └── workflow/    # orchestrateur 20h
├── shared/          # logger, db, notifier, helpers API
├── data/            # base SQLite
├── ui/              # dashboard Flask port 5555
└── cron/            # scripts à lancer en cron
```

## Services
- `cabinet.service` — bots + watchers
- `cabinet-dashboard.service` — Flask port 5555
- Crons :
  - 20h : workflow principal
  - 8h L-S : alerte matin Telegram
  - 2h : backup DB

## Base de données (data/cabinet.db)

Tables : `patients`, `consultations`, `rdv`, `dossier_pec`, `documents_pec`,
`patients_groupes`, `chirurgies`, `historique`.

ATTENTION aux noms de colonnes :
- `alertes_preop` (PAS "examens")
- `medicaments_notes` (PAS "medicaments")
- Une consultation référence `patient_id`, jamais `id_patient`

Groupes parcours patient :
`indications_chir`, `attente_admin`, `pec_envoyee`, `a_rappeler`,
`programmes`, `attente_bloc`

## Pipeline PEC (Prise En Charge assurance)

1. Patient en consultation → acte noté (à valider par l'assurance)
2. Workflow 20h : détecte les nouveaux actes, les classe
3. Scan des pièces : OCR + classification + identification patient
4. Quand toutes les pièces obligatoires sont là : génération PDF assemblé
5. Notification + transition du patient vers `pec_envoyee`
6. Validation manuelle de l'envoi par moi (jamais auto)

## Règles de code
- Toujours lire le fichier complet AVANT de le modifier
- Backup automatique avant écriture (via `write_with_backup`)
- Ne JAMAIS modifier `.env`
- Test post-modif : `python3 -m py_compile`
- Un chantier à la fois, consolidation avant expansion
- Opérations métier : passer par `shared/services/*_service.py`

## Sécurité
- UFW actif, seuls 22, 80, 443 ouverts
- `.env` chmod 600, jamais en clair
- Accès distant via VPN uniquement
```

**Total : ~70 lignes.** Lisible par Claude en 30 secondes au début d'une session, ça remplace 10 minutes d'explications.

---

## Construire ton premier CLAUDE.md

Suis ces 5 étapes (≈45 minutes au total) :

### Étape 1 — Architecture (5 min)
Liste : OS, langage(s), base de données, services externes utilisés (API, bots), reverse proxy s'il y en a.

### Étape 2 — Structure (10 min)
Va à la racine de ton projet. `tree -L 2 -d` (ou regarde dans ton explorateur). Garde **uniquement les dossiers qu'on va toucher**. Pour chaque dossier important, une phrase qui dit ce qu'il contient.

### Étape 3 — Services (5 min)
Liste tes crons (`crontab -l`), tes services systemd (`systemctl list-units | grep <ton-projet>`). Si tu n'en as pas, écris *"Aucun service permanent — exécution manuelle uniquement."*

### Étape 4 — Base de données (15 min)
**La section la plus importante**. Liste tes tables principales, les colonnes utiles, et surtout **les pièges**. Si tu n'as pas de pièges encore, écris la liste vide — tu remplis au fur et à mesure que tu en rencontres.

### Étape 5 — Pipeline + Règles + Sécurité (10 min)
- Pipeline : 5-10 lignes qui résument le flux principal.
- Règles : 5-10 lignes courtes à l'impératif.
- Sécurité : 3-5 lignes (ports, secrets, accès).

---

## Comment l'utiliser

Sauvegarde-le à la racine de ton projet :
```
mon-projet/
├── CLAUDE.md      ← ici
├── README.md
└── ...
```

Au début de chaque session :
> *"Avant de répondre, lis le `CLAUDE.md` à la racine du projet, puis dis-moi que tu l'as compris."*

Claude répond, et à partir de ce moment-là, ses propositions de code respectent **TES** conventions sans que tu aies à les répéter.

Si tu utilises Claude Code, place-le à la racine du repo : il est lu automatiquement à chaque démarrage de session.

---

## Le CLAUDE.md est **vivant**

À chaque session où Claude fait une erreur que tu corriges (*"non, la colonne s'appelle X"*, *"non, il y a déjà un service qui fait ça"*), **ajoute ça au CLAUDE.md**. Au bout de quelques semaines, le fichier devient ta mémoire institutionnelle.

Mon `CLAUDE.md` de cabinet médical fait aujourd'hui ~400 lignes. Il accumule 6 semaines de leçons concrètes. Quand un nouveau Claude démarre, il bénéficie immédiatement de ces 6 semaines de savoir.

---

## Les pièges classiques

### Piège 1 — Trop verbeux
Au-delà de 300 lignes, Claude commence à oublier le milieu. **Quand tu dépasses 300 lignes, factorise** : déplace les détails dans des fichiers annexes (`docs/db_schema.md`, `docs/api_externe.md`) et garde le CLAUDE.md en synthèse.

### Piège 2 — Trop générique
*"On utilise Python."* Pas suffisant. Quelle version, quelles libs principales, quel framework si applicable.

### Piège 3 — Trop technique
N'oublie pas le **pourquoi**. La section "Pipeline métier" donne le sens. Sans elle, Claude code mais ne comprend pas l'usage.

### Piège 4 — Pas de gotchas DB
La section qui te fera gagner le plus de temps. Si tu n'as rien à y mettre, c'est que tu n'as pas encore travaillé assez avec ta DB pour connaître ses pièges. Reviens y dans 2 semaines.

### Piège 5 — Tu oublies de demander à Claude de le lire
Le CLAUDE.md ne s'auto-charge pas (sauf dans Claude Code). Si tu utilises Claude.ai en web, tu dois lui demander explicitement de le lire en début de session.

---

## Pour aller plus loin

- **Tuto 05 — Premier agent en chat (sans code)** : combine ton brief (tuto 03) et ton CLAUDE.md pour créer un agent réutilisable, sans une ligne de Python.
- **Tuto 07 — Premier appel API** : quand le contexte est fixé par le CLAUDE.md, passer à du code Python est facile.

---

## Récap mémorisable

> Sept sections : **Architecture**, **Structure**, **Services**, **Base de données** (avec pièges !), **Pipeline métier**, **Règles de code**, **Sécurité**. À la racine du projet. **Vivant** : tu l'enrichis à chaque leçon. Sous 300 lignes.

---

[← Retour au sommaire](../README.md)
