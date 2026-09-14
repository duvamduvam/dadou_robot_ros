# Étude — petite télécommande USB à base de RP2040

*Ouverte le 2026-09-14, à partir de quatre photos d'atelier d'un module joystick.
Rien n'est fabriqué. Les décisions marquées **OUVERT** attendent David.*

Documents liés : [`chantiers.md`](chantiers.md) · [`etude-chemin-commande-roues.md`](etude-chemin-commande-roues.md) ·
[`etude-suivi-personne.md`](etude-suivi-personne.md) · [`hardware/inventaire-stock.md`](hardware/inventaire-stock.md)

---

## 1. Ce que c'est, et ce que ce n'est pas

**Le besoin, mot pour mot** : « j'aimerais faire une petite télécommande USB avec une
RP2040 ». Destination confirmée : **la télécommande Pi 4 existante ET la simulation**.

**Ce n'est pas** un remplacement de la télécommande de scène (`dadou_control_ros`, Pi 4
portable, 10 périphériques USB, GUI, liaison Wi-Fi). C'est un **petit boîtier filaire**,
qui se branche par un câble USB soit sur cette télécommande, soit sur le PC d'atelier.

**Pourquoi ce chantier peut avancer maintenant.** Depuis le 2026-09-12, le Pi 4 du robot a
fumé et **le robot est en pièces** : les chantiers 0 et 1 sont gelés. Celui-ci ne touche
**aucun matériel du robot** — il se développe et se vérifie entièrement au banc (PC +
simulation Gazebo). C'est du travail utile pendant le gel, et il prépare le test scénique
au sol (priorité 1) au lieu de l'attendre.

---

## 2. Le matériel constaté sur les photos

