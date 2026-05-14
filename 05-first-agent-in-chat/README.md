> 🇬🇧 **English version**: [README.en.md](README.en.md)

# 05 — Ton premier agent en chat (sans code)

**Difficulté** : 🟢 Débutant  |  **Durée** : 30 min de lecture, 1h-2h de pratique

> Tu vas construire ton premier vrai agent — un Claude qui joue un rôle précis, suit des règles strictes, produit un format constant. Sans une ligne de Python. Juste un brief, un CLAUDE.md léger, et la discipline de toujours démarrer ta conversation de la même façon.

---

## Pourquoi ce tuto existe

Quand on parle d'"agent IA", les gens imaginent immédiatement du code complexe, des APIs, des serveurs. Cette représentation décourage ceux qui n'ont pas fait d'informatique. Pourtant, **80 % de la valeur d'un agent vient de la méthode, pas du code**.

Avant d'écrire ma première ligne de Python, j'ai passé plusieurs semaines à construire des agents en chat seul. Je leur donnais un brief, un contexte, et je travaillais avec eux. Ça suffit pour énormément de cas réels — et ça t'apprend ce qui compte avant que tu attaques du code que tu ne saurais pas déboguer.

Ce tuto t'emmène jusqu'au bout : un agent que tu vas utiliser **vraiment**, pas un exercice théorique.

---

## Ce qu'on construit

Un agent en chat qui :
- A un **rôle clair** (défini par ton brief)
- Connaît ton **contexte projet** (défini par ton CLAUDE.md léger)
- Produit des résultats **constants** à chaque utilisation
- Que tu peux convoquer en 30 secondes pour faire son travail

On va prendre un exemple concret de bout en bout : **un agent "trieur de mails clients"**. Tu pourras adapter à ton métier après.

---

## Pré-requis

- Avoir lu et fait le tuto **03 — Construire ton premier brief**
- Avoir lu et fait le tuto **04 — Un CLAUDE.md pour ton projet**
- Un compte Claude (gratuit suffit pour démarrer, mais Pro/Max est largement plus confortable pour les longues sessions)
- 30 minutes au calme

---

## Étape 1 — Choisir une vraie tâche que tu vas vraiment utiliser

C'est la marche la plus importante, et celle qu'on saute le plus souvent. Si tu choisis une tâche bidon pour t'entraîner, tu n'utiliseras jamais l'agent et tu n'apprendras rien.

**Critères d'une bonne première tâche pour un agent en chat** :

