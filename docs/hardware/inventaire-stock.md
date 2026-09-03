# Inventaire du stock de composants (2026-09-03)

> **État : passe complète du dépouillement vidéo faite.** 427 des 650 images de la vidéo
> d'atelier ont été lues (les 223 écartées sont les plus floues). Ce qui reste à lever ne
> l'est plus par l'image : ça demande d'ouvrir un sachet, retourner une carte ou sortir un
> pied à coulisse — voir §3. Le plan de marquage et de rangement qui en découle est dans
> **`docs/hardware/rangement-atelier.md`**.

**À quoi sert ce fichier.** À être lu par l'IA **avant toute commande**. Le chantier
« inventaire du stock » (`docs/chantiers.md`) est né d'un constat : en deux heures, le stock
a démenti deux fois la liste de courses de l'odométrie (74AHCT125, puis PC817). Acheter ce
qu'on possède déjà coûte de l'argent, du délai, et **3,60 € de droits par catégorie** depuis
juillet 2026. Toute nomenclature d'achat doit être confrontée à ce fichier d'abord.

**Ce que ce fichier N'EST PAS.** Un inventaire vérifié. C'est un **dépouillement visuel**
d'une vidéo de 10 min 50 s filmée à main levée le 2026-09-02 (+ une photo). David a prévenu
en la tournant : *« tu ne pourras sans doute pas tout voir, il y a des boîtes avec plusieurs
éléments »*. L'image a maintenant été exploitée jusqu'au bout (§4) ; ce qui reste flou ne se
lèvera qu'en atelier. Donc :

- **Aucune quantité n'est comptée.** Ce sont des ordres de grandeur vus du dessus, sans
  vider un seul bac : **toutes les quantités sont des minorants**.
- **Aucune référence n'est déduite.** Une ligne ne porte une référence que si la sérigraphie
  ou l'étiquette a été **réellement lue**. Sinon la colonne est vide et la désignation reste
  descriptive (« condensateurs électrolytiques radiaux »), ce qui est utile et honnête.
- **Le boîtier prime sur la référence** — c'est lui qui décide (DIP-4 vs SOP-4, DO-41 vs SMA,
  AHCT vs AHC). Quand il n'est pas mesurable à l'image (pas d'un JST, d'un bornier), c'est
  écrit, et **c'est un préalable bloquant** à toute commande de contrepartie.

**Colonne « repère »** : l'horodatage dans la vidéo (`t0495` = 8 min 15 s). C'est aujourd'hui
la seule adresse dont on dispose — voir « Limite n° 1 » plus bas.

---

## 1. Ce que cet inventaire change, tout de suite

### 1.1 Confrontation avec la liste de courses de l'odométrie

C'est l'usage même de ce fichier. `docs/etude-odometrie.md` §9 liste ce qui **reste à
acheter** pour souder la carte. Voici cette liste passée au stock. **Rien ici n'est une
autorisation de ne pas acheter** : quatre lignes sur douze deviennent des *vérifications à
faire en atelier*, ce qui n'est pas la même chose.

| Ligne de la nomenclature | Ce que dit le stock | Verdict |
|---|---|---|
| 2 × Barrette **mâle 1×9** | Barrettes sécables mâles 2,54 mm en masse (`t0378`, 30-50 barrettes) | **Probablement inutile d'acheter** — sécable, donc la longueur ne pose pas de problème |
| 2 × **JST-XH 4 pts** + boîtiers + contacts | Boîtiers JST blancs 2 à 6 points **et** deux compartiments pleins de contacts à sertir (*photo*) | **À vérifier en priorité** — voir §1.2 |
| 1 × **JST-XH 2 pts** + boîtier + contacts | idem | **À vérifier** — voir §1.2 |
| 1 × C **100 µF / 25 V** radial | Kit BOJACK : la valeur `100 µF 25 V 5×11` figure au tableau, 20 pcs (`t0625`) | **Probablement en stock** |
| 4 × **LED 3 mm** | Plusieurs centaines de LED, mais identifiées **5 mm** (`t0134`). Un sachet paraît plus petit, non confirmé | À vérifier — sinon acheter |
| 4 × Support **tulipe DIP-4** | Supports DIP tulipe vus (`t0004`) mais **le nombre de points n'est pas lisible** | À vérifier — le DIP-4 est rare, ne pas parier dessus |
| 2 × Barrette **tulipe 1×9** sécable | Non identifiée distinctement | À acheter, sauf découverte |
| 8 × R **1,5 kΩ** et **10 kΩ** 1/4 W | **Aucun bac de résistances n'a été identifié dans toute la vidéo** | À acheter — et voir §3, limite |
| 4 × C **10 nF** céramique | Le kit BOJACK est un kit d'**électrolytiques** : il ne couvre pas le 10 nF | À acheter |
| 1 × **1N5819** (Schottky DO-41) | ~50-100 diodes DO-41 en stock, **références illisibles** (`t0014`) | À vérifier à la loupe — voir §3 priorité 2 |
| 1 × **P6KE15A** / SA15A (TVS) | Rien d'identifié | À acheter |
| 1 × **PTC 500 mA** | Rien d'identifié | À acheter |
| 2 × **RP2040-Zero** (Waveshare) | ⚠️ **Pas de Zero, mais beaucoup de RP2040** : `Seeed XIAO-RP2040`, `Waveshare RP2040-One` (le grand frère du Zero, même famille castellée), et **~5-10 cartes format Pico** (`c0301`-`c0306`) | **À examiner avant d'acheter** — voir ci-dessous |