Photos : [`hardware/photos/2026-09-14-module-joystick/`](hardware/photos/2026-09-14-module-joystick/)
(4 images, copiées du Xiaomi le 14/09 ; c'est le seul relevé dont on dispose — rien n'a
été mesuré à l'établi).

| Fait | Comment il est établi | Confiance |
|---|---|---|
| Module **`HW-504`** (famille « KY-023 ») | sérigraphie lue sur le flanc et au dos (`221117`, `221123`) | **H** |
| Brochage `GND · +5V · VRx · VRy · SW`, barrette 5 broches au pas 2,54 | sérigraphie lue en gros plan (`221113`) | **H** |
| 2 potentiomètres montés à 90° + poussoir sur l'appui du manche | forme, sans ambiguïté | **H** |
| **L'emplacement `R5` est VIDE** au dos | vu en gros plan (`221123`) | **H** |
| Valeur des potentiomètres (10 kΩ ?) | **non lue** — aucune sérigraphie visible | ⛔ |
| Second objet noir en bord de cadre (potentiomètre rotatif de panneau ?) | forme seule, hors sujet depuis §4.6 | **B** |

### 2.1 Deux pièges qui se paient cher, à traiter dès le premier câblage

**⚠️ Piège 1 — la broche `+5V` doit être alimentée en 3,3 V, jamais en 5 V.**
Le module n'est qu'un pont diviseur : le rail alimente le haut des potentiomètres, donc
`VRx`/`VRy` sortent au maximum la tension d'alimentation. En 5 V, ces sorties attaquent les
entrées analogiques du RP2040, dont le maximum absolu est 3,63 V — destruction de la carte,
éventuellement silencieuse et différée. En 3,3 V le module fonctionne exactement pareil, on
perd seulement de la dynamique qu'on n'utilisait pas. **Cette ligne est la seule erreur de ce
montage qui coûte une carte.**

**⚠️ Piège 2 — `SW` est flottant sur cet exemplaire.** `R5`, la résistance de tirage du
poussoir, n'est pas peuplée : sans tirage, la broche lit du bruit, et le bouton paraîtra
« parfois appuyé ». Remède gratuit : **pull-up interne du RP2040** (`Pull.UP`), bouton actif
à l'état bas. Aucune résistance à souder. À écrire dans le firmware **et** dans le test.

---

## 3. Ce que l'existant impose (relevé dans les dépôts, pas supposé)

La télécommande Pi 4 sait déjà lire dix périphériques USB. Leur convention n'est pas
négociable si on veut s'y brancher sans rien casser :

| Fait | Où c'est écrit |
|---|---|
| Les périphériques sont des **séries USB CDC**, identifiés par un chemin udev stable `SERIAL_ID` | `dadou_control_ros/controller/control_config.py:169-245` |
| Il existe **déjà** un device `JOYSTICK` sur un **Waveshare RP2040-Zero**, et un device `sliders` sur un second | idem, lignes 232-245 |
| Trame du `JOYSTICK` : **4 caractères**, deux entiers de 2 chiffres, mappés `10..99 → -100..+100` | `controller/input/serial_inputs.py:64` (`send_gamepad`) |
| Un chemin **totalement distinct** existe pour les manettes du commerce : `USBGamepad` (pygame) | `controller/input/usb_gamepad.py` |
| Côté robot, `twist_mux` arbitre `cmd_vel_remote` (100) > `cmd_vel_web` (50) > `cmd_vel_anim` (10), avec un verrou `e_stop` latché | `conf/ros2_dependencies/robot_drive` |
| Le repo héberge déjà du firmware RP2040, avec une convention de découpage explicite | `firmware/pico_odometry/README.md` |

**Deux observations qui orientent la conception.**

1. **Le protocole existant est trop pauvre pour ce boîtier.** 4 caractères, ~90 pas de
   résolution par axe, **aucun bouton, aucune somme de contrôle, aucun compteur de séquence**.
   On ne peut pas y faire entrer un homme-mort et quatre boutons. Il faudra un nouveau type de
   périphérique — voir §4.5.
2. **Incohérence relevée au passage, non corrigée ici** : la config déclare `msg_size: 6`
   pour le `JOYSTICK` alors que `send_gamepad` exige `len(msg) == 4` et journalise une erreur
   sinon. Ça marche sans doute parce que le séparateur est retiré en amont, mais les deux
   chiffres se contredisent. **À instruire dans `dadou_control_ros`, pas ici.**

---

## 4. Décisions

### 4.1 Carte : **Seeed XIAO RP2040** — DÉCIDÉ (révisable au §7)

Faits sourcés le 2026-09-14 sur les wikis officiels (voir §8 pour les réserves) :

| | XIAO RP2040 | Waveshare RP2040-One | RP2040-Zero |
|---|---|---|---|
| USB | **Type-C** | **USB-A mâle intégré** (façon clé USB) | Type-C |
| Broches exposées | **11** (D0-D10) | 20 en bord de carte | 20 en bord de carte |
| ADC utilisateur | **4** (A0-A3 = GP26-29) | 4 (broches non précisées par le wiki) | 4 |
| Dimensions | **21 × 17,8 mm** | non publiées en texte | non publiées en texte |
| En stock ? | **oui** (+ 2 cartes Seeed non identifiées) | oui, 1 | **non** |

**Pourquoi le XIAO.** (a) L'USB-C accepte un câble détachable : un objet tenu en main tire
sur son câble, et le connecteur USB-A mâle du RP2040-One obligerait à faire sortir la carte
elle-même du boîtier, en porte-à-faux — le wiki Waveshare admet d'ailleurs que « la fiche USB
tient lâche » et livre un autocollant pour la caler. Mauvais pour un objet de scène.
(b) 4 ADC là où le Raspberry Pi Pico n'en offre que 3 (sur Pico, GP29 mesure VSYS) : il reste
**deux voies analogiques libres** après le joystick. (c) 21 × 17,8 mm. (d) Il est en stock,
donc on soude ce soir.

**La contrainte à accepter** : **11 broches, pas une de plus.** Le décompte ci-dessous
montre que ça passe, mais sans marge :

| Fonction | Broche | Reste |
|---|---|---|
| `VRx` | A0 / GP26 | |
| `VRy` | A1 / GP27 | |
| Homme-mort | D6 / GP0 | |
| 4 boutons | D7, D8, D9, D10 | |
| OLED I²C (SDA/SCL) | D4 / GP6, D5 / GP7 | |
| **Libres** | **A2, A3** (GP28, GP29) | 2 analogiques |

Le `SW` du joystick **n'a plus de broche numérique** : il faut le câbler sur A2 ou A3 (une
entrée analogique se lit très bien en numérique). C'est possible, mais ça consomme la
dernière réserve d'extension. **Si David veut le `SW` ET une extension future, c'est le
RP2040-One (20 broches) qu'il faut prendre**, en acceptant sa mécanique USB.