1. Tu la fais **au moins une fois par semaine**
2. Elle prend **entre 10 et 60 minutes** à chaque fois
3. Le résultat suit toujours **plus ou moins le même format**
4. Tu peux la décrire en **5 à 10 phrases**
5. **Aucune décision irréversible** (l'agent peut se tromper sans casser ta vie)

Exemples par métier :

| Métier | Bonne première tâche |
|---|---|
| Médecin | Préparer un compte-rendu de consultation à partir de notes brutes |
| Avocat | Résumer une décision de justice dans un format précis |
| Comptable | Catégoriser un relevé bancaire selon ton plan comptable |
| Prof | Rédiger une fiche d'évaluation d'élève à partir de notes |
| Marketeur | Transformer un article long en post LinkedIn |
| Indépendant | Préparer un devis à partir d'un brief client |
| Manager | Synthétiser les comptes-rendus de tes 1:1 hebdo |

Pour le reste de ce tuto, on prend l'exemple **"trier mes mails clients"**. Concret, fréquent, format constant. À adapter à ta propre tâche.

---

## Étape 2 — Écrire le brief

Tu connais déjà le pattern (tuto 03) : Rôle / Principe fondamental / Règles / Processus / Format de sortie.

Voilà le brief pour notre exemple :

```markdown
# Brief — Agent Tri-Mails-Clients

> Rôle : Lire un mail reçu d'un client et le catégoriser selon mes règles
> pour que je traite chaque type efficacement.

## Principe fondamental

Un mail mal catégorisé est pire qu'un mail non catégorisé. **Si tu hésites
entre deux catégories, mets "À VOIR" et explique ton hésitation en deux
lignes — je tranche.** Ne JAMAIS deviner.

## Règles

1. JAMAIS inventer un contenu absent du mail.
2. Si le mail contient plusieurs sujets distincts, le catégoriser dans la
   catégorie principale, mais signaler les autres dans les notes.
3. La priorité est mesurée par mon impact business, pas par le ton du
   client.
4. Une catégorie "spam" existe et est gérée différemment (action = supprimer).
5. Si le client demande explicitement à parler à moi par téléphone, la
   priorité monte automatiquement à HAUTE.

## Processus

### 1. Lecture du mail entier
Ne jamais répondre sur la base du sujet seul. Lire tout, y compris la
signature et les pièces jointes mentionnées.

### 2. Identifier la catégorie principale
- `DEVIS` — demande de chiffrage / proposition commerciale
- `SUIVI_COMMANDE` — question sur une commande en cours
- `RECLAMATION` — problème avec un produit ou service livré
- `INFO_GENERALE` — question informative sans demande d'action
- `RDV` — demande de rendez-vous
- `SPAM` — promotionnel, automatique, non sollicité
- `A_VOIR` — tu ne peux pas trancher, explique en deux lignes

### 3. Évaluer la priorité
- `HAUTE` : client demande un délai court (<48h), réclamation grave,
  client signale qu'il est mécontent, mention de la concurrence,
  demande explicite d'appel
- `MOYENNE` : demande de devis ou de RDV sans urgence affichée
- `BASSE` : question informative, suivi de routine

### 4. Extraire les éléments-clés
Date demandée si applicable, montant si applicable, référence commande,
nom du contact, sentiment du client (positif/neutre/négatif).

### 5. Suggérer une action
Une action concrète que je peux exécuter en 5 minutes.

## Format de sortie

```
SUJET : [reprise exacte du sujet du mail]
DE    : [nom + email]

CATÉGORIE : [DEVIS | SUIVI_COMMANDE | RECLAMATION | INFO_GENERALE | RDV | SPAM | A_VOIR]
PRIORITÉ  : [HAUTE | MOYENNE | BASSE]

CLIENT      : [nom, société si applicable]
RÉFÉRENCE   : [numéro de commande, devis, etc. — ou "aucune"]
SENTIMENT   : [positif | neutre | négatif]

RÉSUMÉ (2 lignes) :
[résumé factuel de la demande]

ACTION SUGGÉRÉE :
[une phrase, action concrète exécutable en <5 min]

NOTES (si applicable) :
[autres sujets mentionnés, points d'attention, hésitations]
```
```

Ce brief fait ~70 lignes. Tu peux l'écrire dans 30 minutes en t'inspirant de cette structure.

---

## Étape 3 — Écrire un CLAUDE.md léger

Pour un agent en chat, tu n'as pas besoin du `CLAUDE.md` complet du tuto 04 (qui sert pour des projets de code). Tu as besoin de **2-3 sections seulement** :

```markdown
# Cabinet Dr Amiroune — Contexte mail

## Activité
Cabinet médical d'urologie à Fès. Je reçois des mails de patients, de
collègues médecins, de fournisseurs (matériel médical, assurance,
laboratoires), et beaucoup de spam.

## Clients/Contacts récurrents
- Cabinet Akdital (clinique partenaire) — souvent des PEC à valider
- Laboratoires Echo-Plus (matériel d'échographie)
- Cabinet d'un confrère le Dr X — partage de patients
- Mutuelle FAR — gestion des dossiers militaires

## Mes priorités business
- Les PEC d'assurance sont prioritaires : tout retard impacte le patient.
- Les RDV nouveaux patients sont prioritaires : ne pas les rater.
- Les mails de matériel médical peuvent attendre 48-72h.
- Spam : direct poubelle.

## Sentiments à surveiller particulièrement
Si un patient ou un assureur exprime une frustration sur un délai de
prise en charge, c'est immédiatement HAUTE.
```

Ce mini-contexte fait ~25 lignes. Il complète ton brief en donnant à Claude **les noms, les contacts, les priorités** spécifiques à ton monde.

---

## Étape 4 — Construire ta routine d'utilisation

C'est ici que beaucoup de débutants se trompent. **Un agent qui marche, c'est un agent que tu utilises de la même façon à chaque fois.** Tu dois te construire un rituel.

Voilà le rituel que je te recommande :

### a) Ouvre une nouvelle conversation Claude

Sur claude.ai, clique sur *"New chat"*. Tu repars d'une feuille blanche pour cette tâche.

### b) Premier message : colle le brief + le CLAUDE.md

Dans ce premier message, colle :

```
Voici mon brief pour l'agent Tri-Mails-Clients, ainsi que mon contexte projet.
Lis tout en entier, confirme que tu l'as compris, et attends mes mails à trier.

================================================================
BRIEF
================================================================
[le contenu de ton brief]

================================================================
CONTEXTE PROJET
================================================================
[le contenu de ton CLAUDE.md léger]
```

Claude répond : *"Brief reçu, je suis prêt. Envoie-moi le premier mail."*

### c) Tu envoies tes mails un par un

Copie le mail (sujet + corps + signature) et colle dans le chat. Claude répond dans le format prévu. Tu lis, tu valides, ou tu corriges.

### d) Quand Claude se trompe, tu améliores le brief

Si Claude classe un mail en `INFO_GENERALE` alors que c'était un `DEVIS` selon toi, **deux options** :

1. **Une fois** : tu corriges Claude dans la conversation (*"non, c'est un DEVIS parce que..."*). Claude apprend pour le reste de la conversation.
2. **Récurrent** : tu **modifies le brief** sur ton disque. Tu ajoutes une règle ou tu précises la définition de la catégorie.

L'option 2 est la clé. **Ton brief n'est pas figé. Il évolue avec ton usage.** Au bout de quelques semaines, ton brief devient pointu sur tes vrais cas.

### e) Tu sauvegardes tes briefs

Sauvegarde tes briefs dans un dossier dédié sur ton disque (par exemple `~/Documents/briefs-claude/`). Versionne avec un nom de fichier daté : `brief_tri_mails_v2_2026-05-15.md`. Comme ça tu peux revenir à une version précédente si une modification t'a fait régresser.

---

## Étape 5 — Évaluer ton agent

Au bout de **1 semaine d'utilisation** (donc une dizaine de fois), pose-toi 5 questions :

1. **Est-ce que je gagne du temps ?** Combien de minutes économisées par utilisation × combien d'utilisations par semaine ?
2. **Est-ce que Claude se trompe encore sur les mêmes cas ?** Si oui, c'est que ces cas ne sont pas couverts par ton brief actuel.
3. **Est-ce que je copie-colle le brief à chaque fois ?** Si oui, c'est normal — c'est exactement ce que ferait du code automatisé.
4. **Est-ce que je suis tenté de sauter le brief ?** Si oui, c'est le signe que tu commences à mémoriser tes propres règles. Bon signe.
5. **Est-ce que la sortie est vraiment exploitable ?** Tu peux la copier-coller dans ton CRM, dans ton agenda, dans ton mail ?

**Si 4 questions sur 5 ont une réponse positive**, ton agent est un succès. Tu peux passer au tuto suivant et envisager de l'automatiser via l'API.

**Si tu hésites sur plusieurs questions**, **n'attaque pas l'API**. Itère sur le brief jusqu'à ce que ce soit solide. Tu construirais sur du sable sinon.

---

## Les limites de l'agent en chat

Soyons honnêtes : l'agent en chat (niveau 2 du tuto 02) a des limites réelles :

- **Tu dois être devant ton écran.** L'agent ne tourne pas sans toi.
- **Tu copies-colles à chaque fois.** Aucune intégration avec ton mail, ton CRM, ton agenda.
- **Tu n'as pas de trace systématique.** Si tu veux savoir combien de mails tu as traités la semaine dernière, tu dois compter à la main.
- **Le contexte se perd entre conversations.** Si tu fermes le chat, tu repars de zéro la fois suivante (sauf à recoller le brief).
- **Les coûts sont peu visibles.** Tu sais combien Claude.ai te coûte par mois, pas combien chaque tâche te coûte précisément.

Ces limites **ne sont pas des défauts**. Elles sont normales à ce niveau. Et elles te disent quand passer au niveau suivant — c'est exactement le sujet du tuto 06.

---

## Le piège classique : sauter cette étape

Beaucoup de débutants veulent passer directement à du code Python parce que ça fait "plus sérieux". C'est une erreur, pour trois raisons :

1. **Tu écris du code que tu ne saurais pas déboguer.** Si Claude (via API) sort un résultat moyen, tu ne sais pas si c'est ton prompt ou ton code Python qui pèche. En chat, tu vois immédiatement.

2. **Tu paies pour rien.** Faire 100 itérations sur un brief en chat te coûte quelques euros sur ton abonnement Claude.ai. Faire 100 itérations via API te coûte le tarif de chaque appel, **et** tu dois redéployer ton code à chaque fois.

3. **Tu te décourages.** Un agent qui marche, c'est gratifiant. Du code qui plante toutes les 10 minutes au début, c'est démoralisant. La phase chat est ta phase "facile", qui te donne les wins rapides dont tu as besoin pour continuer.

**Reste en chat tant que tu n'as pas la stabilité.** Tu sauras quand passer.

---

## Récap mémorisable

> 1. Choisis une **vraie tâche** que tu fais 1×/semaine minimum.
> 2. Écris le **brief** (tuto 03) et un **mini-CLAUDE.md** (tuto 04 simplifié).
> 3. Routine : **nouvelle conversation, colle brief + contexte, travaille, sauvegarde**.
> 4. Quand Claude se trompe → **modifie le brief**, pas seulement la conversation.
> 5. Évalue après une semaine. Si ça marche, c'est ton premier agent. Reste à ce niveau tant que tu n'as pas la stabilité.

---

## Pour aller plus loin

- **Tuto 06 — Quand et pourquoi passer à l'API ?** : les signaux qui te disent qu'il est temps d'automatiser.
- **Tuto 07 — Premier appel API** : ton premier script Python qui fait la même chose que ton agent en chat.

---

[← Retour au sommaire](../README.md)
