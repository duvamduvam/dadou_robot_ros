# Déclenchement de la conversation — détecter l'intention de communiquer

*Étude du 2026-07-12, déclenchée par le constat qu'il n'y a « très peu
d'intelligence dans le déclenchement de la conversation » : le chat écoute en
permanence dès qu'il est ON, sans aucun lien avec la présence ou l'attitude
d'un passant. Statut : **PROPOSITION — plan à griller avant lancement**
(recommandation : `/grill-me`, comme pour le télédiagnostic). Périmètre :
perception + machine à états d'engagement + armement du micro/de la parole.
Les ROUES ne sont PAS concernées (l'abordage actif « le robot se déplace vers
la personne » est explicitement hors périmètre tant que les verrous roues —
test scénique, W1 — ne sont pas levés).*

## 1. Le problème

Didier est destiné à la déambulation : parler à des gens dans la rue. Or le
déclenchement actuel de la conversation est purement acoustique :

- Dès que le toggle `chat` est ON, le `ConversationEngine` tourne en boucle
  ([conversation.py](../../dadou_vision_ros/vision/ai/conversation.py)) : le
  VAD à énergie ([vad.py](../../dadou_vision_ros/vision/audio/vad.py), seuil =
  médiane du bruit de fond × 1,3) déclenche STT → LLM → TTS sur **n'importe
  quel bruit** dépassant le seuil. Le seul garde-fou est le filtre
  « ≥ 2 caractères alphanumériques » après transcription.
- **Aucun signal de perception n'entre dans la décision** : pas de lien avec
  `/vision/person`, pas de notion de personne présente, s'approchant, faisant
  face ou parlant AU robot.
- **Aucune notion de session** : une seule conversation ChatDB pour toute la
  vie du node, pas de timeout, pas de début/fin liés à l'arrivée ou au départ
  d'une personne.

Conséquences déjà observées : chat_node coupé sur le Pi vision depuis le 11/07
parce qu'il écrasait le visage au moindre bruit. En rue, ce serait pire :
Didier répondrait au trafic, parlerait dans le vide, ou interpellerait des
gens qui passent sans intention — exactement le mode d'échec dominant mesuré
par la littérature (§3.2).

L'objectif est déjà écrit dans la vision V3 de
[`ARCHITECTURE.md`](../../dadou_vision_ros/ARCHITECTURE.md) côté vision :
*« il décide seul de suivre du regard, d'interpeller quelqu'un […] Didier
remarque quelqu'un qui entre, le suit du regard, engage la conversation »*.
Cette étude en est la concrétisation.

## 2. Ce qu'on a déjà (état des lieux 2026-07-12)

**Signaux disponibles** :

| Signal | Source | Contenu | Fréquence |
|---|---|---|---|
| Position d'une personne | `/vision/person` | azimut [-1..1], élévation, confiance | ~16,7 Hz max |
| Distance approximative | `/vision/person_box` | azimut, **hauteur de silhouette** [0..1] (proxy monoculaire, EMA) | idem |
| Parole/silence | VAD interne chat_node | machine à états CALIBRATING/IDLE/SPEECH + RMS | interne, **non exposé en topic** |
| Séquence en cours | `animation_state` (latché) | nom ou "", time=remaining_ms | événementiel |
| Toggles régie | `chat`, `gaze`, `follow` | "on"/"off" | console web |

Détection : MediaPipe EfficientDet-Lite0 int8 (~24 % CPU du Pi 5 à 16,7 Hz),
une seule cible retenue à la fois (adhérence anti-saut dans
`target_picker.py`).

**Signaux absents** : pose corporelle (un backend MediaPipe Pose existe dans
`vision/tracking/bench_detection.py`, jamais branché en prod), détection et
orientation du visage, trajectoire dans le temps (au-delà du lissage EMA
frame à frame), multi-personnes, niveau micro ambiant exposé, état interne du
chat (écoute/réfléchit/parle) publié en ROS.

**Atouts en place** : le gaze cou+yeux est VALIDÉ EN RÉEL (12/07) — c'est
précisément le « signal de disponibilité » que la littérature recommande
d'utiliser en premier (§3.2) ; l'arbitrage `animation_state` protège déjà le
visage et la tête pendant les séquences ; le toggle `chat` est le canal
d'activation naturel qu'un détecteur d'intention piloterait.