### 4.2 Deux interfaces USB dans un seul firmware — DÉCIDÉ, à valider sur matériel

C'est la décision structurante, et elle vient directement du « télécommande **et**
simulation ». Les deux destinations ne parlent pas la même langue :

- la **télécommande Pi 4** attend une **série USB CDC** avec une trame maison ;
- la **simulation** n'a besoin de rien de spécifique si le boîtier se présente comme une
  **manette de jeu HID standard** : `ros2 run joy joy_node` la lit, `teleop_twist_joy` la
  convertit en `/cmd_vel_remote`. **Zéro ligne de code à écrire côté ROS**, et le paramètre
  `enable_button` de `teleop_twist_joy` est *exactement* un homme-mort.

Écrire un nœud ROS maison pour lire la série en simulation serait du code à maintenir pour
refaire ce que `joy_node` fait déjà. **Donc : les deux à la fois.** CircuitPython l'autorise
en principe — `usb_cdc.enable(console=…, data=True)` et `usb_hid.enable(…)` dans `boot.py`,
avec la bibliothèque `hid_gamepad.Gamepad` d'Adafruit qui fournit un descripteur tout fait.

> ⚠️ **Ceci n'est pas vérifié sur matériel.** La recherche du 14/09 n'a trouvé **aucun
> exemple officiel Adafruit combinant HID et CDC-data**, et la documentation prévient qu'on
> peut « manquer d'endpoints USB », sans jamais chiffrer combien le RP2040 en offre. Si les
> endpoints manquent, CircuitPython passe en **mode sans échec** après `boot.py`.
> **C'est pour ça que le lot T0 (§6) ne fait que ça, et passe avant tout le reste.**
> Repli si ça ne passe pas : deux firmwares, un interrupteur de mode au démarrage (bouton
> tenu au branchement), ou on renonce au HID et on écrit un petit nœud `joy` maison.

### 4.3 Homme-mort : bouton séparé sous l'index — DÉCIDÉ (choix de David)

Règle non négociable du projet : « toute fonctionnalité mouvement DOIT traiter son cas
d'arrêt ». Le `SW` du module a été écarté : c'est un clic sec obtenu en **enfonçant le
manche**, pénible à tenir plusieurs minutes, et l'appui parasite l'axe qu'on tient.
Un poussoir dédié (le stock en contient 40-60 en 6×6 et 12×12) est tenu sans y penser.

**Ce que ça apporte au-delà du confort.** Aujourd'hui, l'arrêt d'urgence effectif du robot
est le deadman 400 ms **en aval** : il se déclenche sur *absence de trame*, c'est-à-dire sur
une **panne**. Aucun geste volontaire ne coupe les roues, et CLAUDE.md note que le verrou
`e_stop` de `twist_mux` est déclaré mais que **personne ne le publie**. Un bouton tenu, plus
un bouton d'arrêt franc (§4.4), donneraient enfin au projet ces deux sources manquantes.

**Ce que ça n'apporte pas** : ce boîtier reste **filaire**. Il ne remplace ni le
coup-de-poing sans fil du chantier web (W1), ni la coupure générale. Et il ne répare pas le
danger actif des deux boutons du dos (« stop » = `shutdown`, donc emballement).

### 4.4 Les 4 boutons — **OUVERT**

David a répondu par une question : « sélection menu OLED ? ». Les deux schémas possibles :

| | **A — 4 actions directes** (recommandé) | **B — 4 touches de menu** |
|---|---|---|
| Rôle des boutons | e-stop franc, cran de vitesse, `follow` on/off, animation | haut, bas, valider, retour |
| Navigation du menu | **au joystick** (haut/bas + `SW` pour valider) | aux boutons |
| Actions scéniques | les 4 principales sont à un geste | toutes au menu, ≥ 2 gestes |
| Extension | limitée à 4 | illimitée (le menu grandit) |

**Je recommande A**, pour une raison qui n'est pas ergonomique : **un menu fabrique des
modes**, et le même bouton ne fait plus la même chose selon l'écran affiché. L'étude du robot
suiveur du 14/09 vient d'identifier le mode implicite comme *le* mode dangereux du projet.
Le joystick, lui, sait déjà naviguer un menu — c'est un organe à quatre directions avec un
bouton de validation intégré. Le prendre pour le menu **libère** les quatre boutons, et
laisse chaque bouton signifier une seule chose pour toujours.

