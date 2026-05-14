# 01 — Comment parler à Claude pour qu'il te comprenne

**Difficulté** : 🟢 Débutant  |  **Durée** : 20 min de lecture, 30 min de pratique

> Le plus dur avec Claude, ce n'est pas qu'il soit incapable. C'est qu'il fait des suppositions silencieuses sur ce que tu veux. Ce tuto te donne les cinq leviers pour qu'il arrête de supposer et qu'il fasse, exactement, ce dont tu as besoin.

---

## Pourquoi ce tuto existe

Au début, j'utilisais Claude comme un meilleur Google. Je tapais une question, je copiais la réponse, je passais à autre chose. Ça marchait pour les questions simples. Pour les vraies tâches métier, c'était imprévisible.

Un jour je lui demande de me résumer un compte-rendu d'hospitalisation. Il me sort un résumé. La fois suivante, même type de document, même question — il me sort un résumé **complètement différent**, avec des sections que je n'avais jamais demandées et qui oublient ce dont j'ai vraiment besoin.

J'ai compris à ce moment-là que ce n'était pas Claude qui était inconstant. C'était moi qui lui parlais mal. Je lui donnais un texte et le mot *"résume"*, en attendant qu'il devine ce que voulait dire *"résumé"* pour moi à ce moment précis.

Ce tuto, c'est ce que j'aurais voulu lire ce jour-là.

---

## Le problème, formulé clairement

Quand tu poses une question à Claude, ton cerveau fournit **silencieusement** plein d'informations qui ne sont pas dans ton message :

