# Agents en Pratique

> Apprendre à construire des agents IA avec Claude — de zéro à la production, en français.

**Auteur** : Driss Amiroune — médecin urologue à Fès, architecte logiciel auto-formé.

---

## Pourquoi ce repo

Il y a quelques mois, je ne savais pas ce qu'était une API. Aujourd'hui j'ai quatre systèmes qui tournent en production grâce à Claude — un pour gérer mon cabinet médical, un pour analyser la Bourse, un pour mes finances perso, et un pour ma veille IA personnalisée.

Ce repo, c'est ce que j'aurais voulu trouver au début. Pas un cours abstrait, pas une doc officielle aride, pas un tuto YouTube de 2h qui survole. Juste des **petits projets concrets** qui marchent, expliqués pas à pas, en français, pour les professionnels qui découvrent les agents IA sans avoir fait d'études d'informatique.

Chaque dossier est autonome : tu peux le lire en 5 minutes, le faire tourner en 15.

---

## ⚡ Démo méta : ce repo est géré par mon IA

Petite note avant d'aller plus loin.

Ce repo n'a pas été créé "à la main". À aucun moment je n'ai ouvert github.com pour cliquer sur *"New repository"*, ni tapé `git commit` dans un terminal. Sa création, le profil, les commits, le push — tout a été fait **en live depuis une conversation chat avec Claude**.

**Mon rôle** : lui dire ce que je veux, en français.
**Son rôle** : tout le reste.

C'est rendu possible par les serveurs MCP que j'ai construits sur mon serveur, qui exposent à Claude exactement les outils dont il a besoin pour piloter mon environnement.

---

## Ce que je fais déjà (et qui n'est pas open source)

Pour situer où ce repo va dans le temps, voici ce qui tourne actuellement sur mon serveur :

- **~104 000 lignes de Python** en production, ajoutées en quelques mois
- **4 systèmes métier** orchestrés par Claude, sur **un seul serveur à moins de 5 €/mois**
- **4 serveurs MCP** en parallèle (cabinet médical, valuation boursière, finances, R&D)
- **Defense-in-depth** : 4 rôles Claude séparés avec garde-fous pour empêcher l'agent de toucher à la prod par accident
- **Charte méthodologique versionnée** sur 228 itérations, séparée du code, dont les règles sont enforced par `AssertionError` citant les sections de la charte (§3.4ter, §4.4.4...)
- **Pipeline médical** PEC assurance avec OCR, extraction patient, assemblage PDF, notifications WhatsApp
- **Plateforme de valuation fondamentale** boursière : 7 archétypes × 68 paramètres, 319 tests pytest verts
- **30 crons orchestrés**, supervision automatique, audit log médico-légal par domaine métier
- **claude-agent-sdk** avec `@tool` + `can_use_tool` callback pour validation humaine en boucle

Aucun de ces systèmes n'est public — ils contiennent des données sensibles (patients, comptes). Mais **les patterns que j'ai construits en chemin finiront ici, en tutoriels**, au fur et à mesure qu'ils deviennent assez stables pour être pédagogiquement clairs.

---

## À qui ça s'adresse

- Aux médecins, juristes, profs, comptables, indépendants qui voient passer "agent IA" partout sans savoir ce que c'est concrètement
- Aux développeurs juniors qui veulent comprendre Claude au-delà du chat
- Aux gens qui ont essayé `n8n` ou `Make` et qui veulent passer à du code Python
- Aux curieux qui n'ont pas peur de copier-coller 30 lignes de Python
- Aux devs expérimentés qui veulent une référence FR concise à partager à des collègues débutants

## À qui ça ne s'adresse PAS

- Aux experts en LLM qui cherchent des techniques avancées (retrieval-augmented generation, fine-tuning, etc.)
- Aux gens qui veulent une solution clé-en-main sans rien comprendre
- Aux purs débutants Python qui ne savent pas installer Python — commence par [le tuto officiel Python](https://docs.python.org/fr/3/tutorial/index.html) d'abord

## Sommaire

| # | Tuto | Difficulté | Durée |
|---|---|---|---|
| 01 ✅ | Ton premier appel API Anthropic en Python | 🟢 Débutant | 15 min |
| 02 ✅ | Ton premier MCP server (4 outils utiles) | 🟢 Débutant | 30 min |
| 03 | Faire tourner ton agent 24/7 avec systemd | 🟡 Intermédiaire | 30 min |
| 04 | Faire parler ton agent avec Telegram | 🟡 Intermédiaire | 45 min |
| 05 | Tracer le coût de chaque appel API | 🟢 Débutant | 20 min |
| 06 | Fix "database is locked" en SQLite | 🟡 Intermédiaire | 20 min |
| 07 | Versionner /etc/nginx avec Git | 🟢 Débutant | 15 min |
| 08 | Screenshot d'une URL depuis ton agent | 🟢 Débutant | 25 min |
| 09 | Recherche web gratuite depuis ton agent | 🟡 Intermédiaire | 30 min |
| 10 | Digest hebdo de vidéos YouTube | 🟠 Avancé | 60 min |

Les tutos publiés ont leur statut ✅ dans le tableau. Les autres sont en cours de rédaction.

## Pré-requis communs

- **Python 3.10+** installé
- Un compte **Anthropic** avec une clé API ([créer une clé](https://console.anthropic.com/))
- Un terminal (macOS, Linux, ou WSL sur Windows)
- **Aucune connaissance préalable** des agents IA, MCP, ou async Python — chaque concept est expliqué quand on en a besoin

## Comment utiliser ce repo

Trois façons :

1. **Lecture seule** : tu lis les README dans l'ordre, tu apprends. Pas besoin de coder.
2. **Suivre étape par étape** : tu clones le repo, tu fais tourner chaque exemple, tu modifies.
3. **Cherry-pick** : tu vois un tuto qui résout ton problème actuel, tu sautes directement dedans.

```bash
git clone https://github.com/Kryscekk/agents-en-pratique.git
cd agents-en-pratique/01-premier-appel-api
# lis le README, copie le code, fais tourner
```

## Langues

- 🇫🇷 **Français** — langue principale, version de référence
- 🇬🇧 English — traduction prévue à partir du mois 3 pour les tutos qui marchent
- 🇲🇦 العربية — traduction prévue à partir du mois 5 pour les tutos qui marchent

## Licence

MIT — fais ce que tu veux avec ce code, donne-moi du feedback si ça t'a servi.

## Contact

- GitHub : [@Kryscekk](https://github.com/Kryscekk)
- LinkedIn : à venir

---

*Tutos écrits sur mon temps libre entre deux consultations, à Fès, Maroc. Si tu trouves une erreur ou une amélioration, ouvre une issue — j'apprends aussi en écrivant.*
