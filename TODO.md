# TODO — quizz-violon

Cocher au fur et à mesure. Chaque item terminé = build/testé sur iPad mini 4 si visuel/audio.

## Phase 0 — Décisions
- [x] Plage de notes G3 → E5.
- [x] Chrono pendant la 2e chance (couvre toute la note).
- [x] Réécoute : chrono non remis à zéro.
- [x] Compteur : plafond 30, formule `points / max(10, essai)`.
- [x] Réponse = classe de hauteur (sans octave).
- [x] Persistance de la partie en cours.
- [x] 5 étoiles + demi-étoiles.
- [x] Source audio : VSCO 2 Community Edition (CC0).

## Phase 1 — Scaffolding
- [x] Initialiser le repo `quizz-violon` (git sur `main`, `.gitignore`).
- [x] Créer `index.html` (3 écrans : accueil / jeu / fin, meta iOS).
- [x] Créer `violon-v1.css` (thème rose Peach, étoiles, touches).
- [x] Créer `notes.json` (16 notes : id, nom, classe, octave, fréquence, fichier).
- [x] Fallback en dur des notes dans le JS si le fetch échoue.

## Phase 2 — Audio (VSCO 2 CE → fichiers locaux)
- [x] Choisir la source : VSCO 2 CE (CC0), violon solo `Arco Vib`.
- [x] Écrire `generer-notes.py` (télécharge 8 bases + ré-échantillonne → mp3).
- [x] Générer les 16 notes (G3 ... E5).
- [x] Vérifier la justesse (toutes < 25 cents de la fréquence attendue).
- [x] Vérifier durée ~3 s et format mono 128 kbps.
- [x] Origine + licence documentées dans `AGENTS.md`.

## Phase 3 — Moteur de jeu (logique pure)
- [x] Tirage aléatoire d'une note (évite la répétition immédiate).
- [x] Machine à états d'un essai : note → 1re réponse → 2e chance → fin.
- [x] Chrono 10 s démarré à la 1re lecture ; stop à la réponse juste / timeout.
- [x] Score : +1 (1re juste), +0,5 (2e juste), 0 (double erreur ou timeout).
- [x] Pause silencieuse 2 s entre deux essais.
- [x] Compteur `points / max(10, essai)` plafonné à 30.
- [x] Fin : victoire (`points>=10 && essais>=10`), défaite (essai 30, `points<10`).
- [x] Bouton « Réécouter » en appui maintenu (play on hold / stop on release).

## Phase 4 — UI / écrans
- [x] Écran accueil : titre + boutons « Reprendre » / « Nouvelle partie ».
- [x] Écran jeu : réécoute, touches Do→Si (dérivées de `notes.json`), chrono,
      étoiles, compteur.
- [x] Feedback juste / faux / timeout avec révélation de la bonne note.
- [x] Écran victoire : « Bravo » + étoiles + « Rejouer ».
- [x] Écran défaite : « Tu as fait X points » + « Rejouer ».
- [x] Pause de 2 s : touches désactivées, pas de réponse possible.

## Phase 5 — État / persistance
- [x] État sous préfixe `violon-v1-` (`violon-v1-game`).
- [x] Reprendre la partie en cours (bouton « Reprendre la partie »).
- [x] « Rejouer » et fin de partie = remise à zéro propre.

## Phase 6 — Tests iPad mini 4 (réels)
- [ ] Ajout à l'écran d'accueil + plein écran, safe-area OK.
- [ ] 1er son après tap (contrainte autoplay iOS).
- [ ] Hold-to-replay : joue tant qu'on appuie, stop au relâchement.
- [ ] Chrono 10 s fiable (pas de dérive en arrière-plan).
- [ ] Pause 2 s respectée, enchaînement des essais fluide.
- [ ] Compteur 4/10 → 4/11 → ... → 4/30, jamais > 30.
- [ ] Fin victoire à 10 points (min 10 essais) et fin défaite à 30 essais.
- [ ] Demi-étoiles / demi-points (½) affichés correctement.
- [ ] Tester avec les doigts d'Ambre (taille des touches, lisibilité).

## Phase 7 — Finition / déploiement
- [ ] Nettoyer `index.html` (petit, lisible, ES5) — fait, à revalider sur iPad.
- [ ] Vérifier licence/attribution audio (VSCO 2 CE, CC0).
- [ ] Créer le repo GitHub `gfahrni/quizz-violon` + push `main` → GitHub Pages.
- [ ] Vérifier le cache Safari (renommer le CSS si changement visuel).
- [x] Mettre à jour `AGENTS.md` (structure finale + décisions prises).