**⚠️ Le point RP2040 mérite un examen, pas une conclusion.** Le plan de plaque à bandes de
l'odométrie (`26 × 29 trous`, commit `99db4d8`) a été dessiné **pour le RP2040-Zero
précisément** : module sur barrette tulipe 1×9 par côté, bus 3,3 V/GND devant toucher ses
pastilles, coupures placées en conséquence. Les cartes RP2040 en stock ont des **brochages et
des encombrements différents** — le `RP2040-One` est plus long, le `XIAO` a 7 broches par
côté, une carte format Pico fait 2×20. **Aucune n'est un remplacement direct.**

L'arbitrage appartient à l'étude, pas à l'inventaire : soit on redessine la plaque autour
d'une carte qu'on possède déjà, soit on achète les deux Zero. Mais commander sans avoir
regardé serait la quatrième fois que le stock dément cette liste de courses.

**Ce que ça change concrètement** : la commande reste nécessaire (résistances, TVS, PTC,
céramiques, et peut-être les Zero). Mais elle peut se réduire de plusieurs lignes — et
surtout, chaque ligne évitée est potentiellement **3,60 € de droits de catégorie**
économisés, ce qui est l'ordre de grandeur du composant lui-même.

> ℹ️ **Les capteurs `LJ12A3-4-Z/BX` ne sont PAS une découverte** — l'étude le sait déjà
> (§9 : « capteurs et optocoupleurs : rien à acheter », ×6 reçus le 14/07). L'inventaire
> apporte deux choses : la **confirmation visuelle** avec la référence lue au zoom sur
> l'étiquette (`187-LJ12A3-4-Z/BX`, repère `t0495`, corps M12, LED témoin, 3 fils), et un
> **écart de comptage à lever** : la vidéo montre **3 sachets scellés** (un 4ᵉ en bord de
> cadre) alors que l'étude en compte **6 (4 + 2 rechange)**. Soit les autres sont ailleurs,
> soit la marge de rechange n'existe pas. À compter avant de s'y fier.

### 1.2 La boîte de connecteurs (photo) mérite un contrôle dédié

La photo prise juste après la vidéo montre une boîte à ~20 compartiments **pleine** de
connectique à sertir : deux compartiments entiers de **contacts métalliques nus** (plusieurs
milliers), des boîtiers noirs (Dupont/IDC) et une majorité de **boîtiers blancs JST de 2 à
6 points**.

Le commit `99db4d8` a établi que « les petits JST de David sont bien des **XH** (pas 2,5 mm) »
— vérification faite parce qu'un PH (2,0 mm) aurait cassé le plan de plaque. Si ce sont bien
ces connecteurs-là, alors les trois lignes JST-XH de la nomenclature (boîtiers **et**
contacts) sont couvertes. **C'est le contrôle le plus rentable de tout ce fichier** : il
porte sur trois lignes de commande et demande de vérifier deux choses en atelier —
qu'il existe des boîtiers **4 points** et **2 points**, et que les contacts nus sont bien
des contacts **XH** (et non des Dupont, qui leur ressemblent).

### 1.3 Un plan B optique existe pour l'odométrie

Repères `t0216`, `t0227`, `t0230` : **fourches optiques** (photo-interrupteurs à barrière,
boîtier en U traversant) en vrac — environ 5 nues visibles — **et** ~8 à 10 modules montés
« MH-Sensor-Series » (fourche + comparateur SOP-8 + ajustable + sortie VCC/GND/DO/AO).
C'est la solution classique du disque cranté. À connaître, **sans rouvrir l'arbitrage** :
l'étude a tranché pour l'inductif et elle a de bonnes raisons (§4). Simplement, si un
capteur venait à manquer, il existe une réponse en stock avant d'ouvrir un panier.

### 1.4 Autres pièces qui touchent des chantiers ouverts

