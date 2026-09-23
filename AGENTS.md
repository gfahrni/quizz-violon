# AGENTS.md — quizz-violon

## But du projet
App **« Quizz violon »** pour **Ambre** (joue du violon) sur **iPad mini 4**
(Safari ancien, max iPadOS 15.x).
Jeu d'oreille : on lui joue une **note de violon**, elle doit **nommer la note**
(Do, Ré, Mi... sans l'octave). Partie de 10 à 20 essais, objectif **5 points**.
Thème **rose** (même palette Peach que `missions-soir` / `instruments-check`).
Déployé sur **GitHub Pages** (repo `gfahrni/quizz-violon`).

## Règles du jeu
- Bouton **« Nouvelle partie »** sur l'écran d'accueil.
- Chaque essai :
  1. Une note de violon est tirée au hasard dans la liste autorisée (`notes.json`).
  2. La note est **jouée automatiquement 3 s**, et le **chrono de 10 s démarre**
     dès la première lecture.
  3. Bouton **« Réécouter »** : **appui maintenu = la note joue**, **relâchement = stop**
     (rejouer ne remet PAS le chrono à zéro).
  4. Elle répond en tapant une des **touches de notes** (Do à Si, seules les notes
     existantes dans `notes.json` sont affichées).
  5. **1re réponse juste** → **+1 point**.
     **1re réponse fausse** → **2e chance** ; si la 2e est juste → **+0,5 point**.
     Fausse aux deux, ou **temps écoulé (10 s)** sans réponse juste → **0 point**.
     *(Validé : le chrono de 10 s couvre toute la note, 2e chance incluse.)*
  6. Fin d'essai → **pause silencieuse de 2 s** → essai suivant.
- **Score / compteur** : étoiles qui se remplissent (5 étoiles, demi-étoile possible)
  + compteur de la forme **`points / essais_max`**.
  - `essais_max` = **max(10, numéro de l'essai en cours)**, plafonné à **20**.
    Donc 4/10, puis 4/11 quand on démarre le 11e essai, ... jusqu'à 4/20.
- **Fin de partie** :
  - **Victoire** dès que `points >= 5` **et** `essais >= 10` (donc pas avant 10 essais).
  - **Défaite** si après **20 essais** `points < 5`.
  - Écran **« Bravo »** (+ étoiles) avec bouton **« Rejouer »**.
  - Écran défaite : **« Tu as fait X points »** avec bouton **« Rejouer »**.

## Notes autorisées (source unique : `notes.json`)
- Plage : **Sol (une octave sous l'octave normale) → Mi (une octave au-dessus)**
  = **G3 → E5** en notation scientifique (octave « normale » = octave 4).
  *(Validé)*
- Dièses autorisés : **Do# (C#)** et **Fa# (F#)** uniquement.
  Pas de La#/Si♭, Ré#/Mi♭, Sol#/La♭.
- Notes résultantes (16) :
  `G3, A3, B3, C4, C#4, D4, E4, F4, F#4, G4, A4, B4, C5, C#5, D5, E5`.
- **Touches de réponse = classes de hauteur** dérivées de `notes.json` :
  Do, Do#, Ré, Mi, Fa, Fa#, Sol, La, Si (9 touches).
- Changer la liste des notes = **éditer `notes.json`** (les touches se regénèrent).

## Thème / UI
- Palette rose Peach : texte `#6b103f`, boutons `#fff` + bord `#ffcc33`,
  accent `#9d174d`, étoiles `#ffd43b`, dégradé fond `#ffe3ef → #c2255c`.
- Écran d'accueil, écran de jeu, écran de fin (bravo / défaite).
- Tactile : grosses zones, pas de hover-only.

## Stack / structure
- HTML/CSS/JS **statique**, sans build, sans framework, sans dépendance.
- Fichiers prévus :
  - `index.html` : écrans + logique du jeu (JS inline, tourne en ES5).
  - `violon-v1.css` : thème rose versionné (renommer à chaque change visuel).
  - `notes.json` : **liste autorisée des notes** (id, nom FR, octave, classe,
    fréquence, fichier audio). Fallback en dur dans le JS si fetch échoue.
  - `audio/<id>.mp3` : une note par fichier (offline, stocké dans le repo).
    Nom de fichier : `#` → `s` (ex. `C#4` → `Cs4.mp3`).
  - `generer-notes.py` : script local one-shot (ffmpeg) qui télécharge 8 échantillons
    VSCO de base (`audio-src/`, ignoré par git) et ré-échantillonne (`asetrate`) pour
    produire les 16 mp3. Vérifie la cohérence avec `notes.json`.
- État de partie en `localStorage` sous préfixe `violon-v1-` (`violon-v1-game`).

## Audio — source libre
- Besoin : **une note de violon tenue par hauteur** (16 fichiers), idéalement **CC0**.
- **Décision : VSCO 2 Community Edition** (CC0-1.0, `github.com/sgossner/VSCO-2-CE`,
  dossier `Strings/Solo Violin/Arco Vib`). Bases `_f` : G3, A3, C4, E4, G4, A4, C5, E5.
  Les autres notes sont obtenues par décalage de +1/+2 demi-tons (ré-échantillonnage).
- Sortie visée : mp3 mono ~96–128 kbps, normalisés, courts (~2-3 s), commités dans `audio/`.
- **Note** : les échantillons de l'Université d'Iowa sont des **gammes glissées**
  (ex. `G3B3`), pas des notes isolées → non retenus tels quels.

## Contraintes iPad mini 4 (importantes)
- Compatible **Safari iOS 15** : JS ES5, pas de modules ES, pas d'optional chaining.
- Garder les meta iOS : `viewport-fit=cover`, `apple-mobile-web-app-capable`,
  `apple-mobile-web-app-status-bar-style`, `apple-mobile-web-app-title`.
- **Audio iOS** : le premier son ne peut démarrer que sur un **geste utilisateur**.
  → la 1re note est lancée par le tap sur « Nouvelle partie » (geste = OK).
- Pas de lecture `hold` fiable sans `<audio>`/Web Audio : à tester en conditions réelles.
- Tester : ajout à l'écran d'accueil + plein écran.

## Conventions de travail
- Modifier `index.html` directement, garder le fichier petit et lisible.
- `notes.json` = source de vérité des notes autorisées ; fallback en dur dans le JS.
- Préfixe d'état `violon-v1-` pour toutes les clés `localStorage`.
- Un test = un commit clair (ex : `test: hold-to-replay audio iOS 15`).
- Ne pas ajouter de tooling/build sans demande explicite.
- Langue UI : **français**.

## Décisions prises
1. **Plage** : G3 → E5 (octave normale = octave 4). **Validé.**
2. **2e chance / chrono** : le chrono de 10 s couvre toute la note, 2e chance incluse. **Validé.**
3. **Réécoute** : maintenir « Réécouter » ne remet pas les 10 s à zéro. **Validé.**
4. **Audio** : **VSCO 2 Community Edition (CC0)**. **Validé.**
5. Octave ignorée : la réponse est la **classe** (Do, Do#...), pas l'octave.
6. Persistance : la partie en cours est sauvegardée et reprise via « Reprendre la partie ».
7. Étoiles : 5 étoiles, demi-étoile pour 0,5 point.
8. Plafond d'essais : 20 ; compteur = `points / max(10, essai)`.

## Tests
- Logique de jeu validée par harnais Node (DOM/audio/timers simulés) : 26 cas OK
  (victoire à 10 essais, défaite à 20, demi-points, timeouts, compteur /11, persistance).
