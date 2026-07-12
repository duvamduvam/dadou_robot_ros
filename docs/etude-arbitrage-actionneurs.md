# Arbitrage des actionneurs d'expression (visage LED + tête) — analyse et plan

*Étude du 2026-07-12, déclenchée par un symptôme observé sur le vrai robot : « les
animations de la tête déconnent quand plusieurs programmes tournent en même temps ».
Statut : **analyse complète, plan proposé** — les lots A/B sont recommandés, les
décisions restantes sont en §7. Périmètre : visage LED (`face`) et servos de tête
(`neck`, `left_eye`, `right_eye`). Les roues ne sont PAS concernées (elles ont déjà
leur arbitre, `twist_mux`) mais servent de modèle de référence.*

## 1. Le symptôme et le constat

Sur scène, le visage et la tête sautent/clignotent ou restent bloqués sur une
expression parasite dès que plusieurs programmes tournent (animations + chat,
animations + gaze). Ce n'est pas un bug ponctuel : c'est une propriété de
l'architecture actuelle. **Les topics `face`, `neck`, `left_eye`, `right_eye` sont
des ressources partagées sans arbitre** — tout node qui y publie commande
l'actionneur, et le dernier message reçu gagne.

Le contournement opérationnel en vigueur (chat_node coupé depuis le 11/07, gaze OFF
pendant les séquences, cf. `docs/operations.md`) confirme qu'aucune solution
logicielle n'existe à ce jour.

## 2. L'architecture actuelle : des ressources sans conducteur

Chaque actionneur d'expression est un node consommateur à **souscription plate**
(un seul topic, pas de notion de source) :

- **Visage LED** : `lights_node` s'abonne à `face`
  ([lights_node.py:57-58](../robot/nodes/lights_node.py)) et applique chaque message
  immédiatement (`face_callback` → `Face.update`, [lights_node.py:62-68]) ; le champ
  `anim` du StringTime est **ignoré**, il n'y a **pas de deadman** sur face
  (`FACE ∉ DEADMAN_KEYS`, [animations_node.py:30](../robot/nodes/animations_node.py)).
- **Servos de tête** : un `servo_node` par servo, abonné au topic homonyme
  ([servo_node.py:42-46](../robot/nodes/servo_node.py)) ; chaque message réécrit la
  cible de rampe (`Servo.set_target`).

Les producteurs, eux, sont **mutuellement aveugles** — répartis sur deux machines,
aucun ne sait si un autre est en train de jouer :