> **Règle de sécurité, elle, NON négociable quel que soit le schéma retenu :**
> **le menu est inerte tant que l'homme-mort est tenu.** Naviguer un écran à deux mains
> pendant que 50 kg roulent, c'est l'accident. Homme-mort tenu ⇒ l'OLED n'affiche que la
> conduite, les boutons de menu ne font rien. Cette règle se teste sur l'hôte (§6, T2).

### 4.5 Protocole série : un **nouveau** type de périphérique — DÉCIDÉ

On ne touche pas au device `JOYSTICK` existant ni à `send_gamepad` : une trame étendue
casserait le contrôle `len(msg) == 4`. On déclare un **nouveau type** (`remote_usb`) avec
son propre décodeur, à côté. L'existant continue de marcher sans être relu.

Trame proposée, une ligne ASCII terminée par `\n`, **émise inconditionnellement à 50 Hz**
(c'est cette répétition qui fait vivre le deadman aval — un boîtier silencieux au repos
serait indistinguable d'un boîtier débranché) :

```
R;<seq>;<x>;<y>;<flags>;<crc8>\n
    seq   : compteur 0..255, pour détecter les trames perdues
    x, y  : entiers signés -1000..+1000 (centré, zone morte appliquée à bord)
    flags : masque hexadécimal — bit0 homme-mort, bit1..4 boutons, bit5 SW
    crc8  : sur tout ce qui précède
```

**Pourquoi un CRC sur un câble USB, qui a déjà le sien ?** Parce que le CRC de l'USB protège
le transport, pas le décodage : une trame tronquée à la reconnexion, un buffer réassemblé de
travers, et `x` prend une valeur plausible. Sur un chemin qui commande des roues, une valeur
plausible et fausse est le pire cas. `firmware/pico_odometry` a déjà tranché dans ce sens.

**Découpage du code — on copie la convention `pico_odometry`, qui est bonne :**

| Fichier | Où il tourne | Testé ? |
|---|---|---|
| `firmware/remote_usb/remote_protocol.py` | RP2040 **+ nœud/décodeur hôte + tests** | ✅ à écrire |
| `firmware/remote_usb/code.py` | RP2040 seul (broches, ADC, boucle) | ❌ non importable sur l'hôte |
| `firmware/remote_usb/boot.py` | RP2040 seul (déclaration USB) | ❌ |

Tout ce qui peut être *faux* — le signe des axes, la zone morte, le masque de boutons, le
CRC — vit dans le fichier partagé, exercé par les tests du dépôt. C'est ce qui évite
d'écrire deux fois une convention de signe et d'inverser un axe sans s'en apercevoir.

### 4.6 L'OLED : **local seul** — DÉCIDÉ (choix de David)

L'écran n'affiche que ce que le boîtier sait de lui-même : axes, homme-mort tenu ou relâché,
cran de vitesse, bouton actif, état de la liaison vue de son côté. **Aucun flux descendant**
(robot → télécommande) n'est à écrire, et le boîtier reste utile branché sur une machine qui
ne connaît pas le protocole. Conséquence assumée : **la batterie et l'état du robot ne
s'afficheront pas.** Si ce besoin revient, il rouvrira cette décision — et imposera un
canal descendant plus un nœud qui l'alimente.

Le potentiomètre-limiteur de vitesse proposé le 14/09 a été **écarté par David** au profit
des boutons. Les voies A2/A3 restent libres : la décision est réversible sans redessiner.

---

## 5. Ce que ce boîtier change — et ce qu'il ne change pas

**Il change** : un geste volontaire peut enfin arrêter les roues (§4.3) ; la simulation se
pilote au joystick au lieu du clavier ; le projet gagne des sources pour `e_stop`.

**Il ne change pas** : les roues au sol restent suspendues au test scénique (priorité 1) et
au protocole caméra ; `direction_sign` n'est toujours pas tranché en réel ; la chaîne de
sécurité matérielle (watchdog, `OE`, coup-de-poing) reste physiquement inexistante.

> ⚠️ **Le jour où ce boîtier commande des roues réelles, il entre dans le chemin roues** :
> validation en simulation d'abord, puis **protocole caméra** roues hors sol, plus revue par
> un modèle fort. Tant qu'on est en simulation et au banc, rien de tout ça ne s'applique —
> et c'est justement pourquoi les lots T0-T3 sont conçus pour rester de ce côté-là.

---

## 6. Lots

| Lot | Contenu | Où ça se vérifie | Verrou |
|---|---|---|---|
| **T0** | **Lever l'inconnue USB** : `boot.py` minimal, CDC-data + HID gamepad ensemble sur le XIAO. Le seul but est de savoir si CircuitPython tient les deux. | carte nue sur le PC : `lsusb`, `/dev/ttyACM*`, `evtest` | — |
| **T1** | `remote_protocol.py` + ses tests hôte (CRC, zone morte, signes, masque, trame tronquée) | `.venv/bin/pytest` | — |
| **T2** | `code.py` : lecture ADC, pull-up du `SW`, 4 boutons, homme-mort, émission 50 Hz. Règle « menu inerte si homme-mort tenu » testée en T1. | banc, joystick câblé à l'air | T0 |
| **T3** | **Simulation** : le boîtier pilote Gazebo via `joy_node` + `teleop_twist_joy` (`enable_button` = homme-mort) | sim headless + console web | T0, T2 |
| **T4** | Intégration `dadou_control_ros` : type `remote_usb`, `SERIAL_ID`, décodeur | dépôt télécommande | T1-T3 |
| **T5** | OLED : référence à identifier, menu local | banc | OLED en main |
| **T6** | Boîtier imprimé 3D (PETG), après que l'électronique marche à l'air | CR-10 | T2 |

L'ordre compte : **T0 peut invalider le §4.2 à lui seul**, et il coûte une soirée. Rien ne
doit être soudé ni imprimé avant qu'il ait répondu.

---

## 7. Inconnues à lever (et par qui)

| # | Inconnue | Comment la lever | Bloque |
|---|---|---|---|
| 1 | CircuitPython tient-il **HID + CDC-data** sur RP2040 ? | T0, 1 soirée | §4.2, donc T3 |
| 2 | Référence exacte de l'OLED (SSD1306 ? SH1106 ? 128×64 ? adresse 0x3C ?) | David : lire la carte ou une photo | T5 |
| 3 | Schéma **A ou B** pour les 4 boutons (§4.4) | arbitrage de David | T2 |
| 4 | Le `SW` du joystick est-il câblé ? (il coûte la dernière voie libre, §4.1) | arbitrage de David | T2 |
| 5 | Valeur des potentiomètres du `HW-504` | ohmmètre, 1 min | rien (informatif) |
| 6 | Dimensions du RP2040-One / Zero (jamais publiées en texte) | pied à coulisse, si on change de carte | §4.1 si repli |
| 7 | Combien de XIAO exactement ? (l'inventaire dit 1 sûr + 2 cartes Seeed non identifiées) | ouvrir le tiroir | T2 |

---

## 8. Provenance des chiffres du §4.1

Relevé le **2026-09-14** sur les pages officielles (wiki Seeed, wiki Waveshare, docs
CircuitPython), avec les réserves suivantes, à ne pas effacer :

- Les **dimensions des cartes Waveshare** ne sont publiées qu'en image de plan coté, jamais
  en texte. Une valeur vue en synthèse de moteur de recherche a été **écartée** faute de page
  primaire. Si on passe au RP2040-One, **mesurer au pied à coulisse**.
- Le mapping GP26-29 → ADC0-3 du RP2040-Zero/One n'est confirmé que par des sources tierces ;
  le wiki officiel dit seulement « 4 × ADC 12 bits ».
- L'absence de conflit sur A3/GP29 du XIAO de base est établie **par contraste** avec le
  paragraphe du modèle *Plus* (où GP29 est multiplexé avec la mesure batterie), pas par une
  phrase affirmative. À confirmer à la première lecture analogique.
- Le nombre d'endpoints USB du RP2040 n'est chiffré **nulle part** dans la doc consultée.

Conformément à la règle du projet, aucun de ces chiffres n'a été écrit de mémoire ; ceux qui
manquent sont déclarés manquants plutôt que comblés.
