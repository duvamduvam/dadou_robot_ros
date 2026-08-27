# Chantiers — tableau de bord

*Le point d'entrée du pilotage : statut, prochaine action et verrous de chaque
chantier. Créé le 2026-07-12 en dégraissant CLAUDE.md (qui était devenu un
journal de bord illisible).*

**Convention de tenue** (pour que ça ne se re-dégrade pas) :
- Chaque lot terminé met à jour **sa ligne** du tableau et **sa section** ici —
  pas CLAUDE.md (qui ne garde que les règles, commandes et priorités de tête).
- Le détail des décisions vit dans le **doc du chantier** (`etude-*.md`) ;
  ici, l'état et la prochaine action ; dans les **commits**, l'historique.
- Un chantier clos passe dans sa section avec la mention CLOS + date, et sort
  du tableau au bout d'un moment.

## Vue d'ensemble

| Chantier | Statut | Prochaine action | Verrou / condition |
|---|---|---|---|
| **0. Conversation (chat_node V2)** | code COMPLET, validé sim ; jamais testé matériel | protocole physique complet (conversation au casque, caméra à l'appui) | rebuild image ARM vision ; Pi 5 sur alim 27 W |
| **1. Test scénique au sol** | À FAIRE — première fois que cmd_vel roule au sol | séquence de spectacle complète, télécommande en main | — (c'est LUI le verrou des autres) |
| Interface web / télé-présence | W0 + console + W3-sim FAITS ; bringup réel actif (sans drive) | W1 : source e_stop + coup-de-poing sans fil | roues web réel ⟸ test scénique (1) + protocole caméra dédié |
| Télédiagnostic par agent IA | plan décidé ; étape 1 « trousse d'atelier » FAITE | étape 2 : boîte noire rosbag + bouton START | étape 3 ⟸ RAM du Pi 4 à relever (`ssh r 'cat /proc/meminfo'`) |
| Conversation en déambulation (intention + contenu) | plan DÉCIDÉ (grillé 12/07) ; D0 outillage + personas commutables FAITS 13/07 | campagne D0 (robot allumé) ; textes personas à valider avec David | D1+ ⟸ protocole physique chat_node V2 (0) ; D6 ⟸ verrous roues |
| Voix de Didier (ventriloquie ↔ synthèse) | OUVERT 26/08 ; cadre + état de l'art posés, **arbitrage artistique suspendu** ; **26/08 : « l'effet robot » de prod est un ÉCRÊTEUR DUR à ±3000 (−20,8 dBFS) — facteur de crête 13,5 dB → 3,1 dB, confirmé à l'oreille** (étude §2) **V3 palier minimal FAIT 26/08** (5,2 min en personnage au SM58, pupitre `essais/voix/enregistre.py`) ; **CLONAGE FAIT le jour même** (accès HF gated OK, 3 états de voix bancés : réf 15 s int8 = RTF 0,43 et 6/6 au contrôle ASR ; réf 60 s moins stable ; ⚠️ le clonage coûte ×1,6 en RTF → Pi probablement > temps réel, à mesurer) ; **montage alternance David-réel/machine-clonée PRÊT** (`sorties/alternance-david-machine.wav`) | ✅ **VERDICT DAVID 26/08 : « oui, c'est bien ma voix »** (prouvé sur un texte INÉDIT de 99 s) → branche synthèse clonée VIABLE. **Mais : c'est sa voix NORMALE, pas la ventriloquie** — F0 clone 136,8 Hz vs référence 134,5 Hz, le clone est FIDÈLE, c'est la PRISE qui n'était pas en ventriloquie → **V3 bis : réenregistrer la référence en voix de personnage** (la ventriloquie est une technique vocale, donc elle appartient au corpus — pas un filtre à mettre en aval : §3 corrigé). Volume inégal = dynamique naturelle reproduite (clone 13,8 dB d'écart, l'humain 16,2) → remède AVAL `nivelle.py` (13,8 → 1,4 dB), à intégrer à la diffusion vision | **V3 bis (référence en ventriloquie, 60 s)**, puis **V0** banc octaver et V0b-Pi (avec état CLONÉ, pas Estelle) | V0/V0b en atelier ; **Kyutai sur ARM = inconnue qui décide de la forme du chantier** ; ne pas lancer l'enregistrement long avant V0b ; ⚠️ **le seuil d'écrêtage est ABSOLU : changer de TTS change la voix en silence** — relever le niveau d'entrée de l'effet à chaque bascule |
| Suivi de personne (roues) | validé sim 5/5, déployé, **SIM-ONLY** | — (attend ses verrous) | test scénique (1) PUIS protocole caméra (`direction_sign` inconnu) |
| Gaze V1 + arbitrage actionneurs | validé RÉEL 12/07 ; arbitrage déployé sur les 2 Pi | vérif visuelle : gaze ON pendant une séquence (la tête ne doit plus trembler) | — |
| Odométrie des roues (encodeurs) | **disque IMPRIMÉ et monté le 19/08** (plaqué contre la couronne, rondelles — vigilances fluage/faux-rond au README plans) ; support capteurs : **v4 MORTE AU MONTAGE 19/08** (le palier occupe le volume), **direction v5 = pince sur la vis de suspension du palier** (double écrou, hors chemin d'effort) ; capteurs LJ12A3 reçus | **berceau v5 DESSINÉ 20/08** (palier KP004, bloc E rempli) + **firmware Pico ÉCRIT et testé 20/08** (`firmware/pico_odometry/`, 35 tests) → valider `E4_VIS_DISQUE` (hyp. 25 mm, réglet) + vue de montage, **imprimer x2** ; côté élec : refondre la carte (en bas, USB, sans J6/D13) puis banc d'établi | E4 hypothèse ; `PAL_BOSS_R` (21) non coté ; **12 V dispo en bas ?** ; sens de comptage à MESURER (protocole caméra) ; restent `ROUE_D` (hyp. 250) et entraxe roues (C2) |
| Chaîne de sécurité matérielle (main-carrier) | schéma révisé 14/07 ; **contrat figé en tests sur la branche `chaine-securite`** | router la bande sécurité (122 chevelus) + note de sécurité docs/ | carte non fabriquée ; encombrement 195×150 à confirmer |
| Fond de tiroir | — | voir §Fond de tiroir | — |

## 0. Conversation — protocole physique chat_node V2

Le code est COMPLET et commité (nuit du 10 au 11/07 : ~15 commits sur les
3 dépôts, validé en sim — bras+yeux bougent sur l'animation « parle », vu par
David dans Gazebo). Côté vision : chat_node (`chat_enabled:=true`, défaut
false), pipeline VAD→whisper→OpenRouter→piper→mixette, didascalies/émotions →
topics face+animation. Côté robot : fix MODE (dadou_utils_ros 5aefdf1 — le
mode random servo était mort depuis sept. 2025), expression « parle »,
séquence didier/parle.json.

**À faire sur le vrai matériel** : rebuild image ARM vision (voix piper +
whisper préchargés), Pi 5 avec ALIM 27 W (crash constaté sur USB-C PC),
sentinelles robot/change + vision/CHANGE, dérouler une conversation complète
au casque, vérifier gestes/bouche/arrêts propres (caméra à l'appui). Vérifier
aussi le gate d'arbitrage en conversation réelle (voir chantier gaze).

## 1. Test scénique en conditions réelles

Roues AU SOL, télécommande physique en main (boutons, slider, gants), une
séquence de spectacle complète — **première fois que le mode cmd_vel roule au
sol**. Vérifier aussi le sens de rotation gauche/droite (le protocole roues
hors sol ne l'a validé qu'en marche avant symétrique).

C'est le verrou de : roues web au réel (chantier web), suivi de personne au
réel.

## Odométrie des roues

Plan : [`etude-odometrie.md`](etude-odometrie.md) (décidé 2026-07-14 — ne pas
re-trancher §3 à §6 ; inconnues §7).

**Le trou** : les roues n'ont AUCUN retour de rotation. Le moteur est un MY1016Z
**à balais** (la fiche matériel disait « brushless » — faux, corrigé le 14/07),
donc pas de capteurs Hall à dériver, et le SmartDrive40 n'expose aucune sortie
tachy. Conséquence : `/cmd_vel` est en **boucle ouverte** (des m/s qui sont du
PWM déguisé), et il n'y a pas de TF `odom` → `base_link`. C'est le verrou de
`ros2_control` ET de nav2. Ni le lidar ni la caméra ne le comblent.

**La solution retenue** : roue phonique lue par la FACE avec deux capteurs
inductifs `LJ12A3-4-Z/BX` (M12, NPN, 12 V) par roue → quadrature → PC817 → Pico
(PIO) → **USB** → nœud ROS.

⚠️ **Renversé le 20/08 (David)** : la carte va **en bas, près des roues**, et c'est
le câble **USB** qui remonte au Pi. Le §6 plaçait la carte côté Pi avec un lien
UART, pour ne pas faire porter la distance à un fil logique 3,3 V nu — juste, mais
l'USB est une paire différentielle blindée, bien plus robuste que ce fil, et on
raccourcit en prime les câbles capteurs. Le Nano (stock de David) a été écarté pour
UNE raison : les clones CH340 n'ont pas de numéro de série, donc pas de règle udev
stable. Conditions gravées : **bridage du câble USB à moins de 5 cm de la prise**,
**boîte imprimée fermée**, **les 4 PC817 restent**. Inconnue : 12 V dispo en bas ?

**Firmware ÉCRIT et testé le 20/08** : `firmware/pico_odometry/` (MicroPython).
Coupure de conception : `odom_protocol.py` (décodage quadrature + CRC + trames)
tourne à l'identique sur le Pico, dans le futur nœud ROS et dans **35 tests hôte** ;
`main.py` ne garde que le PIO. Écrire le décodeur en C aurait imposé de l'écrire
deux fois — le moyen canonique d'inverser un signe sans le voir.

**Fixation du disque — la COIFFE, confirmée le 17/08 au soir.** Une variante
« sandwich boulonné sur la couronne » a été explorée les 16 et 17/08 puis RANGÉE
(`../plans/odometrie/variante-sandwich-couronne/`, avec son NOTE.md) : le cercle des vis
mesuré à Ø 77 mettait la visserie trop près des cibles, on tombait à 8 cibles / 24,5 mm/front,
sous le seuil de 22 que l'étude §7 juge inasservissable. La coiffe donne 19,6 et elle est
déjà imprimée. **Le détour n'a pas été perdu** : il a produit 4 cotes MESURÉES qui renforcent
la coiffe — couronne 6 mm, chaîne 16 mm hors-tout (donc débord réel **5 mm**, contre 6
supposés « optimistes »), et surtout **obstacle carter à ~66 mm et non 63** (disque Ø 113
présenté : **≥ 10 mm d'air** relevés contre 6,5 au modèle). Les deux hypothèses les plus
inquiétantes du chantier étaient donc **pessimistes**.
⚠️ **Et une erreur trouvée au passage, qui vaut pour la coiffe aussi — la quadrature.** Toute
la doc prescrivait « capteur B réglé 7 mm plus bas que A » : FAUX, les capteurs étant
diamétralement opposés, ça donne un déphasage **rigoureusement nul** (les deux LED basculent
ensemble, plus de sens de rotation, et rien ne casse). Il faut les décaler **du même côté** de
l'axe, de `R·sin(pas/8)` chacun = **3,45 mm**. Corrigé dans `patte-capteur.scad`.

*(Le détail de la variante sandwich — pourquoi elle était séduisante, pourquoi elle
a échoué, et comment la réveiller — est dans son `NOTE.md`. Ne pas le recopier ici.)*

**16/08 — le disque Ø 155 CONTREDIT PAR LE RÉEL, redimensionné Ø 113.** Le premier jeu
imprimé (gabarit → jupe → disque, PETG) butait sur le **carter du réducteur** — jamais
mesuré — et la chaîne traverse son plan (photos de la collision :
`../plans/odometrie/photos/`). Cote relevée : axe → obstacle = **63 mm** (`OBSTACLE_R`).
Recalé le jour même : **10 cibles à R = 44, Ø 113 × 12, 19,6 mm/front** (M8/clé de 13
conservé : cible ≥ 3×Sn = 12 mm), garde-fou 5b désormais purement radial, et **empreinte
hexa des deux côtés** (tête indexée = cibles au même profil, serrage sans clé à tenir).
Le gabarit a rendu son verdict au passage : `JEU_HEX` 0.4 trop libre → **0.25**, à
revalider par le gabarit avant tout disque. Tout est régénéré, asserts verts.

**16/08 soir — fixation capteurs en v4 (montage de David, qui a retoqué mes v3.x
deux fois avec raison)** : **4 pattes identiques** (2/roue) vissées sous la caisse,
un capteur **de chaque côté du palier, à hauteur d'axe** — là il y a 30 mm de place,
donc **montage classique, un écrou M12 de chaque côté du voile** (les v3.x à 6 H
reposaient sur une erreur de signe : l'axe est 30 mm SOUS la caisse). On ne touche
plus aux boulons du palier, **la tôle pliée et son plan papier restent SANS OBJET**.
⚠️ La **quadrature est un réglage vertical** : capteur B 7 mm plus bas que A (un
quart de pas), calé aux LED — lumière verticale ±8 mm prévue pour. Détail : étude
§3 ter, rendus dans le dépôt plans (odometrie/rendus/).

**16/08 soir aussi — les capteurs LJ12A3 SONT ARRIVÉS** (photo : 2 écrous +
rondelle livrés avec) → **l'étape 1 (banc d'établi) est débloquée**. Et la
**couronne est déposée** : au réglet ~130-135 mm hors-tout, l'étude disait
« Ø 110 mesuré » → à re-mesurer posée à plat (gardes chaîne à recaler ; le disque
Ø 113 n'est pas concerné, son plafond est l'obstacle mesuré à 63 mm).

**Pièces dessinées** (`../plans/odometrie/`, dépôt plans) : roue phonique `disque-phonique.scad`
(coiffe, porte-cibles PETG + **10** têtes de vis M8 en acier ZINGUÉ — l'inductif ne voit que le
métal, et surtout PAS l'inox), pattes capteurs sous caisse (v4), et le banc d'établi. Géométrie
sous `assert()` : une cote fausse refuse de compiler.

~~Plan papier 1:1 du support tôle — fait le 15/08~~ — **SANS OBJET depuis la v3** (plus de
tôle). L'outillage reste dans le dépôt plans pour mémoire : `plan-decoupe-metal.py` savait
sortir une A4 1:1 auto-vérifiée, la méthode resservira si une pièce métal revient.

**Prochaine action — étape 1, sans robot, zéro risque** : commander les capteurs
(~15 €, cf. §9 — ⚠️ variante **NPN**, jamais PNP), imprimer le banc, passer la
réglette à la main devant les deux capteurs. Ça valide détection, entrefer, logique
inversée, quadrature et **le sens** (aller-retour), et tout le firmware Pico + le
nœud ROS se déboguent là.

**En parallèle, les mesures au pied à coulisse** (§7). Les six cotes bloquantes ont été
levées le 14/07 (dont la garde axe → châssis, 30 mm, qui plafonnait le rayon du disque).
Il reste **trois cotes de palier** — `D_BOULON`, `PAL_ENTRAXE`, `PAL_AXE_SEM` — qui ne
bloquent que la **tôle** : `D_BOULON` place les trous, et fausse de 3 mm elle rend la pièce
bonne à jeter. Le gabarit papier est fait pour ça : on le présente sur le robot avant de
toucher au métal.

Puis : étape 2 carte à trous au brochage définitif → étape 3 robot **roues hors
sol** + protocole caméra (on mesurera enfin la vraie vitesse pour un PWM donné,
première mesure objective du chemin roues) → étape 4 seulement, le PCB KiCad.

**Carte électronique FAITE et vérifiée** (14/07) :
`~/Nextcloud/dev/didier/pcb/kicad/wheel-odometry/` — schéma (ERC 0 violation,
netlist contrôlée), PCB placé, et **implantation stripboard vérifiée PAR
PROGRAMME**, net par net, contre la netlist. Lien vers le Pi en **UART**
(J6 : 5V/TX/RX/GND), pas USB — le micro-USB est le point faible d'une machine
qui part en tournée.

⚠️ **L'I²C est INTERDIT sur ce chantier.** `wheels_node.stop()` écrit le PWM par
le bus I²C : un esclave qui fige le bus empêcherait le robot de freiner (le
PCA9685 garderait sa dernière consigne = emballement). Raisonnement complet dans
l'étude — ne pas re-trancher.

**Verrous** : (a) les 5 cotes du §7, dont la **bloquante** — la garde axe →
châssis, qui plafonne le rayon du disque donc la résolution ; (b) **quel UART
côté Pi** : le primaire (GPIO14/15) est pris par la console et le Bluetooth, et
les GPIO libres sur la carte principale restent à vérifier.

**Aval** : `ros2_control` / `diff_drive_controller`, EKF (encodeurs + IMU pour
le yaw), nav2. Le BNO055 existe déjà dans le code (`robot/move/bno_055_extended.py`)
mais n'est appelé nulle part en prod — vérifier s'il est encore sur le robot.

## Chaîne de sécurité matérielle (carte main-carrier)

**Le trou (découvert 14/07)** : l'arrêt d'urgence de Didier est 100 % logiciel.
`wheels_node.stop()` écrit le PWM **par le bus I²C** — si le bus se fige ou si
le node meurt, le PCA9685 garde sa dernière consigne et les roues continuent,
pendant que le deadman 400 ms croit avoir freiné. Le protocole caméra du 04/07
a validé la mort de la chaîne *amont*, jamais celle de `wheels_node` lui-même.

**La parade (schéma main-carrier révisé 14/07, commit KiCad 4484d54)** :
watchdog matériel 74HC123 (250 ms, réarmé par un battement GPIO26 émis
seulement APRÈS chaque écriture I²C réussie) → ET par diodes avec la boucle
coup-de-poing → bascule D 74HC74 à `/CLR` dominant (maintenir ARM ne réarme
pas) → OE du PCA9685 roues. Coup-de-poing = catégorie 0 (relais 40 A,
purement électromécanique). Les deux PCA9685 sont séparés (roues 0x40,
servos 0x41 à venir) pour que couper les roues ne fige plus le visage.

**Contrat figé en tests — branche `chaine-securite`** (la carte n'existe pas
encore ; `main` reste le reflet du robot réel) : modèle exécutable de la carte
(`robot/tests/unit/safety_chain_model.py`) branché sur le **vrai** code
`Wheels`, 11 tests (`test_safety_chain.py`) couvrant mort du node, bus figé,
`/CLR` dominant, coup-de-poing, et LE piège du réarmement : sans remise à zéro
des registres, ARM rejoue l'ancien PWM. Les helpers `drive()`/`try_stop()` du
fichier de tests SONT la spec du futur node. Merger la branche quand la carte
sera fabriquée et le node écrit.

**Verrous** : bande sécurité du PCB placée mais **pas routée** (122 chevelus,
volontaire) ; encombrement 195×150 mm à confirmer dans le coffret avant
Gerbers ; le node (battement + `/e_stop` depuis ESTOP_SENSE GPIO23) n'existe
pas — volontaire aussi, les tests d'abord.

## Interface web / télé-présence

Plan : [`etude-interface-web.md`](etude-interface-web.md) (décidé 2026-07-11 —
ne pas re-trancher, inconnues §9).

FAIT : **W0** vérifiée en sim le 11/07 (package `robot_web` autonome — node
rclpy+aiohttp, whitelist sans roues/e_stop, session exclusive + heartbeat, UI
vanilla — 511 tests, protocole WS validé de bout en bout, `WEB=true` port
8765 ; 8088 = Superset sur le PC de dev). **Console + W3-sim** le même jour :
console de régie (vidéo + pad + recherche), caméra gz → MJPEG `/video`,
pilotage pad/manette → `cmd_vel_web` (twist_mux prio 50, plafond dur 0,5 m/s
backend, zéro unique à l'arrêt — vérifié e2e jusqu'à `/cmd_vel`) ;
`WEB_DRIVE=true` requis (défaut false) + chaîne roues à la main
(docs/operations.md). **Bringup robot câblé** (web_bridge dans
robot_app.launch.py, contenus/supervision seulement — drive non passé donc
false) ; image ARM rebuildée (python3-aiohttp + python3-pil). **Console
enrichie le 12/07 (déployé + vérifié)** : alias mDNS `didier.local` (service
`avahi-alias-didier`, source `conf/systemd/`, install docs/operations.md —
`/etc/avahi/hosts` ne publie PAS sur le réseau) + toggle **Parole IA** (topic
`chat` en whitelist technique, ON/OFF → chat_node du Pi vision, même contrat
que `gaze`).

**Suite : W1** (source e_stop + coup-de-poing sans fil). Le passage des roues
web au ROBOT RÉEL reste conditionné au test scénique au sol (chantier 1) et à
un protocole caméra dédié.

## Télédiagnostic par agent IA

Plan : [`etude-telediagnostic.md`](etude-telediagnostic.md) (**décidé, grillé
le 2026-07-12** — ne pas re-trancher, décisions §8 : hybride embarqué host Pi
+ PC atelier, Opus sur abonnement, START télécommande → topic `incident`,
boîte noire segments SD 30 j sans caméra, remédiations autonomes encadrées).

FAIT : **étape 1 « trousse d'atelier »** le 12/07 —
`conf/scripts/collect-incident.sh` (host du Pi, best-effort, testé de bout en
bout contre la sim ; piège corrigé : `ros2 node list` vide au premier appel du
daemon → retente), skill `/diag` (`.claude/skills/diag/SKILL.md`), journal
[`incidents/`](incidents/README.md) (post-mortem obligatoire). Part avec le
rsync habituel, rien à déployer. **Utilisable dès maintenant** : panne →
`ssh r '~/ros2_ws/src/*/conf/scripts/collect-incident.sh'` → session Claude
+ `/diag`.

**Suite : étape 2 « boîte noire + bouton »** (§9 du plan) : enregistreur
rosbag par segments SD 60 s + purge 30 j dans le bringup, topic `incident`,
bouton START télécommande (libre — GPIO D21 + manette USB ; côté
dadou_control_ros : l'ajouter à `PUBLISHER_LIST`) + boutons logiciels,
marqueur `INCIDENT` dans robot.log, endpoints `/api/logs` + `/health` sur le
pont web, topic santé publié par system_node. Validation en sim d'abord.
**Préalables de l'étape 3 (agent embarqué)** : RAM du Pi 4
(`ssh r 'cat /proc/meminfo'` — non documentée nulle part), charge d'une
investigation vs tick 20 Hz, santé/espace SD, 4G partagé en salle.

## Conversation en déambulation (intention de communiquer + contenu)

Plan : [`etude-declenchement-conversation.md`](etude-declenchement-conversation.md)
(**DÉCIDÉ, grillé le 2026-07-12** — ne pas re-trancher, décisions §5, points
ouverts §8). Périmètre élargi au grill : déclenchement + contenu + robustesse
rue.

Décisions clés : opérateur à vue, robot peut rouler → **regard généreux en
roulant, micro seulement à l'arrêt** (gate `/cmd_vel`) ; ENGAGED = personne
en zone sociale ET (arrêt ≥ 3 s OU parole détectée) — le bruit sans personne
ne déclenche plus jamais ; sessions (clôture silence 12 s / perte 3 s,
cooldown 45 s) ; **réactif d'abord** (invitation par le corps : regard +
expressions + gimmick sonore + animation « invite », rejet encaissé en jeu) ;
persona à créer de zéro (atelier d'écriture, garde-fous = confiance au modèle
pour l'instant, répliques courtes et relanceuses) ; micro U20 et CPU Pi 5
mesurés avant tout achat (soupape whisper API) ; latence < 2 s au premier
son ; corpus complet type tournage (affichage + bouton garder/effacer,
effacement par défaut). Abordage mobile, proactif verbal et mémoire des gens
en D6, derrière les verrous roues.

**D0 outillage FAIT le 13/07** (dadou_vision_ros 53c6d13, 162 tests) : topic
`chat_state` latché (listening/thinking/speaking/off), rejeu VAD de prod sur
wav (`vad_replay`), scripts `enregistre-rue.sh` / `mesure-cpu-conversation.sh`
/ `calibre-distance.sh`. **Atelier persona FAIT le 13/07** (partie écriture +
commutation) : 3 personnalités commutables à tester — « bougon » (défaut) /
« naif » / « vantard » — socle + textes dans `vision/ai/personas.py` (repo
public, tranché §8), commutation à chaud topic `persona` (nouvelle session de
conversation à chaque bascule), sélecteur sur la console web.

**MICRO CHANGÉ le 26/08** : le ReSpeaker XVF3800 est reçu et **testé au banc
sur le Pi 5** — driverless, 16 kHz natif, 21 dB de SNR à 3 m sur le robot au
repos, `faster-whisper base` transcrit à RTF 0,39, **et la DoA fonctionne**
(`xvf_host` installé dans `~/xvf_host/` sur le Pi vision, build `rpi_64bit`).
Détail et pièges dans `hardware/overview.md` §Microphone.

Ce que ça change pour D0 :
- **FAIT le 26/08** : l'alias `casque_mic` d'`/etc/asound.conf` pointe sur
  `CARD=Array` (nom d'alias conservé = contrat avec `vision_config.py`, donc
  aucun code touché et `dadou_vision_ros` reste gelé), vérifié DEPUIS le
  conteneur. Alias `webcam_mic` ajouté pour garder l'ancienne captation
  disponible en comparaison A/B. Mode d'emploi et piège du bind-mount :
  `operations.md` ;
- toute mesure D0 doit **nommer le modèle Whisper utilisé** — sur la prise à
  3 m, `base` était le maillon faible, pas le micro ;
- la DoA ouvre le recoupement micro × caméra pour l'attribution du locuteur :
  prendre la valeur 1 (faisceau focalisé), **jamais la valeur 2 qui est une
  constante à 90°**, et amortir la valeur 3 (bruitée). L'azimut absolu n'aura
  de sens qu'une fois la carte fixée (offset de montage à relever).

**Support 3D — étude faite le 27/08, dessin EN ATTENTE de 8 cotes.**
`plans/supports/support-respeaker-xvf3800/README.md` (hors dépôt, Nextcloud).
Trois pièces, berceau/platine séparés. Deux résultats à ne pas redécouvrir :
le **silentbloc caoutchouc amplifierait** le bruit des servos (f0 = 159 Hz sur
30 g → +4,7 dB à 200 Hz) — mousse souple + lest, f0 = 33 Hz ; et le **câble USB
tendu court-circuite le découplage** en silence.

**Emplacement arrêté : à plat sous l'arceau d'acier en T qui enjambe la tête.**
Une première idée (verticale sur le torse) a été écartée, et le pourquoi sert :
une antenne **plane** ne résout une direction que **dans son plan** — à la
verticale, l'azimut mêle gauche/droite et hauteur, il est **indéterminé pile en
face** et ambigu avant/arrière. Pas « moins précis » : faux tout en ayant l'air
juste, comme la `value 2` constante à 90°. L'arceau lève les deux conditions
d'un coup (antenne **horizontale**, repère **fixe** — c'est la tête qui pivote
dessous) : **la DoA est préservée**, et l'anneau LED redevient un signal honnête.
En prime : rien sous la carte (air libre 360°, les ports bottom-firing sont
servis sans rien faire), câble qui ne traverse aucune articulation, point le plus
éloigné des moteurs de roues. **Risque créé** : les servos des yeux sont sur la
même barre d'acier — brider au sommet, à mi-chemin des deux, et trancher par la
mesure.

Montage **SUR le dessus de la traverse** : l'axe de la tête occupe le dessous, et
le dessus ne coûte rien en hauteur (les yeux dépassent déjà de ~15 cm, l'empilage
fait ~40 mm). Capuchon anti-pluie obligatoire, transformé en **lanterne** (fente
360°). À contrôler : que le cercle des ports acoustiques soit plus large que la
semelle du T, sinon la barre bouche un micro.

**Prochaine action : David relève les 8 cotes de la carte + le profil du T +
le dépassement des yeux au-dessus de la traverse, avec photos quadrillées.**

⚠️ Trouvé le 26/08 : **la webcam du Pi 5 était débranchée** sans que rien ne
le signale — gaze, suivi de personne ET micro de conversation à terre en même
temps. Rebranchée le jour même. À retenir pour la boîte noire du
télédiagnostic : un contrôle « caméras/micros présents » coûte zéro.

**ÉCHO MESURÉ le 26/08, ampli branché — le half-duplex devient LE verrou.**
Didier a joué sa propre voix dans sa sono pendant que le micro écoutait, à
volume MODÉRÉ (donc tous les chiffres sont des planchers) : silence −60,0 dBFS,
Didier qui parle **−10,4 dBFS**, soit +49,5 dB — et **22 dB AU-DESSUS d'un
humain à 3 m** (−32,4). L'entrée micro **écrête** (crête −0,0 dBFS, 65
échantillons saturés), ce qui achève l'espoir d'un AEC utile : un AEC exige un
chemin linéaire. Et **Whisper a transcrit Didier lui-même** (7 segments) : le
mode de panne du 11/07 n'est plus une hypothèse, il est reproductible à la
demande. Détail : `hardware/overview.md` §Echo. **Prochaine action du chantier
0 : implémenter le gate half-duplex** (aucun matériel requis, que du code) —
et il doit écouter « une source audio est vivante », pas « piper joue » (le
récepteur HF de l'interprète sort par le même châssis).

**Suite : la campagne D0** (robot allumé : mesure CPU en conversation,
enregistrements rue à rejouer, calibration distance) et la **validation des
textes par David** ;
reste D3 : bouton télécommande, multi-langues, chrono latence. Verrou de
D1+ : protocole physique chat_node V2 (chantier 0). Réussite finale = grille
chiffrée du test rue D5 (§7 du plan).

## Voix de Didier (continuité ventriloquie ↔ synthèse)

Plan : [`etude-voix-didier.md`](etude-voix-didier.md) (ouvert 2026-08-26).

Problème : l'IA arrive dans les réponses, mais la voix de la ventriloquie et
celle de piper n'ont rien à voir — le personnage tombe à chaque alternance.

Constat qui structure tout (câblage relevé 26/08) : **« la voix de Didier » =
la voix de David + l'octaver**, et le **Pi ne passe pas par l'octaver** (il
entre en direct dans la mixette). D'où le principe directeur (§3, ne pas
re-trancher) : **cloner avant les filtres, unifier après** — la continuité
vient du dernier étage commun, pas du clonage.

**Suite = deux lots parallèles et indépendants :**

- **V0 — banc d'écoute**, en atelier sans modification permanente (sortie Pi →
  octaver via un pad, 6 phrases, écoute en aveugle, **test en alternance** : la
  rupture ne s'entend qu'en juxtaposition). C'est V0 qui débloque
  l'**arbitrage artistique du §5, volontairement suspendu** : cloner la voix de
  David (A) ou pousser la robotisation jusqu'à rendre la source indifférente (B).
- **V0b — Kyutai Pocket TTS tourne-t-il sur le Pi 5 ?** L'inconnue la plus
  rentable du chantier (état de l'art du 26/08) : MIT, français natif, clonage
  **zero-shot depuis ~10 s** — mais aucune mesure sur ARM n'existe. S'il passe,
  il supprime le corpus d'une heure, le GPU loué et le fine-tune. Mesurer dans
  l'ordre : tourne sur ARM ? RTF sur Pi chargé ? tenue sur un énoncé de 30 s ?

Ensuite V1 câblage permanent (aiguillage A/B sur le relais existant), V2
accordage (voix piper la plus proche + pré-transposition F0), V3 enregistrement
**au dimensionnement conditionnel à V0b**, V4 fine-tune piper (filet de
sécurité, MIT, donne le timbre pas le jeu).

Deux garde-fous de séquencement :
- **Ne rien engager en clonage avant V0** — l'octaver écrase peut-être assez
  pour que l'écart résiduel ne s'entende pas.
- **Ne pas faire enregistrer 1-3 h à David avant V0b** — 10 s pourraient
  suffire. Seul le palier minimal (quelques minutes **en personnage**) est utile
  dans tous les cas.

Deux points structurants consignés dans l'étude, à ne pas perdre : l'octaver
unifie le **timbre mais pas la prosodie** (donc la garantie s'amincit sur les
énoncés longs, exactement là où on en a besoin), et **le corpus est le plafond
du clone** — enregistrer en lisant proprement donne un clone plat à vie ; il
faut jouer, pas lire.

## Suivi de personne aux roues

CODE COMPLET, VALIDÉ EN SIM 5/5 (11/07 soir) : chaîne `/vision/person_box`
(Pi vision : azimut + HAUTEUR de silhouette = proxy de distance monoculaire,
cf. dadou_vision_ros) → `person_follower` (logique pure
`robot/move/follow_control.py` testée : deadzones, plafonds durs ABS 0,5/1,0
bornant même les paramètres, slew, zéro franc sur perte de cible < 600 ms et
sur OFF, marche arrière interdite par défaut) → `cmd_vel_follow` → twist_mux
**prio 20** (remote 100 > web 50 > follow 20 > anim 10, contrat gelé
re-testé). Toggle topic `follow` "on"/"off", **OFF par défaut**, lancé À LA
MAIN, PAS dans le bringup. Validé sim : T1 désactivé=zéro mouvement,
T2 avance+rotation vers la personne (odom confirme le déplacement gz), T3 la
télécommande écrase et le suivi reprend, T4 perte=zéro franc puis silence,
T5 OFF=zéro unique. Code DÉPLOYÉ sur les Pi au déploiement complet du 12/07
(rsync Ansible + sentinelles).

**SIM-ONLY** : usage réel conditionné au test scénique au sol (chantier 1)
PUIS protocole caméra roues hors sol (`direction_sign` azimut→rotation
inconnu, comme l'était celui du gaze).

## Gaze V1 (cou + yeux) + arbitrage actionneurs

**Gaze : PROTOCOLE CAMÉRA FAIT ET VALIDÉ le 12/07** sur le vrai robot, David
en scène. Résultats gravés en défauts du node : cou `direction_sign=+1`
(boucle fermée AUTO-VALIDANTE : la caméra est sur la tête, l'azimut converge
vers 0 — un mauvais signe aurait divergé en butée), amorti `ema_alpha=0.15` /
`slew_max=1.5` (les valeurs initiales 0.4/3.0 oscillaient : retard de phase
EMA×2 + slew + rampe servo), YEUX ajoutés (2e instance de GazeControl,
gain 49 = plein débattement 1-99 comme les séquences, `eye_direction_sign=-1`
— montage MIROIR du cou, validé visuellement). Toujours lancé À LA MAIN (pas
dans robot_bringup), toggle topic `gaze` "on"/"off".

**Arbitrage amont FAIT le 12/07** (lots A+B de
[`etude-arbitrage-actionneurs.md`](etude-arbitrage-actionneurs.md), contrat +
validation §8) : `animations_node` publie l'état latché `animation_state`
(nom ou "", time=remaining_ms, TRANSIENT_LOCAL des DEUX côtés — un abonné
volatile raterait le latch), le gaze et le chat (Pi vision, module pur
`vision/ai/arbitration.py`) se TAISENT quand une séquence a la main, avec
PÉREMPTION façon deadman (remaining+2 s) si animations_node meurt en pleine
séquence. Chat : rattrapage idle() après abandon STT (fini le visage coincé
sur « reflechit ») + stop ciblé (fini le stop GLOBAL qui tuait la séquence en
cours). Validé en sim 5/5 (latch, silence pendant séquence — contre-preuve
sans piste neck —, reprise, redémarrage en cours de séquence, péremption sur
kill). **DÉPLOYÉ ET VÉRIFIÉ sur les deux Pi le 12/07** : contrat joué en réel
("" latché au repos → "parle" time=4999 pendant une séquence de 5 s → "" au
retour), module arbitration + câblage péremption confirmés dans l'install du
Pi vision. Arbitrage aval par source différé (étude §5.3).

**Reste** : vérif VISUELLE comportementale à la prochaine session robot —
gaze ON pendant une séquence (la tête ne doit plus trembler), et le gate chat
en conversation réelle (avec le chantier 0).

## Fond de tiroir (pas urgents, pas oubliés)

- Calibrer `max_wheel_speed` réel (m/s à consigne 1.0) — mesurable à la
  caméra, distance/temps. Débloque le plafond de vitesse distant (web §2.3).
- Action ROS 2 `PlayAnimation` (les pistes roues des séquences passeront par
  cmd_vel_anim).
- Source unique des séquences JSON (côté robot, la télécommande interroge par
  service).
- Affiner l'URDF depuis les plans FreeCAD (~/Nextcloud/dev/didier/plans).
- Quirk latent à vérifier caméra un jour : en legacy, une paire [0,0] de
  séquence passe par update_cmd(0,0) → PWM au plancher MIN_PWM=5000 (rampage
  lent possible).
- Batterie : aucun capteur câblé — parqué vers le chantier élec (cartes PCB),
  décision télédiagnostic §8.
- ~~Micro réseau~~ — **SORTI DU FOND DE TIROIR** : ReSpeaker XVF3800 acheté
  (66,39 €), **REÇU et testé au banc sur le Pi 5 le 26/08** (driverless UAC 2.0,
  16 kHz natif, 21 dB de SNR à 3 m, Whisper transcrit). Mesures et restes à
  faire : `hardware/overview.md` §Microphone. **DoA testée le 26/08 aussi**
  (`xvf_host`, build `rpi_64bit`). Restent : l'ÉCHO entier (half-duplex à
  implémenter, c'est ce qui a fait couper chat_node le 11/07) et le montage
  (découplage, ports acoustiques VERS LE BAS, offset d'azimut) — un chantier
  CAO à part entière.
- Détection d'obstacle (lidar 2D) — RPLIDAR C1 repéré (68,99 €) et contraintes de
  conception consignées dans `hardware/overview.md` §Distance & obstacle sensing
  (2026-07-13, RIEN acheté). Le trou n'est PAS la distance à la personne (déjà
  résolue par la hauteur de silhouette) mais l'obstacle qui n'est pas la personne.
  Points clés : pas besoin de 360° (arc AVANT suffit, secteur occulté à masquer),
  plan de scan BAS, barrière d'obstacle **appliquée EN LIGNE** sur le Pi 4 dans la
  chaîne cmd_vel, CPU négligeable hors nav2. Pas avant la priorité 1 (test au sol) :
  c'est lui qui dira si l'opérateur au deadman suffit.
  ⚠️ **Argument corrigé le 27/08** : cette ligne disait « jamais sur le Pi vision —
  une sécurité qui dépend du wifi n'en est pas une ». Prémisse FAUSSE : une fois
  correctement câblé, **les deux Pi sont en RJ45 sur le routeur embarqué, seule la
  télécommande est en wifi**. Ce qui compte n'est pas le média mais **la manière de
  tomber** : un garde-fou qui est un FILTRE en ligne est fail-safe (on le tue, la
  chaîne casse, le deadman met les zéros en 400 ms) ; un garde-fou qui se contente
  de PUBLIER un veto ne l'est pas (on le tue, aucun veto n'arrive jamais, et le
  robot cesse de voir les obstacles **en silence**). Règle qui survit : **exiger un
  battement de cœur positif** (« vivant et voie libre »), jamais déduire la
  sécurité de l'absence de veto.
- Caméra CSI (nappe) à la place de la webcam USB — module IMX219 130° repéré et
  critères de tri consignés dans `hardware/overview.md` §Vision & camera
  (2026-07-13, RIEN acheté). Gain réel : la webcam plafonne à 16,7 fps alors que
  MediaPipe ne prend que 24 % de CPU. Trois coûts à ne pas oublier : la webcam
  EST le micro de chat_node V2 (→ micro USB à acheter), la nappe FPC traverserait
  le cou mobile (fatigue mécanique), et `cv2.VideoCapture` ne voit pas une CSI
  sur Pi 5 → libcamera/Picamera2 dans le conteneur vision. Ne pas lancer avant
  les priorités 0 et 1.