| Producteur | Machine | `face` | `neck`/yeux (servos) | Quand il émet |
|---|---|---|---|---|
| `animations_node` (pistes de séquence) | Pi robot | ✔ jusqu'à 20 Hz | ✔ jusqu'à 20 Hz | pendant toute animation (dont « parle ») |
| `chat_node` (émotions, didascalies, thinking) | Pi vision | ✔ | — (via l'animation « parle ») | piloté par le VAD/LLM, **dès le moindre bruit** |
| `gaze_follower_node` (suivi du regard) | Pi robot | — | ✔ ~10 Hz (cou + 2 yeux, [gaze_follower_node.py:182,189](../robot/nodes/gaze_follower_node.py)) | quand `gaze` est ON |
| `web_bridge` (console de régie) | Pi robot | ✔ (whitelist spectacle) | ✔ (whitelist technique, [web_protocol.py:27-28](../conf/ros2_dependencies/robot_web/robot_web/web_protocol.py)) | clics opérateur |

`AnimationManager.playing` ([animation_manager.py:104](../robot/sequences/animation_manager.py))
existe mais **n'est publié nulle part** : aucun producteur ne peut savoir qu'une
animation est en cours. Il n'existe ni mux, ni priorité, ni verrou, ni état partagé
— le seul point du robot qui a tout ça est la chaîne roues (`twist_mux` : remote 100
> web 50 > follow 20 > anim 10, avec péremption par source).

## 3. Scénarios de collision (tous vérifiés dans le code)

- **S1 — bruit ambiant vs animation (le symptôme principal).** Le VAD du chat
  détecte une fin de « parole » sur du bruit de salle → `thinking()` publie
  `face="reflechit"` **avant même le STT** — décision documentée comme volontaire,
  avec limite explicitement « à revisiter si ça se voit mal sur scène »
  ([conversation.py:16-28](../../dadou_vision_ros/vision/ai/conversation.py)). Si le
  tour est abandonné (STT vide), **aucun rattrapage** : le visage reste coincé sur
  « reflechit ». Le helper `idle()` (retour au neutre) existe dans
  [performance.py:128-131](../../dadou_vision_ros/vision/ai/performance.py) mais
  n'est **appelé nulle part**.
- **S2 — le chat peut tuer une animation de spectacle.** `speaking_stop()` publie
  `animation=False` ([performance.py:85-92]) → `animations_node` déclenche un **stop
  GLOBAL** : `"stop"` publié sur TOUS les topics de piste (face, servos, roues,
  audio — [animations_node.py:81-88]). Si une séquence de spectacle (lancée par la
  télécommande ou le web) joue à ce moment-là, elle est écrasée et le visage revient
  au défaut.
- **S3 — alternance à 20 Hz = clignotement.** Deux producteurs qui poussent des
  **noms différents** sur `face` : chaque message reconstruit les 3 pistes et force
  un rendu immédiat (`show_first_frames`, [face.py:88-111](../robot/actions/face.py))
  — le garde-fou « même nom → simple re-timestamp » ne protège que contre un
  producteur unique qui se répète.
- **S4 — gaze vs animation sur les servos de tête.** Même topologie : le gaze écrit
  cou + yeux à ~10 Hz, une animation avec pistes de tête écrit les mêmes topics à
  20 Hz → la cible de rampe saute d'un émetteur à l'autre (à-coups). Aggravé le
  12/07 : le gaze écrit désormais AUSSI les yeux.
- **S5 — toute fin d'animation efface l'état posé par d'autres.** La fin naturelle
  d'une séquence passe par le même stop global (S2) : une expression posée par
  l'opérateur web ou le chat est réinitialisée au défaut.

## 4. Analyse — « ça doit être géré en amont, non ? »

Oui — **le conflit d'intention doit être réglé en amont**. Deux comportements ne
doivent jamais *vouloir* le visage en même temps : il faut un « conducteur » désigné
à chaque instant, comme dans une voiture il n'y a qu'un conducteur. C'est la bonne
intuition, et c'est la cause racine : aujourd'hui **personne ne conduit** — chaque
programme croit être seul au monde.

Mais l'analogie voiture va jusqu'au bout : une voiture réelle a **aussi** un étage
aval câblé (l'ABS/ESP écrase le conducteur, la priorité frein-sur-accélérateur
existe précisément parce qu'un capteur de pédale peut mentir). Les deux étages ne
font pas le même travail :

- **Amont = qui a l'intention de conduire.** Résout le conflit de comportements
  (spectacle vs conversation vs regard). C'est là que se décide « le chat se tait
  pendant une séquence ».
- **Aval = garde-fou d'exécution.** Protège contre un producteur bugué, en retard,
  ou mort en cours de route (messages encore en vol, crash en pleine animation).
  L'amont ne peut pas s'en charger : un process planté ne respecte plus les règles.

Le robot applique déjà ce modèle complet **aux roues** : la règle amont
(« télécommande > tout ») ET l'arbitre aval (`twist_mux` + deadmans). Pour le visage
et la tête, **aucun des deux étages n'existe**. La différence de criticité justifie
en revanche un dosage différent : les roues déplacent 50 kg (l'aval y est de la
sécurité) ; le visage et la tête sont de l'expressif (l'aval y est du confort). D'où
le plan : **l'amont d'abord, l'aval en garde-fou différable**.

## 5. Les solutions, par étage

### 5.1 Correctifs ciblés (indépendants de toute architecture — dépôt vision)

1. **Rattrapage après tour abandonné** : quand le STT est inexploitable, publier
   `idle()` (déjà écrit, jamais appelé) pour ramener le visage au neutre au lieu de
   le laisser sur « reflechit ». Révise la « limite connue acceptée » de
   conversation.py — la condition documentée (« si ça se voit mal sur scène ») est
   remplie. Mettre à jour le test qui fige le choix
   (`test_stt_vide_publie_thinking_puis_rien_dautre`).
2. **Stop ciblé au lieu du stop global** : `speaking_stop()` ne doit arrêter QUE
   l'animation « parle », pas n'importe quelle séquence en cours (S2). Nécessite de
   savoir ce qui joue → dépend de l'état partagé du lot B (ou d'un arrêt
   conditionnel par nom côté `animations_node`).

