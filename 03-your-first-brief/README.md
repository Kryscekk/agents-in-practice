# 03 — Construire ton premier brief

**Difficulté** : 🟢 Débutant  |  **Durée** : 30 min de lecture, 1h de pratique

> Avant le code, avant l'API, avant les outils : **le brief**. Un fichier markdown qui définit comment Claude doit penser pour une tâche précise. C'est l'invention la plus puissante et la plus oubliée de ma méthode.

---

## Pourquoi ce tuto existe

Si tu utilises Claude depuis quelque temps, tu as probablement déjà eu cette frustration : tu lui demandes deux fois la même chose à un mois d'intervalle, et tu obtiens deux réponses **complètement différentes**. Pas parce que Claude est inconstant — parce que **toi**, tu lui as posé la question avec un contexte différent à chaque fois.

J'ai eu cette frustration tellement de fois sur mon analyse boursière que j'ai fini par écrire un fichier. Un fichier markdown qui dit à Claude *"voilà comment tu dois penser, voilà tes règles, voilà ce que tu dois produire en sortie"*. Je l'ai appelé un **brief**.

Quand je commence une session de travail, je colle ce brief en premier message. Claude prend son rôle. Tous mes briefs suivent la même structure, et c'est devenu mon meilleur outil — bien avant le code, bien avant l'API.

Aujourd'hui j'ai 7 briefs en prod sur un de mes projets (un par "agent" : extracteur, classifieur, valorisateur, validateur, etc.), et plusieurs dizaines de briefs ponctuels que j'utilise quand j'en ai besoin.

---

## Qu'est-ce qu'un brief ?

Un brief, c'est **un document qui définit un rôle pour Claude**. Avec :