| Pièce | Repère | Pourquoi ça compte |
|---|---|---|
| **Cytron MDDS30** (double driver moteur, 7-35 V) — ~2 ex. | `t0600`, `t0649` | Étage de puissance des roues. Savoir s'il existe un **spare** change la criticité d'une panne moteur. |
| **Mean Well SD-50B-5** (DC 19-36 V → 5 V 10 A) | `t0532` | L'étude odométrie mentionne « le rail Mean Well 12 V existe ». Celui-ci est un **5 V 10 A** : à ne pas confondre. |
| **DIANQI D-30A** (secteur → +5 V 4 A / +12 V 1 A) — 3 à 5 cartons **neufs** | `t0584` | Alims d'établi/banc. Le 12 V n'y est que **1 A** : insuffisant pour 4 capteurs + moteurs. |
| **Matrices LED RGB WS2812B-64** (8×8) — 3 à 5 | `t0054` | Même famille que le visage. Utile en rechange/essai, sans toucher au câblage gravé (`image_mapping.py`). |
| **PCA9685** (PWM 16 voies I²C) | `t0273` | C'est le driver de servos du robot. Un exemplaire de rechange en stock. |
| **SN74AHCT125N** DIP-14 — ~6 à 8 | `t0006` | Le level shifter déjà identifié le 2026-08. Confirmé et localisé. |
| **Entretoises laiton hex + visserie** — 200+ | `t0630`, `t0635` | Fixation des cartes. **Filetage non déterminé (M2.5 ou M3)** : à mesurer. |
| **Embouts de câblage VE, coffret 1800 pcs** | `t0642` | Câblage propre des borniers de puissance. Sections lues : 0,5 mm² (500 pcs) et 0,75 mm² (400 pcs). |

### 1.5 Un isolateur audio à transformateurs, pour le chantier « ronflement »

Repère `c0331` : une petite carte rouge portant **deux transformateurs audio**, **deux jacks
3,5 mm** (un droit, un coudé) et deux connecteurs blancs 3 points, sérigraphiée `HIFI` d'un
côté et `Car Audio` de l'autre, avec les repères `R` et `L`. C'est un **isolateur de masse
audio par transformateur** — le composant fait exactement pour couper une boucle de masse
entre deux appareils.