### 5.2 Étage amont — un conducteur à la fois

- **Option retenue à l'analyse : état d'activité publié.** `animations_node` publie
  un topic latché `animation_state` (nom de la séquence + temps restant, `""` au
  repos). Les comportements autonomes (chat, gaze) s'y abonnent et **se taisent**
  quand une animation joue — règle simple et scénique : *une séquence en cours a la
  main sur le visage et la tête*. Coût faible, zéro changement des contrats
  actionneurs, et il donne au chat l'information qui lui manque pour le stop ciblé
  (5.1-2). Limite assumée : c'est de la coopération (un producteur bugué peut
  l'ignorer) — c'est le rôle de l'aval de couvrir ce cas, plus tard.
- Écartés : les **modes exclusifs** globaux (spectacle XOR conversation) — plus
  rigides, ils interdisent le cas nominal « le chat répond entre deux séquences »
  sans intervention opérateur ; et la **priorité chat > spectacle** — un bruit de
  salle ne doit jamais écraser une expression scriptée.
- **Long terme (déjà en feuille de route)** : l'exécutif comportemental (py_trees) +
  l'Action ROS 2 `PlayAnimation`. C'est la forme achevée du « conducteur unique » :
  les comportements *demandent* les ressources, l'exécutif accorde. Le lot B est un
  pas dans cette direction (l'état publié devient une entrée de l'exécutif), pas un
  détour.

### 5.3 Étage aval — le garde-fou au consommateur (différé)

Arbitrage par source dans `lights_node`/`servo_node` : chaque producteur publie sur
son sous-topic (`face_anim`, `face_chat`, `face_web`…), le consommateur applique la
source la plus prioritaire non périmée — décalque du `twist_mux`. C'est la seule
protection qui tient face à un producteur bugué. **Différé volontairement** : il
change les contrats de 3 dépôts pour des actionneurs non critiques sécurité, alors
que 5.1 + 5.2 suppriment les collisions du fonctionnement normal. À ressortir si les
incidents persistent après le lot B, ou à fusionner dans le chantier exécutif.

## 6. Plan proposé

- **Lot A — correctifs chat_node** (dépôt vision, petit) : A1 rattrapage `idle()`
  après abandon STT (+ test mis à jour) ; A2 préparation du stop ciblé (bascule
  complète quand `animation_state` existe).
- **Lot B — état amont** (dépôt robot + vision) : topic latché `animation_state`
  publié par `animations_node` ; `gaze_follower_node` et `chat_node` suspendent
  leurs émissions visage/tête quand une animation joue ; `speaking_stop()` ne stoppe
  que si « parle » est l'animation courante. Validation en sim (scénarios S1-S5
  rejoués), puis sur le robot — pas de protocole caméra roues requis (aucun chemin
  roues touché), une vérification visuelle visage/tête suffit.
- **Lot C — arbitrage aval par source** : différé (cf. 5.3).
- **Lot D — exécutif py_trees + `PlayAnimation`** : feuille de route existante,
  absorbe A2/B à terme.

En attendant les lots A/B, les règles opérationnelles restent en vigueur : chat_node
coupé pendant les sessions visage/spectacle, gaze OFF pendant les séquences.

## 7. Décisions à valider / inconnues

1. **Valider la règle amont** « une animation en cours a la main sur visage + tête »
   (le chat et le gaze attendent la fin). Variante possible : le gaze reprend la main
   sur le cou seul si la séquence n'a pas de piste `neck` — raffinement à trancher au
   lot B, pas avant.
2. **thinking() dès le speech_end** : on le garde (réaction honnête, choix scénique
   documenté) — seule la sortie (rattrapage idle) change. À confirmer.
3. Le **web** (console de régie) reste hors arbitrage amont : l'opérateur humain
   prime, comme la télécommande pour les roues. Un clic face/servo pendant une
   animation continuera d'entrer en concurrence — acceptable (acte volontaire) ?
4. Forme exacte d'`animation_state` (QoS latché, contenu : nom seul ou nom+restant)
   — à spécifier en tête du lot B.