- **un rôle clair** (qu'est-ce que tu dois faire ?)
- **un principe fondamental** (la règle d'or absolue)
- **des règles** (ce qu'on fait, ce qu'on ne fait pas)
- **un processus** (les étapes à suivre, dans l'ordre)
- **un format de sortie** (à quoi ressemble une bonne réponse)

C'est la même logique qu'un brief client en agence ou qu'une fiche de poste : tu cadres ce que tu attends pour ne pas tomber sur du flou.

**Ce que le brief n'est pas** :
- Un long mode d'emploi de l'API
- Un prompt magique de 5 mots
- Une description de Claude lui-même

C'est un **rôle métier** que Claude va endosser.

---

## La structure type d'un brief

Voilà la structure que j'utilise dans tous mes briefs, sans exception :

```markdown
# Brief — Agent X

> Rôle : (UNE phrase qui dit ce que tu dois faire)
> Fichier : (optionnel — quel fichier de code implémente ça si applicable)

## Principe fondamental

(La règle d'or absolue. Une à trois phrases. C'est l'idée qui prime sur tout.)

## Règles

1. (Première règle non négociable)
2. (Deuxième règle)
3. (...)

## Processus

### 1. (Première étape)
Description de ce que tu fais à cette étape.

### 2. (Deuxième étape)
...

## Format de sortie

(Description précise de ce que tu dois produire. Si possible avec un exemple.)
```

Cinq sections, toujours dans cet ordre. C'est court (souvent 50-150 lignes) et lisible d'un seul coup.

---

## Pourquoi cette structure marche

### "Rôle" — l'identité
Une phrase. *"Tu es l'agent qui extrait les données financières des PDFs."* C'est ce qui permet à Claude de se positionner. Pas trois paragraphes — une phrase.

### "Principe fondamental" — la règle qui dépasse les autres
C'est la phrase que Claude doit garder en tête s'il oublie tout le reste. Exemple tiré de mon vrai brief d'extraction :

> *"Le PDF est une source primaire officielle — même fiabilité qu'une donnée en base. Si le PDF donne directement un chiffre, l'utiliser tel quel. Ne pas le recalculer."*

C'est une phrase, mais elle évite 80% des erreurs que je voyais avant. Le principe fondamental, c'est ta **clé de voûte**.

### "Règles" — les non-négociables
Liste numérotée, phrases courtes, formulations à l'impératif ou en interdictions. Exemple :

```markdown
1. Toujours lire le fichier entier AVANT de répondre.
2. Si un chiffre est ambigu, NE PAS deviner — demander confirmation.
3. JAMAIS inventer une donnée absente.
4. Une seule source de vérité par section, citée explicitement.
```

Les majuscules sur **JAMAIS** et **AVANT** ne sont pas des cris : ce sont des marqueurs visuels qui aident Claude (et toi en relecture) à voir ce qui ne se discute pas.

### "Processus" — les étapes ordonnées
Pas une liste plate, une **séquence**. *"D'abord 1, ensuite 2, puis 3."* Si tu peux numéroter, numérote.

```markdown
### 1. Identifier la période du document

Repère dans le PDF : annuel, S1, T1/T2/T3/T4. Critère :
- "Rapport annuel" → annuel
- "Communiqué résultats S1" → S1
- "Communiqué T1" → T1

### 2. Lire les données structurées

Privilégier les états de synthèse (compte de résultat) aux communiqués
de presse. En cas de divergence, l'audité prime.

### 3. Calculer ce qui manque

Si BPA non affiché : BPA = RNPG × 1000 / NbAct.

### 4. Enregistrer dans la base
...
```

Claude exécute mieux quand il sait *où il en est* dans la séquence.

### "Format de sortie" — l'exemple concret
La section la plus oubliée par les débutants. Tu dois montrer à Claude **à quoi ressemble une bonne réponse**.

Mauvais format de sortie : *"Rends-moi un résumé structuré."*

Bon format de sortie :

```markdown
## Format de sortie

```
Ticker : ATW
Période : annuel 2025
Source : atw_rapport_annuel_2025.pdf

BPA      : 49.48 DH/action
DPA      : 22.00 DH/action
RNPG     : 10 643 MDH
NbAct    : 215 140 K actions

Notes : (texte libre, max 3 lignes)
```
```

Claude voit le gabarit exact, il s'y conforme. Pas besoin de répéter en chat *"donne-moi un résumé avec ces champs"*, c'est dans le brief.

---

## Un exemple complet, anonymisé

Voilà un brief que j'utilise pour un assistant qui m'aide à préparer mes rapports de consultation médicale. **Anonymisé et simplifié** pour ce tuto :

```markdown
# Brief — Assistant CR (compte-rendu de consultation)

> Rôle : Rédiger un CR de consultation à partir de mes notes brutes.

## Principe fondamental

Le CR doit **refléter exactement** ce que j'ai écrit, sans rien ajouter, sans rien inventer, sans extrapoler une pathologie absente de mes notes. Si une info est manquante, le CR dit "non précisé" — il ne devine pas.

## Règles

1. JAMAIS inventer un diagnostic, un médicament, un examen complémentaire.
2. JAMAIS supposer un antécédent ou une comorbidité absente des notes.
3. Si une abréviation est ambiguë, demander avant de la traduire.
4. Toujours conserver la chronologie : motif → examen → diag → CAT.
5. La langue est le français médical neutre. Pas de jargon spécialiste si le destinataire est généraliste.

## Processus

### 1. Lire mes notes en entier

Avant d'écrire la première ligne, lire TOUTES les notes que je t'ai données. Repère les éléments principaux : motif de consultation, examen clinique, conclusion, conduite à tenir.

### 2. Identifier les éléments manquants

Si une section type d'un CR n'apparaît pas dans mes notes (ex : pas d'examen biologique mentionné), tu marques "non précisé" — tu n'inventes pas.

### 3. Structurer dans l'ordre standard

1. Identité (à partir de l'en-tête que je te donne)
2. Motif de consultation (une phrase)
3. Antécédents (uniquement ceux mentionnés)
4. Examen clinique
5. Examens complémentaires (résultats si présents)
6. Conclusion / Diagnostic
7. Conduite à tenir
8. Prochain rendez-vous

### 4. Rédiger en respectant le ton

Phrases courtes, voix active, vocabulaire médical mais pas spécialiste, pas d'opinion personnelle.

## Format de sortie

```
COMPTE-RENDU DE CONSULTATION

Patient : [Nom Prénom]
Date    : [JJ/MM/AAAA]

Motif :
[une phrase]

Antécédents :
- [liste à puces, "néant" si rien]

Examen clinique :
[paragraphe]

Examens complémentaires :
[paragraphe ou "non précisé"]

Conclusion :
[1-2 phrases]

Conduite à tenir :
1. [...]
2. [...]

Prochain RDV :
[date ou "à programmer"]
```

Pas de signature, pas de cachet — je m'en charge moi-même à l'impression.
```

Ce brief fait **~60 lignes**. Je le colle au début de chaque session, je lui donne mes notes, j'obtiens un CR cohérent à chaque fois.

**Compare ça à** : *"Claude, fais-moi un compte-rendu à partir de ces notes."* Tu vois la différence ?

---

## Comment construire **ton premier brief**

Choisis une tâche que tu fais souvent avec Claude où tu n'es pas satisfait du résultat actuel. Exemples possibles selon ton métier :

| Métier | Tâche type |
|---|---|
| Avocat | Résumer une décision de jurisprudence dans un format précis |
| Comptable | Catégoriser des opérations bancaires selon ton plan comptable |
| Prof | Préparer une fiche de cours à partir d'un programme officiel |
| Marketeur | Rédiger un post LinkedIn dans le ton de ton entreprise |
| Dev | Reviewer un PR selon des règles précises (sécurité, perf, conventions) |
| Médecin | Préparer une lettre de référence vers un confrère |

Maintenant, suis ces 5 étapes (≈30 minutes au total) :

### Étape 1 — Note ta frustration actuelle (5 min)

Réponds par écrit à : *"Qu'est-ce qui ne va pas dans les réponses actuelles de Claude sur cette tâche ?"*

Sois concret. Pas *"c'est pas bon"*. Plutôt *"il oublie de mentionner la date de la décision"* ou *"il met trop de jargon pour mes clients"*.

### Étape 2 — Écris le principe fondamental (5 min)

Une à trois phrases. **Le principe qui doit dépasser toutes les règles.**

Exemples :
- *"Le résumé doit faire au max 200 mots et inclure la date, la juridiction, et la solution."*
- *"Ne JAMAIS catégoriser une opération sans certitude. Préférer 'à classer manuellement' à une erreur."*

### Étape 3 — Liste tes règles (10 min)

5 à 10 règles maximum, numérotées, à l'impératif ou en interdictions. **Ne dépasse pas 10.** Au-delà, Claude commence à oublier les premières.

### Étape 4 — Décris le processus (5 min)

3 à 6 étapes. *D'abord, ensuite, puis...*

### Étape 5 — Donne un exemple de sortie (5 min)

C'est l'étape la plus puissante. Mets dans le brief **un exemple précis** de ce que tu attends comme réponse. Pas une description abstraite — un vrai exemple, dans un bloc de code.

---

## Comment utiliser ton brief

Sauvegarde-le dans un fichier `brief_xxx.md` quelque part dans tes documents.

Au début d'une nouvelle conversation Claude, copie-colle le contenu en premier message, avec une phrase d'introduction :

> *"Voici le brief de l'agent X. Lis-le en entier, confirme que tu l'as compris, et attends mes instructions."*

Claude répond : *"Brief reçu, je suis prêt à...".* À partir de ce moment-là, ses réponses suivent les règles, le processus, et le format de sortie.

Si tu vois qu'une règle est mal formulée ou qu'il manque un cas — modifie le brief sur ton disque. Le brief est **vivant** : il évolue avec ta pratique.

---

## Les pièges classiques

### Piège 1 — Le brief de 5 lignes
*"Tu es un expert juridique. Réponds bien."* C'est un prompt, pas un brief. Si tu ne peux pas écrire 30 lignes, c'est que tu ne sais pas encore ce que tu veux exactement. Réfléchis avant.

### Piège 2 — Le brief encyclopédique
500 lignes. Claude va lire le début et la fin, oublier le milieu. **Reste sous 200 lignes.** Si tu as besoin de plus, c'est que tu as plusieurs rôles distincts — fais plusieurs briefs.

### Piège 3 — Les règles contradictoires
*"Sois concis"* + *"Détaille bien chaque point"*. Claude va trancher comme il peut, et tu seras frustré. Relis tes règles à voix haute et cherche les contradictions.

### Piège 4 — Pas de format de sortie
Sans gabarit explicite, Claude improvise. Toujours mettre un exemple concret de sortie attendue.

### Piège 5 — Le brief théorique
Tu décris des concepts au lieu d'instructions. Mauvais : *"La rigueur est importante."* Bon : *"Citer la source de chaque chiffre, format `[source : page X]`."*

---

## Pour aller plus loin

- **Tuto 04 — Un CLAUDE.md pour ton projet** : étend le brief au niveau d'un projet complet, pour que Claude connaisse ton contexte technique sans qu'on lui re-explique à chaque session.
- **Tuto 05 — Ton premier agent en chat (sans code)** : combine un brief + un CLAUDE.md pour faire un vrai agent utilisable au quotidien, sans une ligne de Python.

---

## Récap mémorisable

> Cinq sections, dans cet ordre : **Rôle** (1 phrase), **Principe fondamental** (1-3 phrases), **Règles** (5-10 numérotées), **Processus** (3-6 étapes), **Format de sortie** (avec exemple concret). Sous 200 lignes. Évolutif.

---

[← Retour au sommaire](../README.md)