Le chantier voix (`docs/etude-voix-didier.md`, et le ronflement secteur confirmé le 30/08
comme venant de l'alimentation du Pi 5) est aujourd'hui bloqué par un bruit qui couvre la
voix humaine à 3 m. **Ça ne garantit rien** : un isolateur coupe le bruit qui passe par la
masse audio, pas celui qui est rayonné ou conduit par l'alimentation elle-même. Mais c'est
un essai de dix minutes, avec une pièce déjà là, avant d'acheter une DI ou une alimentation
linéaire.

---

## 2. Table de stock

Confiance : **H** = référence lue ou forme sans ambiguïté · **M** = famille sûre, détail non ·
**B** = identification par la forme seule, à vérifier physiquement.

### 2.1 Semi-conducteurs et composants discrets

| Désignation | Référence lue | Boîtier / format | Qté (minorant) | Repère | Conf. |
|---|---|---|---|---|---|
| Tampon/level shifter Texas Instruments | `SN74AHCT125N` (lot 2380758) | DIP-14 traversant | ~6-8 | t0006 | H |
| **Optocoupleurs** | `PC817` + `C202F` (**lu**, logo Sharp) | **DIP-4 traversant** | **plein compartiment, ~60-100** | c0022-c0028 | H |
| Diodes de redressement | — | DO-41 axial, sur bande | ~50-100 | t0014 | M |
| Diodes signal/Zener (verre, bagues) | — | DO-35 axial, sur bande | ~30-50 | t0014 | M |
| Transistors, sur bande | `BC547B` (**suffixe lu**, 2 images) | TO-92 | ~10-50 | c0032, c0033 | H |
| Fusibles verre, triés par taille | — (**calibres non lus**) | cartouche 5×20 **et** 6×30 | **~150-250** | c0639, c0640 | H |
| Transistors en vrac, **lot hétérogène** | — | TO-92 | ~50-80 | t0014 | M |
| Transistors / régulateurs CMS | — | SOT-23, qq SOT-89 | ~30-40 | t0014 | B |
| Circuits intégrés CMS large corps | — | SOIC/SOP ~300 mil | 2-3 | t0014 | B |
| Inductances CMS blindées | — | ~7×7 mm | ~6 | t0014 | M |
| Composant de puissance non identifié | — | TO-220 | 1-2 | t0039 | B |
| Comparateurs (sur modules) | `LM393` | SOP-8 | ~4 | t0245 | H |

### 2.2 Passifs

| Désignation | Référence lue | Boîtier / format | Qté (minorant) | Repère | Conf. |
|---|---|---|---|---|---|
| **Kit condensateurs électrolytiques, 24 valeurs** | `BOJACK 630 PIECES` | radial 4×7 à 10×16 mm, 105 °C | ~500-630 | t0623 | H |
| Condensateurs électrolytiques de puissance | `220 µF 250 V`, marque `cheng`, série `CD11X` | radial gros Ø | 3 | t0439 | H |
| Condensateur d'antiparasitage secteur | `R.46 MKP X2 SH 0,22 µF 310 Vac` | film boîté radial | 1 | t0014 | H |
| Condensateurs film bleus | — | radial, pas ~5 mm | ~10-15 | t0014 | M |
| Potentiomètres ajustables (trimmers) | — | traversant 3 br., ~6×6 mm | ~50 | t0147 | H |
| Potentiomètres rotatifs, **déjà câblés** | fil `AWM 1007 22AWG` | corps 16 mm, montage panneau | ~10 | t0159 | H |

> Le kit BOJACK couvre 24 valeurs de 0,1 µF à 1000 µF (tableau relevé au repère `t0625`).
> **Avant d'acheter un électrolytique, regarder là.**

### 2.3 Cartes, modules et calculateurs

| Désignation | Référence lue | Format | Qté (minorant) | Repère | Conf. |
|---|---|---|---|---|---|
| **Driver double moteur brossé** | `Cytron MDDS30`, 7-35 V | carte + dissipateur | ~2 | t0600, t0649 | H |
| Driver moteur pont en H | `L298N` | module rouge | 1-2 | t0446, t0450 | H |
| Driver moteur pas à pas industriel | *(non lue)* — `DC 9~42VDC`, borniers PUL/DIR/ENA | boîtier alu à ailettes | 1 | t0490 | M |
| Drivers pas-à-pas sur cartes porteuses | *(puce non lue)* — carte `STEPPER Drivers…` | modules violets à dissipateur | ~6-10 | t0212, t0221 | M |
| Carte de puissance Cytron (2ᵉ modèle) | `Cytron` — **modèle non lu** | carte + dissipateur | 1 | t0599 | M |
| **Driver PWM 16 voies I²C** | `PCA9685 16-Channel 12-Bit PWM Driver` | carte à bornier + 16×3 | ≥1 | t0273 | H |
| Expandeur d'E/S I²C | `PCF 857…` (8574 ou 8575, **non tranché**) | carte | ≥1 | t0273 | B |
| Convertisseurs abaisseurs | `LM2596 DC-DC` | module ~22×43 mm | ~5-10 | t0263, t0266 | H |
| Modules RTC | `DS3231` + `MH` | carte + support CR2032 | 2-3 | t0099 | H |
| Centrale inertielle | `9 DOF` (sérigraphie) | breakout à picots | 1 | t0089 | H |
| **IMU 9 axes Adafruit — NEUVE, barrette non soudée** | `Adafruit BNO055` + « 9-Dof Accel+Gyro+Mag w/ Quaternion, Euler Heading. I2Caddr 0x28 0x29 » | breakout, sachet d'origine | 1 | c0258 | H |
| Accéléromètre analogique 3 axes | `HW` + `X-OUT / Y-OUT / Z-OUT` | breakout | 1 | c0091 | M |
| **HAT ventilateur Raspberry Pi — NEUF sous sachet** | `Argon Controllable FAN HAT` + `www.argon40.com` | HAT 40 br. + ventilo 30 mm | 1 | c0474 | H |
| Cartes RP2040 miniatures | `Seeed XIAO-RP2040` ; `RP2040-One` + `Waveshare` | castellé, USB-C | 1 + 1 | c0306 | H |
| Modules Bluetooth série (HC-05/06, réf non lue) | `STATE/RXD/TXD/GND/VCC/EN`, `LEVEL:3.3V`, `Power:3.6V—6V` | 1×6 | ~4 | c0317, c0318 | M |
| Lecteurs de carte microSD | `HW-125` (lu sur les 2) | carte + barrette 6 br. | **2** | c0329, c0330 | H |
| Cartes rondes type LilyPad | `HW-001` + `ATMEL` + `MEGA328P` | Ø50 mm, pastilles couture | 4-6 | c0321-c0325 | H |
| Capteur temp./humidité (réf non lue) | `DFROBOT` + `www.dfrobot.com` | Gravity 3 fils | 1 | c0329 | M |
| **Isolateur audio à 2 transformateurs** — *voir §1.5* | `HIFI` / `Car Audio` / `R` / `L` | carte ~45×30 + 2 jacks 3,5 | 1 | c0331, c0332 | H |
| Carte de charge lithium (nom non lu) | `B+` / `B-` / `TP2`, USB en bord de carte | carte CMS | 1 | c0113 | M |
| Carte de dev à chargeur LiPo (nom non lu) | `3.7/4.2V Batt`, `USB/BAT/EN/3.3V` | — | 1-2 | c0291, c0296 | M |
| Modules relais 1 canal, **en sachets ESD** | `NO … NC` (bobine non lue) | relais + bornier 3 pts | 2-4 | c0372-c0376 | M |
| Cartes Arduino Mega | `MEGA 2560` | format Mega | 1-2 | t0469 | H |
| Cartes format Mega / Uno / Leonardo | *(aucun nom lu)* | formats Arduino | 4-5 | t0442 | M |
| Clones Arduino Nano | boîte `ELEGOO NANO` | format Nano, USB mini-B | 5-7 | t0309 | H |
| Raspberry Pi Pico | brochage `GP16…GP28` lu | DIP-40 | 2-3 | t0303 | H |
| Cartes Teensy — **version non lue** | `Teensy` | 2×14 + pastilles arrière | 3-4 | t0303 | M |
| Cartes ESP32 LoRa | `HELTEC HTIT-WB32LA` | carte à barrettes | ≥1 | t0294 | H |
| Carte format Feather | `feather` | format Feather | ≥1 | t0295 | H |
| Modules radio 2,4 GHz | `NRF24L01` (versions SMA et antenne PCB) | header 2×4 | 3-5 | t0312, t0315 | H |
| Shield LoRa 868 MHz | `Dragino LoRa Shield v1.4`, `868` | shield Arduino Uno | 1 | t0463 | H |
| Modules capteurs à fourche optique | `MH-Sensor-Series` | carte + fourche + LM393 | 8-10 | t0227 | H |
| Modules capteur vibration/inclinaison | `LM393` lu, capteur **non tranché** | carte 35×15 mm | 4 | t0245 | M |
| Modules capteurs infrarouge (3 types) | — | cartes 3-4 broches | ~8 | t0327 | M |
| Capteurs à ultrasons | *(non lue — HC-SR04 probable)* | paire transducteurs Ø16 | 2 | t0481 | M |
| Carte relais multi-voies, **en sachet** | — | relais traversants | 4-8 voies | t0481 | M |
| Carte audio Adafruit + ampli | `Adafruit`, `Music…`, `Stereo Spk 4-8Ω BTL 3W max` | carte fille | 1 | t0185 | M |
| Module ampli audio (jack + volume + bornier HP) | *(puce masquée par un capot)* | carte rouge | 1 | t0241 | M |
| Afficheur de tension de batterie | `YB27V`, configuré **12 V** | encastrable panneau | 1 | t0195 | H |
| Adaptateur GPIO Raspberry Pi | `SINTRON ST-009 GPIO Plus` | HAT 40 br. | 1 | t0047 | H |
| Carte d'alimentation Raspberry Pi | `clean Power`, `GPIO-04` | HAT | 1 | t0047 | H |
| Adaptateur T-cobbler + nappe 40 c. | — | breadboard | 1 | t0356 | H |
| Petites cartes bleues **non identifiées** | — | ~2×4 cm, CI central | 20-30 | t0251 | B |

### 2.4 Alimentation et énergie

| Désignation | Référence lue | Format | Qté | Repère | Conf. |
|---|---|---|---|---|---|
| Alim DC/DC | `MEAN WELL SD-50B-5` — DC24V(19-36V) 3A → **+5 V 10 A** | châssis tôle perforée | 1 (+1-2 non lues) | t0532 | H |
| Alims secteur **neuves, en carton** | `DIANQI D-30A` — 100-240 VAC → **+5 V 4,0 A / +12 V 1,0 A** | open-frame à bornier | 3-5 | t0584 | H |
| Alims à découpage nues, substrat jaune | — | cartes nues secteur | ~10 | t0455 | M |
| Modules d'alimentation/charge USB, **sachets ESD scellés** | `SKU:705106991534`, `Code:G05-12`, « Dual USB / Type-C » | modules à bornier vert | 3-5 | t0103 | M |
| Connecteur de puissance | `XT90` (moulé) | paire câblée | 1 paire | t0380 | H |
| Connecteurs DC étanches | gravé `DO NOT DISCONNECT UNDER LOAD` (famille MC4) | IP67 à presse-étoupe | 3-5 paires | t0398 | H |
| Support de cellule 18650 | `18650` | traversant à clips | 1 | t0479 | H |
| Module type BMS/protection batterie | — | carte noire CMS | 1 | t0439 | B |

### 2.5 Actionneurs et mécanique

| Désignation | Référence lue | Format | Qté | Repère | Conf. |
|---|---|---|---|---|---|
| Motoréducteurs « TT » | — | carter jaune, double arbre | 3-5 | t0073 | H |
| Roues caoutchouc pour motoréducteurs TT | — | — | 2-4 | t0073 | H |
| Moteurs DC cylindriques (~35-37 mm) | — | flasque métal, JST 2 voies | 2-4 | t0073, t0439 | H |
| Châssis/plateaux robot plastique ajourés | — | — | 2 | t0079 | M |
| Entretoises hexagonales laiton + visserie | — | **filetage M2.5 ou M3 non tranché** | 200+ | t0630 | M |
| Moyeux / accouplements d'arbre percés | emballage `…RIKMAX.COM` | métal | ~10 | t0387 | B |
| Ventilateurs DC | — | cadre carré | 2 | t0487, t0470 | M |

### 2.6 Connectique et câblage

| Désignation | Référence lue | Boîtier / format | Qté | Repère | Conf. |
|---|---|---|---|---|---|
| **Boîte à 20 compartiments de connecteurs à sertir** | — | JST/Dupont blancs et noirs + **contacts nus** | plusieurs milliers | *photo* | H |
| Borniers débrochables verts (fiches + embases) | — | **pas non mesuré** (5,08 / 3,81 / 3,5 ?) | **300+**, 4 contenants | t0351, t0370, t0427, t0431 | H |
| Borniers à vis fixes pour CI, 2-3 pôles | — | traversant, pas ~5,08 | ~100 | t0431 | H |
| Barrettes sécables mâles/femelles, droites et coudées | — | 2,54 mm, 1 et 2 rangées | 30-50 barrettes | t0378 | H |
| Connecteurs IDC + nappes arc-en-ciel | — | 2,54 mm / nappe 1,27 mm | ~50 + plusieurs m | t0363, t0420 | H |
| Nappes GPIO 40 c. Raspberry Pi | — | IDC 40 | 2-3 | t0047 | H |
| Fils Dupont (M/M, M/F, F/F) | — | 2,54 mm | 100+ | t0367 | H |
| **Bornes de connexion rapide à leviers** | `WAGO 221` (**lu**) — 2, 3 et 5 pôles | à levier, sans vis | ~30-45 | c0425 | H |
| **Jacks DC triés par cote** — *le seul contenant du stock correctement étiqueté* | étiquettes manuscrites `2.1*5.5` et `2.5*5.5` | barrel DC, embases + fiches | 20-30 | c0637 | H |
| Cosses faston **laiton nues** + isolants nylon | — (**largeur non mesurée : 4,8 ou 6,35 ?**) | à sertir | ~100 + 100-200 isolants | c0511, c0512, c0514 | H |
| Coques métalliques de connecteurs + inserts 4 contacts (USB-A ?) | — | traversant | **100-200, bac saturé** | c0364, c0365 | M |
| Bobines de fil de câblage, 8 couleurs | `Haerkn` + `XDH Tech, Lyon` (**section non lue**) | bobines à flasques | 8 | c0551, c0554 | H |
| Cosses préisolées rouges (0,5-1,5 mm²) | — | faston / fourche / œillet | 100+ | t0370 | H |
| Cosses préisolées bleues (1,5-2,5 mm²) | — | œillet / faston | 100+ | t0370 | H |
| **Coffret d'embouts de câblage isolés** | `1800PCS VE TERMINALS` — `E0508` 0,5 mm² ×500, `E7508` 0,75 mm² ×400 | ferrules fût 8 mm | 1800 | t0642 | H |
| Manchons thermosoudables (solder seal) | — | codés couleur 0,5 à 6 mm² | 200-300 | t0518 | H |
| Gaine thermorétractable noire, tronçons | — | plusieurs Ø | 100+ | t0518 | H |
| Embouts/contacts laiton (« bullets ») | — | **usage non tranché** | 50-100 | t0394 | M |
| Fil souple au mètre, multi-couleurs et sections | — | ~0,25 à 2,5 mm² + un ≥4 mm² | dizaines de m | t0526 | H |
| Bobines de fil de câblage fin (7-8 couleurs) | — | **section non lue** | 7-8 bobines | t0552 | M |
| Jacks DC barillet (embases CI) | — | **Ø non mesuré (5,5/2,1 vs 2,5)** | ~15-20 | t0017 | M |
| Fiches RCA mâles + adaptateurs | — | à souder | ~20-30 | t0334 | H |
| Fiches jack 6,35 mm (coudées et droites, TS/TRS) | — | — | ~10-12 | t0341 | H |
| Colliers de serrage nylon | — | ~2,5×100 mm | 100+ | t0042 | H |

### 2.7 Interface homme-machine

| Désignation | Référence lue | Format | Qté | Repère | Conf. |
|---|---|---|---|---|---|
| **Capteurs inductifs M12** (odométrie) — *voir §1.1* | `187-LJ12A3-4-Z/BX` | M12 fileté, 3 fils, LED | **3 vus** (l'étude en compte 6) | t0495 | H |
| Interrupteur-sectionneur à bouton rouge | `YH02-A`, `AC-3 16A AC250V`, `IEC60947-3`, `IP55` | montage panneau | ~2 | t0164 | H |
| Interrupteurs à bascule grand format | `ON-OFF-ON ZENGTAI 15A 250VAC` | panneau, cosses à vis | 3-4 | t0166 | H |
| Interrupteurs à bascule (rockers) panneau | — (**calibre non lu**) | encastrable, cosses faston | ~25-35 | c0423 | H |
| Bloc marche/arrêt de machine, touches `I` vert / `O` rouge | — (`CE` seul lisible) | encastrable panneau | ~5-10 | c0161, c0171 | H |
| Coupe-circuit / sectionneur à poignée rouge, bornes à goujon | `BLAN…` (marque tronquée) | panneau, goujons laiton | 1-2 | c0163, c0165 | M |
| Boutons-poussoirs tactiles | étiquette `INTER À P… OFF-(ON) 12VDC`, `5 mm`, `0.05A` | 4 broches, 6×6 et 12×12 | ~40-60 | t0017, t0506 | H |
| Micro-interrupteurs à glissière | — | traversant, SPDT + multipos. | **100+** | t0173 | H |
| Interrupteurs DIP | — | traversant, 4 à 8 positions | ~10-20 | t0124 | H |
| Commutateurs à corps chromé (montage panneau) | `ON` / `OFF` sur bagues | filetage + écrou | ~10-20 | t0137 | M |
| LED 5 mm diffusantes, triées par couleur | — | traversant T-1¾ | **plusieurs centaines** | t0134 | H |
| Matrices LED RGB adressables 8×8 | `WS2812B-64`, « Only ONE Pin / 24 bit color / 64 RGB LEDs » | PCB 8×8, LED 5050 | 3-5 | t0054 | H |
| Cartes rondes à LED RGB + pastilles de couture | *(aucune marque lue)* | Ø ~50 mm | 2 | t0323 | B |
| Claviers matriciels 4×4 | — | à touches, sur carte | 2 | t0209, t0479 | H |
| Joysticks analogiques (thumbsticks) | — | modules 2,54 mm | 5-8 | t0180 | M |
| Afficheur OLED/LCD à nappe FPC | — | dalle + ZIF | 1 | t0204 | M |
| Pupitre : clavier 4×4 métallique + LCD graphique | — | carte magenta assemblée | 1 | t0649 | B |

### 2.8 Prototypage

| Désignation | Boîtier / format | Qté | Repère | Conf. |
|---|---|---|---|---|
| Plaques d'essai nues (pastilles, bandes, trous métallisés) | 2,54 mm, dont formats 100×160 | 10-15 | t0500 | H |
| Plaques à bandes cuivrées (stripboard), neuves + chutes | ~50×80 mm | ~5 | t0042 | H |
| Plaques d'essai sans soudure (breadboards) | 400 et 830 points | 3-4 | t0054, t0446 | H |
| Supports de circuit intégré tulipe | DIP traversant | ~10-20 | t0004 | M |

---

## 3. Zones d'ombre — par ordre de rentabilité

Ce que **David seul** peut lever, et qui rapporte le plus par minute passée.

### Priorité 0 — le stock invisible

Ces contenants n'ont **jamais été ouverts**. Tant qu'ils ne le sont pas, l'inventaire
ci-dessus est un **minorant**, et le risque de racheter ce qu'on possède reste entier.
C'est le seul travail qui *augmente* réellement l'inventaire.

0a. **4 à 6 colis d'expédition scellés** posés au sol (`c0550`-`c0558`). Contenu totalement
   inconnu.
0b. **3 boîtes bleues Cytron** au sol (`c0647`, `c0648`), plus une quatrième manipulée
   (`c0609`) dont le modèle n'est pas lisible. Cytron fabrique des drivers de moteurs :
   c'est **le chemin roues**. À ouvrir en premier.
0c. **Sachets ESD opaques** — plusieurs bacs entiers plus un cageot (`c0478`, `c0480`,
   `c0548`). Un sachet ESD signale un composant qu'on a jugé utile de protéger.
0d. **Le sachet d'alimentations** du bac `c0452`-`c0454`, jamais ouvert (3 cartes identiques
   au moins).

### Priorité 1 — bloque une décision en cours

1. **La boîte à connecteurs JST** (*photo*) : y a-t-il des boîtiers **XH 4 points** et
   **2 points**, et les contacts nus sont-ils bien des **XH** ? Trois lignes de la commande
   d'odométrie en dépendent (§1.2). Le contrôle le plus rentable du fichier.
2. **Compter les capteurs `LJ12A3-4-Z/BX`** (`t0495`) : 3 vus, 6 annoncés par l'étude.
   L'écart porte sur la **marge de rechange**, pas sur la faisabilité. Trente secondes.
3. **Filetage des entretoises laiton** (`t0630`) : M2.5 ou M3 ? Un pied à coulisse, ou une
   vis M3 posée à côté. Sans ça, la boîte est inutilisable pour un achat complémentaire.
4. **Pas des borniers verts** (`t0351`, `t0427`, `t0431`) : c'est le plus gros stock de
   connectique du lot (300+ pièces réparties sur 4 contenants) et il est **inexploitable**
   tant que le pas n'est pas mesuré. Une mesure par contenant.
5. **Référence du 2ᵉ driver Cytron** (`t0599`), noyée dans un reflet. La gamme Cytron va de
   quelques ampères à 30 A : la ligne est sans valeur tant qu'elle n'est pas lue.

### Priorité 2 — gros volume documenté d'un coup

5. **Les diodes sur bande** (`t0014`) : ~150 composants, aucune référence lisible, mais
   elles sont **encore sur bande** donc homogènes par paquet. Une macro par paquet
   (une diode extraite, marquage à plat, lumière rasante) documente tout le compartiment.
   Meilleur rapport effort/gain de l'inventaire.
6. **Le sachet ESD des modules d'alimentation USB** (`t0107`) : jamais ouvert, la ligne
   « Item » de l'étiquette n'est nette sur aucune image. C'est probablement le composant le
   plus utile du lot.
7. **Les petites cartes bleues** (`t0251`) : 20-30 exemplaires, le lot le plus nombreux du
   meuble, **totalement non identifié** (carte MCU ? module driver ?). Une seule carte à
   plat, recto-verso, tranche la question pour tout le lot.
8. **Les sachets antistatiques fermés** (`t0083`, `t0481`, `t0312`) : contenu inconnu par
   construction. Zone d'ombre structurelle.

### Priorité 3 — précisions utiles

9. Version des **Teensy** (`t0303`) — 3.x ou 4.x change la tolérance 5 V des E/S. À traiter
   comme un point de sécurité si une Teensy devait un jour approcher le chemin roues.
10. Pas des **connecteurs JST blancs** (`t0073`, `t0363`, `t0327`) : PH 2,0 vs XH 2,5. Le
    stock existe en masse mais reste incommandable sans cette mesure.
11. Référence du **TO-220 isolé** (`t0039`), du **module ampli** (`t0241`, puce sous capot),
    du **module rouge à 2 TO-220 et 3 ajustables** (`t0446`, fonction non établie).
12. Sorties exactes des **alims DIANQI** : lues (5 V 4 A / 12 V 1 A) sur `t0584` mais floues
    sur `t0608` — vérifier que tous les cartons sont bien le même modèle.

### Limite n° 1 : le stock n'a pas d'adresse

**Aucun bac, aucun tiroir n'est étiqueté** dans toute la vidéo. Le meuble mural compte
~100 bacs à bec ; les casiers gris en comptent autant. Cet inventaire dit *ce qu'il y a*,
il ne dit **pas où le retrouver** — la colonne « repère » renvoie à une seconde de vidéo,
pas à un emplacement.

C'est la limite qui plafonne toute la suite : un inventaire non adressé se re-périme au
premier rangement.

**La passe complète a montré que c'est plus facile que prévu** : **tous** les bacs et tous
les tiroirs portent déjà un **porte-étiquette moulé d'origine**, et **tous sont vides**. Le
support existe, il n'y a rien à acheter. Le plan de marquage complet — quoi écrire, dans
quel ordre, et pourquoi le précédent étiquetage n'a pas tenu — est dans
**`docs/hardware/rangement-atelier.md`**. Dès qu'une étiquette est posée, la colonne
« repère » de ce fichier devient une **adresse**, et l'inventaire cesse d'être un
dépouillement pour devenir un vrai inventaire.

### Limite n° 2 : le passif de base n'a pas été filmé

**Aucun bac de résistances n'apparaît dans les 130 images.** Aucun bac de condensateurs
céramiques non plus (hors le kit BOJACK, qui est un kit d'électrolytiques). C'est
invraisemblable pour un atelier de ce volume : ces bacs existent forcément, la caméra ne
les a simplement pas croisés.

Conséquence directe : les lignes « R 1,5 kΩ / 10 kΩ » et « C 10 nF » de la nomenclature
odométrie sont marquées « à acheter » **par absence de preuve, pas par preuve d'absence**.
Un plan de 30 s sur le rangement des résistances et des céramiques réglerait probablement
plusieurs lignes de commande d'un coup — c'est le complément le plus rentable à filmer.

### Piège documenté : les sachets sont réemployés

Au repère `t0004`, un sachet étiqueté **« INTER A LEVIER — ON-ON 10A 250V »** contient en
réalité des `SN74AHCT125N` et des chutes de stripboard. **L'étiquette d'un sachet ne vaut
pas description de son contenu.** Ne jamais inventorier sur la foi d'une étiquette de sachet
sans avoir vu l'intérieur.

---

## 4. Méthode, et comment compléter

**Source** : `docs/pictures/stock/VID_20260902_235700.mp4` (10 min 50 s, 1080p60, muette —
David ne commente pas) et `IMG_20260903_000903.jpg` (boîte de connecteurs à sertir).

**Dépouillement, en deux passes** :
- *Passe 1* — extraction à 1 image/s (650 images), puis sélection automatique de **l'image la
  plus nette par tranche de 5 s** (variance du laplacien) → 130 images dans `best/`, nommées
  `tXXXX` par horodatage. Lues par 13 agents en parallèle.
- *Passe 2 (complète)* — les **297 images nettes restantes** que la passe 1 n'avait pas
  regardées (dossier `complement/`, nommées `cXXXX`), en 30 lots temporels **contigus** :
  une même scène étant vue sous plusieurs angles, une sérigraphie illisible sur une image
  l'est parfois sur sa voisine. C'est ce qui a permis de lire `PC817 C202F`, `BC547B`,
  `WAGO 221` ou l'étiquette `DIANQI D-30A`.
- Au total **427 des 650 images** ont été lues ; les 223 écartées sont sous le seuil de
  netteté (35ᵉ percentile) et n'auraient rien apporté.

Consigne unique et stricte à tous les agents : **ne citer une référence que si elle est
réellement lue**. Vérification directe des lectures qui engagent une décision (le
`LJ12A3-4-Z/BX` a été recadré, redressé et relu à la loupe).

**Une fausse alerte corrigée** : un agent a conclu que la vidéo était **en miroir** (logo
Arduino inversé) et a invalidé toutes ses indications gauche/droite. C'est faux —
l'étiquette `187-LJ12A3-4-Z/BX` de `t0495` se lit de gauche à droite dans le bon sens. Les
textes « inversés » sont des objets posés à l'envers ou vus par transparence. **Les
indications gauche/droite du dépouillement restent valides.**

**Les médias ne sont pas versionnés** (la vidéo pèse 1,6 Go ; le dépôt est public). Ils
vivent dans Nextcloud, donc sauvegardés, et sont exclus par `.gitignore`. Pour re-dépouiller
sans la vidéo, les 130 images de `best/` suffisent.

**Pour compléter** : refilmer les points de la section 3 **en gros plan, à plat, sans
flash** (lumière rasante), un objet par plan, et relancer le même dépouillement. Un plan
fixe de 3 s vaut mieux qu'un panoramique de 30 s : c'est la netteté qui décide, pas la
durée.