- *Quel est le contexte ?* (qui tu es, pourquoi tu demandes, ce que tu vas en faire)
- *Quelles sont les contraintes ?* (longueur, ton, vocabulaire, ce qu'il faut éviter)
- *À quoi ressemble une bonne réponse ?* (format, structure, exemple)
- *Quelles sont tes préférences cachées ?* (oui mais pas comme ça, oui mais court, etc.)

Claude ne lit pas dans tes pensées. Si tu ne lui donnes pas ces informations, il en invente — et il invente **différemment à chaque fois**. C'est ce qui crée l'impression d'inconstance.

La solution : lui donner explicitement ce que ton cerveau croit "évident". Cinq leviers principaux.

---

## Levier 1 — Donne du contexte

Pas une encyclopédie. Juste **trois choses** :

1. **Qui tu es** (ou pour qui tu écris) — médecin, prof, comptable, étudiant, etc.
2. **Pourquoi tu demandes** — un cas concret, pas un exercice théorique
3. **Ce que tu vas en faire** — l'imprimer, l'envoyer à un client, le poster en ligne

### Sans contexte
> *"Explique-moi la TVA."*

Claude va te faire un exposé général. Tu vas le lire en diagonale et ne rien retenir.

### Avec contexte
> *"Je suis comptable et je dois expliquer le mécanisme de la TVA à un commerçant qui débute son activité auto-entrepreneur en France. Il n'a aucune notion fiscale. Donne-moi une explication en langage simple, avec un exemple chiffré sur un produit à 100 €."*

La réponse devient utile, ciblée, et tu peux la copier directement à ton client.

---

## Levier 2 — Fixe les contraintes

Sans contraintes, Claude fait de la moyenne. Une réponse moyenne pour un usage moyen. Tu ne veux pas de la moyenne — tu veux ce qui te sert toi.

Contraintes typiques à donner explicitement :

- **Longueur** : *"En 100 mots maximum"* / *"En 3 paragraphes"* / *"En une page A4"*
- **Ton** : *"Ton chaleureux pour un client fidèle"* / *"Ton neutre administratif"* / *"Ton pédagogique pour un débutant"*
- **Vocabulaire** : *"Évite les anglicismes"* / *"Niveau lycée"* / *"Sans jargon médical"*
- **Ce qu'il faut éviter** : *"Pas de bullet points"* / *"N'inclus pas la conclusion"* / *"Pas de mention de la concurrence"*

Plus tu en mets, plus la réponse devient prédictible. **L'inconstance dans les réponses vient quasi toujours de contraintes absentes.**

---

## Levier 3 — Montre un exemple

C'est le levier **le plus puissant**, et celui que les débutants oublient le plus.

Au lieu de décrire ce que tu veux, **montre un exemple** de ce que tu veux.

### Description abstraite
> *"Fais-moi un résumé structuré du document."*

Trop vague. "Structuré" veut dire mille choses. Tu vas obtenir un résultat aléatoire.

### Avec exemple concret
> *"Fais-moi un résumé du document selon ce format :*
>
> ```
> ## Objet
> [une phrase]
>
> ## Faits principaux
> - [fait 1]
> - [fait 2]
> - [fait 3]
>
> ## Conclusion
> [deux phrases maximum]
> ```
> *"*

Claude voit le gabarit, il le remplit. Tu sais exactement à quoi t'attendre.

Cette technique est tellement puissante qu'elle est la base du **tuto 03 : Construire ton premier brief**.

---

## Levier 4 — Demande un raisonnement étape par étape

Quand la tâche est complexe (analyse, décision, comparaison), demande à Claude de **réfléchir avant de répondre**, pas juste de produire un résultat.

### Sans raisonnement explicite
> *"Quel est le meilleur fournisseur entre A, B et C ?"*

Tu obtiens une réponse rapide qui peut être superficielle.

### Avec raisonnement étape par étape
> *"Quel est le meilleur fournisseur entre A, B et C, pour mon cas (10 commandes/mois, livraison Maroc, budget serré) ?*
>
> *Réfléchis étape par étape :*
> *1. Quels sont les critères qui comptent pour mon cas ?*
> *2. Comment chaque fournisseur se classe sur chaque critère ?*
> *3. Quel est ton verdict, avec deux phrases de justification ?*
> *"*

Claude prend le temps de structurer, tu vois sa logique, tu peux corriger si tu n'es pas d'accord sur le raisonnement.

---

## Levier 5 — Itère, ne recommence pas

Quand la réponse n'est pas tout à fait ce que tu voulais, **ne ferme pas la conversation pour la rouvrir**. Reste dans la même conversation et corrige :

- *"Refais en plus court."*
- *"Garde la structure mais change le ton, j'écris à un client pas à un collègue."*
- *"Bien, sauf le point 3 qui est faux. Voilà la bonne info : XYZ. Reprends en intégrant ça."*

Claude se souvient de la conversation et ajuste. Tu construis ta réponse couche par couche.

**Ne recommence à zéro que si tu changes complètement de sujet.** Sinon, tu perds ton contexte chèrement construit.

---

## Exemple complet : avant / après

### Avant — un message vague
> *"Aide-moi à rédiger une lettre à un fournisseur qui m'a livré du matériel défectueux."*

Tu vas obtenir une lettre générique, probablement trop formelle, qui n'utilise pas les bons termes commerciaux, et qui ne mentionne pas les détails de ton cas.

### Après — les 5 leviers appliqués

> *"Je suis gérant d'un cabinet médical à Fès. J'ai commandé un échographe à un fournisseur en avril dernier. La sonde abdominale livrée présente une distorsion d'image visible en utilisation normale. Mon technicien a confirmé le défaut. Je veux écrire une lettre formelle de réclamation pour obtenir un remplacement gratuit, pas un remboursement.*
>
> *Contraintes :*
> *- Maximum une page A4*
> *- Ton ferme mais courtois, je veux préserver la relation commerciale*
> *- Pas de menace de procédure judiciaire à ce stade*
> *- Vocabulaire commercial standard, pas juridique*
>
> *Structure attendue :*
> *1. Rappel de la commande (date, référence)*
> *2. Description du problème*
> *3. Constat technique*
> *4. Demande précise (remplacement sous X semaines)*
> *5. Formule de politesse*
>
> *Réfléchis avant de rédiger : quels sont les éléments à mettre en avant pour qu'ils prennent ma demande au sérieux sans se sentir agressés ?*
> *"*

Tu obtiens une lettre que tu peux signer directement ou presque.

**Différence de temps de rédaction** : ton message d'origine fait 15 mots, le bon fait 150 mots. Tu prends 2 minutes de plus. Tu gagnes 20 minutes de retouches après.

---

## Le piège du "Claude devine"

Si tu te surprends à penser *"il devrait bien comprendre que..."*, **c'est le signal que tu as une information dans la tête qui n'est pas dans ton message**. Mets-la.

Exemples typiques :

- *"il devrait bien comprendre que je suis pressé"* → ajoute *"réponse courte, je n'ai pas le temps"*
- *"il devrait bien comprendre que c'est pour mon site"* → ajoute *"contenu destiné à mon site web, ton commercial"*
- *"il devrait bien comprendre que c'est une blague"* → ajoute *"sur le ton humoristique"*

Claude n'est pas méchant. Il fait au mieux avec ce qu'il a. Si tu lui donnes plus, il fait mieux.

---

## Combien de contexte est trop ?

Question légitime. La réponse honnête : **rarement trop**.

Tant que tu donnes des infos pertinentes (qui tu es, pour qui, contraintes, format), tu peux écrire 500 mots de contexte sans problème. Claude lit, intègre, ajuste.

Le moment où c'est "trop", c'est quand tu noies l'instruction principale dans du contexte parasite. *"Hier j'ai vu mon comptable, il portait un pull bleu, on a parlé de la TVA et au passage il m'a dit..."* — supprime ce qui n'est pas utile à la réponse.

Test simple : pour chaque phrase de contexte, demande-toi *"si je l'enlève, est-ce que la réponse devient moins utile ?"*. Si non, supprime.

---

## Quand passer au niveau suivant ?

Quand tu te surprends à **réécrire le même contexte** dans plusieurs conversations différentes — par exemple si tu redonnes ta situation médicale, tes contraintes commerciales, ou la structure de tes notes à chaque nouvelle conversation — c'est le moment de structurer ça **une fois pour toutes**.

C'est exactement le sujet du tuto suivant.

---

## Récap mémorisable

> Cinq leviers : **contexte** (qui, pourquoi, pour quoi faire), **contraintes** (longueur, ton, vocabulaire, à éviter), **exemple** (montre, ne décris pas), **raisonnement étape par étape** (pour les tâches complexes), **itère** (reste dans la conversation). Si tu te dis *"il devrait bien comprendre"*, c'est que tu n'as pas écrit ce que tu pensais.

---

## Pour aller plus loin

- **Tuto 02 — Qu'est-ce qu'un agent IA, vraiment ?** : distinguer chatbot, agent à rôle, agent automatique. Comprendre ce qu'on appelle "agent" dans ce repo.
- **Tuto 03 — Construire ton premier brief** : quand le contexte devient stable, on le formalise en un fichier réutilisable.

---

[← Retour au sommaire](../README.md)