## 3. État de l'art (recherche du 2026-07-12)

### 3.1 Les zones de Hall — la grille de distances de toute la littérature

Hall (1966), validé humain-robot par Walters et al. (2005) : intime 0–0,45 m,
personnelle 0,45–1,2 m, **sociale 1,2–3,6 m** (interaction avec des
inconnus), publique > 3,6 m. La zone sociale est la fenêtre d'abordage :
au-delà, un signal d'intention n'est pas lisible fiablement ; en deçà, on est
déjà dans l'espace personnel de la personne.

### 3.2 Michalowski et al. 2006 — la position statique ne suffit PAS

« A Spatial Model of Engagement for a Social Robot » (CMU Roboceptionist,
12,5 h de vidéo annotée,
[PDF](https://www.ri.cmu.edu/pub_files/pub4/michalowski_marek_piotr_2006_3/michalowski_marek_piotr_2006_3.pdf)) :

- Un modèle à zones fixes **surestime massivement** l'engagement : 1500
  personnes vues « engaged » par le robot contre 174 réelles — l'écart, ce
  sont les gens qui **passent**. 66 % des rotations de tête du robot visaient
  de simples passants.
- 54 % des salutations verbales bien dirigées ne recevaient AUCUNE réponse
  (gêne sociale documentée).
- **Asymétrie clé** : tourner la tête est peu coûteux socialement (26 % de
  suivi d'interaction si bien dirigé) et peut être généreux/anticipé ; la
  **parole** doit être conservatrice (48 % de suivi si bien dirigée, mais un
  échec = malaise réel).
- Conclusion des auteurs : **direction et vitesse du mouvement sont plus
  fiables que la position** ; leur modèle révisé : *Present* (passage
  rapide/tangentiel → ignorer) → *Interested* (approche ou mouvement lent →
  tourner la tête) → *Engaged* (quasi stationnaire + visage détecté → le
  robot peut parler) → *Interacting*.

### 3.3 Satake, Kanda et al. — l'abordage de passants (ATR)

« How to Approach Humans? » (HRI'09, centre commercial réel,
[PDF](https://dl.acm.org/doi/10.1145/1514095.1514117)) :

- Taxonomie des échecs d'un abordage naïf : *unreachable* (cible partie),
  *unaware* (ne perçoit pas le robot), *unsure* (perçoit mais hésite),
  *rejected* (ignore délibérément).
- Classification de trajectoires par SVM (fast-walk / idle-walk / wandering /
  stop) : **88,9 % de reconnaissance** — la trajectoire seule est un signal
  très exploitable.
- Résultat terrain : 56 % de succès (33/59) avec anticipation de trajectoire
  contre 35 % (20/57) en naïf. Le **rejet reste incompressible** (~27-29 %
  dans les deux cas) : il dépend de la volonté humaine, pas du robot — ne
  jamais insister.
- Suite 2022 (« Behavioral Assessment… », Int. J. Social Robotics,
  [PMC9331028](https://pmc.ncbi.nlm.nih.gov/articles/PMC9331028/)) : critère
  d'arrêt opérationnel = présence continue **3 s** dans une zone de
  1,2 × 2,5 m devant le robot. Les **enfants** s'arrêtent significativement
  plus (p<0,01), les **groupes** s'arrêtent et écoutent plus que les
  personnes seules. Un robot « en difficulté » attire plus qu'un robot qui
  salue ou danse — et attire bien plus qu'un humain dans le même rôle
  (stop rate humain : 0,8–4,1 %).

### 3.4 Rich et al. 2010 — les « connection events » et leurs durées

« Recognizing Engagement in HRI » (HRI'10,
[PDF](https://dl.acm.org/doi/10.1145/1734454.1734580)) : l'engagement en
cours se mesure par 4 événements (regard dirigé, regard mutuel,
question-réponse, backchannel). Chiffres réutilisables comme timeouts :
établissement du regard mutuel ~0,6–0,7 s ; temps moyen entre événements de
connexion (MTBCE) **5,7 s** chez l'humain, ~3 s dans leur implémentation
robot ; timeouts calibrés 1,8–3,1 s. Un silence bien au-delà du MTBCE =
désengagement.

### 3.5 Vaufreydaz et al. 2015 — 7 features suffisent

« Starting Engagement Detection Toward a Companion Robot »
([arXiv:1503.03732](https://arxiv.org/abs/1503.03732)) — le plus proche d'une
spec pour nous :

- Validation expérimentale que **distance et vitesse seules ne suffisent
  pas** (on passe près du robot sans le vouloir).
- Classe WILL_INTERACT (détecter l'intention AVANT l'interaction) : SVM
  multimodal à 3 classes → **précision 0,95 / rappel 0,93**.
- Sélection MRMR : **7 features suffisent**, hétérogènes — dont *taille et
  position du visage détecté* (proxy bon marché de proximité + face-à-face),
  localisation sonore, vitesse latérale, et **rotation des épaules**
  (métrique de Scheflen, validée là pour la première fois en HRI).

### 3.6 MuMMER 2019 — le pipeline complet, et ses compromis

Pepper en centre commercial ([arXiv:1909.06749](https://arxiv.org/abs/1909.06749)) :
pose de tête via OpenHeadPose **comme proxy du regard** (le vrai eye-tracking
est explicitement jugé trop coûteux en multi-personnes), fusion distance +
orientation de tête + localisation sonore → une probabilité d'attention
comparée à un seuil, **pénalité anti-re-sollicitation** de quelqu'un qui
vient d'interagir. Perception complète à 10 fps. Limite documentée par
ailleurs (HRI'15) : la pose de tête est un proxy dégradé du regard,
surtout chez l'enfant.

### 3.7 Spécificités rue / espace public

- Le robot doit **signaler sa propre disponibilité** : orientation du regard
  et du corps du robot vers la personne = l'invitation la plus lisible
  (Satake : le différentiel d'orientation robot→cible est un facteur clé de
  la « conscience » du passant ; littérature gaze-cues piétons 2023).
- Biais à éviter : le « robot privilege » (Pelikan 2024) — les robots publics
  tendent à faire porter l'ajustement au piéton. Didier doit inviter, jamais
  imposer ni bloquer le passage.
- En rue ouverte (vs centre commercial), l'effet de surprise amplifie les
  échecs *unaware*/*unsure* ; les groupes et les enfants seront les
  interactions majoritaires (46 % de groupes chez Michalowski ; souvent une
  personne en entraîne une autre).

### Les 5 signaux au meilleur rapport fiabilité/coût (convergence des sources)

1. **Direction + vitesse d'approche** (dérivée temporelle de la boîte
   englobante — aucun modèle ML nouveau requis).
2. **Arrêt soutenu ≥ 3 s en zone sociale** (position + minuteur).
3. **Taille/position du visage détecté** (détecteur de visage léger — proxy
   de proximité ET d'orientation frontale).
4. **Pose de tête** comme proxy du regard (MediaPipe, ~18 fps mesurés sur
   Pi 5 en config « balanced »).
5. **Orientation du corps/des épaules** (pose corporelle type
   MoveNet/YOLO-pose ; coût quasi constant avec le nombre de personnes pour
   les architectures bottom-up).

La parole adressée et le geste explicite sont des signaux forts mais chers à
détecter fiablement (attribution de locuteur = réseau de micros) : à réserver
en **confirmation**, pas en détection primaire.

## 4. Principes de conception pour Didier

- **P1 — L'intention se lit dans le mouvement, pas la position.** Le cœur du
  détecteur est temporel : trajectoire de l'azimut et dérivée de la hauteur
  de silhouette (approche/éloignement), pas des zones statiques.
- **P2 — Escalade asymétrique.** Le regard du robot est généreux (se tourner
  vers quiconque semble intéressé = déjà en place avec le gaze) ; la
  **parole est conservatrice** (n'engager verbalement qu'à signaux forts
  cumulés). Un regard raté ne coûte rien, une interpellation ratée coûte.
- **P3 — Didier signale sa disponibilité.** L'invitation, c'est lui : gaze
  vers la personne, expression faciale d'accueil. Théâtralement c'est aussi
  le plus intéressant (le « robot en difficulté » de Satake 2022 attire plus
  que celui qui salue — matière à jeu de scène).
- **P4 — Fenêtre d'engagement = zone sociale (1,2–3,6 m), signal fort =
  arrêt soutenu ~3 s.** Nécessite de calibrer le proxy hauteur de
  silhouette → mètres.
- **P5 — Le rejet est incompressible : ne jamais insister.** Pénalité
  anti-re-sollicitation (cooldown) après un refus ou une conversation close.
- **P6 — L'engagement définit la session.** Début de session = engagement
  confirmé ; fin = départ de la personne ou silence ≫ MTBCE (~10-15 s sans
  échange) → clôture propre (reset de l'historique LLM, retour au neutre).
- **P7 — Le micro est armé par l'engagement, plus jamais seul.** Le VAD
  passe de déclencheur permanent à **confirmateur** : il n'écoute que quand
  quelqu'un d'engagé est là. Résout structurellement le problème « chat_node
  répond au bruit ».
- **P8 — Groupes et enfants sont le cas nominal, pas l'exception.** Le proxy
  de distance par hauteur de silhouette est biaisé pour les enfants (un
  enfant proche ≈ un adulte loin) — à garder en tête dès la calibration.
- **P9 — Jamais les roues.** L'engagement ne publie RIEN vers la chaîne
  cmd_vel. L'abordage mobile (aller vers la personne, façon Satake) est un
  chantier ultérieur, conditionné aux verrous roues et à un grill dédié.

## 5. Architecture proposée

### 5.1 Un node `engagement_node` (Pi vision), logique pure testée

Nouveau node à côté de `person_tracker_node`, même patron que le reste du
projet : node = I/O, logique dans un module pur testé sans ROS
(`vision/engagement/…`).

- **Entrées** : `/vision/person_box` (azimut + hauteur + confiance), plus
  tard les signaux E2/E3 (visage frontal, pose de tête), `animation_state`
  (se taire pendant une séquence de spectacle), toggle régie.
- **Cœur** : fenêtre glissante de quelques secondes sur la cible → features
  (vitesse d'azimut, dérivée de hauteur = approche, stationnarité, temps de
  présence en zone sociale) → **machine à états** :

```
ABSENT → PRESENT → INTERESTED → ENGAGED → IN_CONVERSATION → COOLDOWN
```

  - PRESENT : personne détectée, loin ou en passage rapide/tangentiel →
    ne rien faire.
  - INTERESTED : approche (hauteur croissante) OU mouvement lent en zone
    sociale → **regard** (le gaze existant) + expression curieuse. Généreux.
  - ENGAGED : quasi stationnaire en zone sociale ≥ ~3 s (E2 : ET visage
    frontal) → expression d'accueil, **micro armé**. Conservateur.
  - IN_CONVERSATION : le VAD confirme une parole exploitable → session
    ouverte, l'état est tenu tant que les échanges continuent.
  - COOLDOWN : après clôture ou non-réponse à une invitation → pas de
    ré-engagement de la même situation pendant N s (~30-60 s).
  - Toute perte de personne > N s → retour ABSENT + clôture de session.

- **Sorties** : topic `engagement` latché (état + confiance, patron
  `animation_state`), consommé par chat_node ; à terme un topic d'intention
  théâtrale (« invite », « accueille ») vers face/animations, en passant par
  l'arbitrage existant.

### 5.2 Adaptations chat_node (Pi vision)

- S'abonner à `engagement` : le VAD n'écoute qu'en ENGAGED/IN_CONVERSATION
  (le toggle `chat` régie reste le master switch — ET logique, comme le gaze
  avec `animation_state`).
- **Sessions** : ouverture/clôture pilotées par l'engagement — nouvelle
  entrée ChatDB par session, reset de l'historique, timeout de silence
  (~10-15 s, inspiré MTBCE), retour visage au neutre en fin de session.
- Publier l'état interne (`listening`/`thinking`/`speaking`) sur un topic —
  nécessaire à l'engagement (tenir IN_CONVERSATION), utile à la régie et au
  télédiagnostic.

### 5.3 Extensions perception, par coût croissant

- **E1 (gratuit)** : tout depuis `/vision/person_box` existant — trajectoire,
  approche, stationnarité. Aucun modèle nouveau.
- **E2 (léger)** : détecteur de visage (MediaPipe face detection) sur la
  cible → taille/position du visage = proxy « me fait face » (feature n°1 de
  Vaufreydaz). Budget CPU à mesurer (le detector actuel prend ~24 %).
- **E3 (plus lourd, à décider plus tard)** : pose de tête et/ou épaules
  (MediaPipe Pose ~18 fps sur Pi 5) pour l'orientation fine ; parole
  adressée en confirmation. Seulement si E1+E2 montrent leurs limites sur le
  terrain.

## 6. Lots proposés

| Lot | Contenu | Validation |
|---|---|---|
| **D0 — instrumentation + calibration** | exposer l'état chat en topic ; calibrer hauteur de silhouette → mètres (personne à 1,2 / 2,4 / 3,6 m, adulte ET enfant si possible) ; rejouer des captures pour constituer un mini-corpus passage vs approche | mesures consignées ici (§8) |
| **D1 — FSM v1, zéro perception nouvelle** | `engagement_node` (logique pure + tests), gate du VAD dans chat_node, sessions + timeout | sim d'abord (perception scriptée `/vision/person_box`, commande existante dans CLAUDE.md) : scénarios passage / approche+arrêt / départ ; puis atelier |
| **D2 — visage frontal** | face detection sur la cible, condition ENGAGED durcie | protocole atelier : passage devant le robot sans le regarder = pas d'armement |
| **D3 — invitation théâtrale + terrain** | expressions d'invitation via arbitrage, éventuel « bonjour » proactif (conservateur, P2), cooldown | première sortie rue encadrée, métriques façon Satake (taux d'arrêt, faux déclenchements) |

Chaque lot suit la méthode maison : logique pure testée → sim → réel, docs
mises à jour dans le même lot. Verrou d'entrée : le **protocole physique
chat_node V2** (chantier 0) doit passer d'abord — inutile de raffiner le
déclenchement d'une conversation jamais validée en réel.

## 7. Inconnues à lever (avant/pendant le grill)

1. **Budget CPU du Pi 5 vision** : detector actuel ~24 % à 16,7 Hz ; que
   reste-t-il pour face detection (E2) voire pose (E3) + whisper + piper ?
   Mesure à faire en conditions chat réelles.
2. **Calibration distance** : fiabilité du proxy hauteur de silhouette en
   rue (enfants, personnes assises, poussettes) — P8.
3. **Micro en rue** : le micro caméra U20 (mono) suffit-il en environnement
   bruyant ? Pas de localisation sonore possible avec un seul micro — la
   « parole adressée » ne pourra être qu'une confirmation faible.
4. **Multi-personnes / attroupement** : `target_picker` ne suit qu'une
   cible ; comportement souhaité quand un groupe entoure Didier ?
5. **Politique d'abordage** : Didier initie-t-il verbalement (D3) ou
   répond-il seulement ? Décision de mise en scène autant que technique.
6. **VAD en rue** : la calibration du bruit de fond (1 s au démarrage)
   tiendra-t-elle dans une rue au niveau sonore variable ? Recalibration
   périodique en IDLE à envisager.
7. **Ré-identification** (la même personne revient) : hors périmètre —
   c'est la « mémoire des gens » de la vision V3.

## 8. Journal des mesures et décisions

*(à remplir au fil des lots — calibrations distance, seuils retenus,
résultats des protocoles)*

## Sources

- Hall, *The Hidden Dimension* (1966) ; Walters et al. 2005 (validation HRI).
- Michalowski, Sabanović & Simmons, *A Spatial Model of Engagement for a
  Social Robot*, IEEE AMC'06 —
  <https://www.ri.cmu.edu/pub_files/pub4/michalowski_marek_piotr_2006_3/michalowski_marek_piotr_2006_3.pdf>
- Satake, Kanda et al., *How to Approach Humans?*, HRI'09 —
  <https://dl.acm.org/doi/10.1145/1514095.1514117>
- Kanda et al., *Behavioral Assessment of a Humanoid Robot When Attracting
  Pedestrians in a Mall*, IJSR 2022 —
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC9331028/>
- Rich, Ponsler, Holroyd & Sidner, *Recognizing Engagement in Human-Robot
  Interaction*, HRI'10 — <https://dl.acm.org/doi/10.1145/1734454.1734580>
- Vaufreydaz, Johal & Combe, *Starting Engagement Detection Toward a
  Companion Robot Using Multimodal Features*, 2015 —
  <https://arxiv.org/abs/1503.03732>
- Foster et al., *MuMMER: Socially Intelligent Human-Robot Interaction in
  Public Spaces*, 2019 — <https://arxiv.org/abs/1909.06749>
- Pelikan, *Encountering Autonomous Robots on Public Streets*, 2024 (« robot
  privilege ») ; littérature gaze-cues piétons (IJSR 2023).
