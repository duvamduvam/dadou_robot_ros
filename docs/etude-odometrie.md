# Étude — odométrie des roues (retour de rotation)

*Décidée le 2026-07-14. Ne pas re-trancher ce qui est marqué DÉCIDÉ : les alternatives ont
été pesées, et les raisons du rejet valent plus que la conclusion. Les inconnues restantes
sont listées en §7.*

## 1. Le problème

Les roues de Didier n'ont **aucun retour de rotation**. Ce n'est pas un oubli, c'est une
conséquence du matériel : le moteur est un **MY1016Z à balais** (et non un brushless, comme
la fiche matériel l'a longtemps prétendu à tort — corrigé le 2026-07-14). Un moteur à balais
n'a pas de capteurs Hall de commutation ; il n'y a donc rien à dériver, aucun encodeur
gratuit. Le Cytron SmartDrive40 qui le pilote est lui aussi un driver *brushed* (PWM + DIR)
et n'expose aucune sortie tachymétrique.

Deux conséquences, qu'il faut bien distinguer parce qu'elles se réparent ensemble mais ne
font pas mal au même endroit :

**La boucle de vitesse est ouverte.** `/cmd_vel` est un mensonge poli : les m/s commandés
sont un rapport cyclique PWM déguisé. La vitesse réelle dérive avec la tension batterie, le
sol, la pente, la charge. Sur 50 kg, le robot ne va pas droit et ne tourne pas d'un angle
connu.

**Il n'y a pas d'odométrie.** Nav2 exige une TF `odom` → `base_link` localement lisse : AMCL
s'en sert comme modèle de mouvement, les contrôleurs y déroulent leurs trajectoires, la
costmap locale s'y accroche. Sans elle, nav2 ne démarre pas.

Ni le lidar ni la caméra ne comblent ce trou. Le lidar peut fabriquer de l'odométrie par
recalage de scans, mais dans une salle de théâtre — rideaux noirs, public mobile, décor
déplacé entre les scènes, murs longs et symétriques — c'est le pire cas du scan-matching, et
à 10 Hz ça ne referme jamais une boucle de vitesse. La caméra monoculaire 130°, elle,
n'a **pas d'échelle métrique** : elle ne peut pas produire de vitesse en m/s.

## 2. La contrainte mécanique — RELEVÉE SUR PHOTOS le 2026-07-14

⚠️ **Correction.** Cette section affirmait « axe acier Ø 20 mm ». C'est **faux** : les photos
du train arrière (2026-07-14) montrent tout autre chose. La conception qui en découlait — une
**bague de serrage fendue Ø 20** en nomenclature — est **caduque**.

Ce qu'il y a réellement, de l'extérieur vers l'intérieur :

```
  pneu │ jante │ COURONNE 428 │ écrou M20 │ FILETAGE NU │ ÉTRIER alu + ROULEMENT │ châssis
                                   ↑            ↑
                        l'ENTRAÎNEUR      > 35 mm de tige filetée libre
                        (déjà en place)
```

- **L'axe est une TIGE FILETÉE M20** — mesuré au mètre le 14/07 : l'écrou fait **30 mm sur
  plats**. Le Ø 20 de l'étude était donc juste ; ce qui était faux, c'est qu'il soit **lisse**.
- **Elle TOURNE avec la roue** — vérifié au feutre (trait tracé sur la tige, roue tournée à la
  main : le trait suit). Ce n'est pas un détail de curiosité : c'est le **postulat de tout le
  montage**. Si la tige avait été un axe mort et la roue montée sur ses propres roulements, un
  disque serré dessus n'aurait mesuré rigoureusement **rien**.
- **La chaîne est marquée 428** → pas de **12,7 mm** confirmé (l'étude le supposait).
- La **couronne est boulonnée à la jante par 3 boulons**, freinés au fil.
- Il reste **plus de 35 mm de filetage nu** entre l'étrier et l'écrou de moyeu.

Cette tige filetée n'est pas une contrainte : c'est un **cadeau**. Un filetage est une interface
de fixation gratuite, réglable et démontable — voir §3 bis.

⚠️ **Mais le M20 coince** : un écrou M20 fait **16 mm de haut**. Serrer le disque entre deux
écrous *ajoutés* coûterait 2 × 16 + 6 (disque) = **38 mm** — plus que les 35 disponibles. C'est
cette cote, et elle seule, qui impose le montage en **coiffe** du §3 bis.

### La garde sous la caisse : 30 mm — et le piège qu'elle tend

Mesuré le 14/07 : **il n'y a que 30 mm entre l'axe et le bas de caisse.** De quoi croire le
disque mort-né (celui qu'on avait dessiné faisait 129 mm de Ø, il aurait tapé au premier tour).

Sauf que **cette garde ne vaut que sous la caisse, à l'aplomb de l'étrier**. Plus loin le long
de l'axe, côté roue, la caisse s'arrête — et **la couronne le prouve** : elle fait ~90 mm de
rayon et elle tourne déjà librement, tous les jours. Il y a **plus de 20 mm de créneau** entre
le bord de la caisse et la face de la couronne.

D'où la géométrie retenue, qui n'est pas intuitive et mérite d'être retenue telle quelle :

```
        │ caisse ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
        │  30 mm ↕              │← la caisse s'arrête ici
   ─────┼───────────────────────┼──────── axe M20 ────────
        │ contre-écrou │ COIFFE │ DISQUE R=78 │ écrou │ COURONNE R≈90
        │   (sous la caisse :   │  (dans le créneau :   │
        │    R=22 < 30, ça passe)│  le grand rayon y est permis)
```

**Le grand disque va du côté de la couronne, pas du côté de la caisse.** Seule la coiffe
(R = 22 mm) passe sous la caisse, où elle tient sans peine dans les 30.

⚠️ Conséquence à ne pas rater au montage : **rien ne doit dépasser côté couronne**. Les écrous
des cibles sont donc **noyés dans des lamages**, et c'est ce qui fixe l'épaisseur du disque
(10 mm). Une vis qui dépasse de ce côté-là tape la chaîne.

### La chaîne : le disque passe DEVANT, il ne la contourne pas

Mesuré le 14/07 : **la couronne ne fait que Ø 110**, donc la chaîne tourne dans un cercle de
**55 mm de rayon**. Le disque en fait 78. **Il déborde.**

Et pourtant il passe — parce qu'**un disque n'a pas à rester dans le cercle de la chaîne, il
lui suffit d'être hors de son PLAN**. Une 428 ne déborde que de ~6 mm de la face de la couronne.
Le disque est donc **décalé de 10 mm par une jupe** : il passe *devant* la chaîne, ne la croise
jamais, et **garde son grand rayon — donc sa résolution**.

```
   face couronne ─┬─ chaîne (R=55, déborde de 6 mm)
                  │        ╭── DISQUE R=78, à 10 mm : hors du plan de la chaîne
                  │   ╭────┴──────────────╮
   ───────────────┴───┴──── axe ──────────┴──────
```

L'alternative — réduire le disque à R = 50 pour « rentrer dans la chaîne » — aurait coûté très
cher : 9 cibles au lieu de 15, soit ~22 mm/front, à peine une impulsion par période de contrôle
à 20 Hz. Inasservissable, une fois de plus.

⚠️ **Le créneau est désormais plein** : décalage (10) + disque (10) + tête de vis (5,3) +
entrefer (2,5) = **27,8 mm pour 30 disponibles**. Ça passe, mais sans gras — et ce qui taperait
la caisse, en cas d'erreur, ce serait **le nez du capteur**. Un `assert()` le vérifie.

## 3. La cible — DÉCIDÉ : roue phonique, lue par la FACE

Un **disque** serré entre deux écrous sur la tige filetée de l'axe (voir §2), portant des **cibles
radiales**. Le capteur est **couché, parallèle à l'axe**, face au disque : il voit défiler
*acier / lumière / acier / lumière*. C'est le principe d'une couronne d'ABS automobile.

### Pourquoi pas les dents du pignon (lecture radiale)

Ça marche, et ça ne demande aucune pièce neuve — c'était la première piste. Mais **la chaîne
impose le pas** : 12,7 mm. Un pas aussi serré force un capteur M8, qui ne détecte qu'à
1,5–2 mm. Cela veut dire un **entrefer d'un millimètre, à vie**, sur une machine de 50 kg qui
part en tournée.

Sur un disque qu'on dessine soi-même, on **choisit le pas** : on l'ouvre à 20–25 mm, ce qui
autorise un capteur M12 détectant à 4 mm, donc un entrefer de 2,5–3 mm — tolérant aux
vibrations, au jeu des paliers, au montage approximatif. Le montage à plat sur une platine
est en prime bien plus facile à aligner qu'une équerre à 1 mm d'une denture.

### Pourquoi pas la chaîne

Piste séduisante, et elle existe en industrie. Trois raisons de la garder en secours :

- **Elle n'apporte aucune résolution supplémentaire.** Par définition d'une transmission par
  chaîne, celle-ci avance d'exactement un pas par dent : compter les maillons ou les dents
  donne le même nombre d'impulsions par tour de roue. Pas de repas gratuit.
- **Elle fouette.** Plusieurs millimètres de battement latéral, face à une portée de
  détection de 1,5 mm → impulsions perdues. Une odométrie qui perd des impulsions dérive, et
  personne ne s'en aperçoit avant que le robot ne parte de travers.
- **Piège discret** : ses maillons alternent extérieur / intérieur tous les **deux** pas. Un
  capteur qui s'accroche sur ce motif-là plutôt que sur les rouleaux **divise silencieusement
  la résolution par deux**. Erreur invisible, robot qui croit avoir parcouru la moitié de la
  distance.

Si le disque s'avérait impossible à loger, la chaîne reste jouable — mais **sur le brin
tendu uniquement**, à deux ou trois centimètres du point de tangence, là où les dents la
contraignent géométriquement et où elle ne peut pas battre.

## 3 bis. La FIXATION — DÉCIDÉ (2026-07-14, après photos) : la COIFFE sur l'écrou de roue

Le disque **coiffe l'écrou M20 déjà en place** contre le moyeu de roue, et un **seul
contre-écrou** le bloque. Rien d'autre : pas de perçage, pas de soudure, pas de collier, pas
une seule pièce du robot démontée — et **on ne desserre jamais l'écrou existant**, on s'appuie
dessus (le contre-écrou pousse le disque vers la roue, donc dans le sens qui le serre).

### Pourquoi une coiffe, et pas simplement deux écrous

C'était le plan initial, et **le M20 l'a tué** : un écrou M20 fait 16 mm de haut, donc deux
écrous ajoutés plus le disque réclament 38 mm, pour 35 disponibles. Ça ne rentre pas.

L'écrou déjà monté résout le problème en rendant **deux services d'un coup**, gratuitement :

- il sert d'**entraîneur** — l'empreinte hexagonale de la coiffe s'emboîte sur ses 30 mm sur
  plats, donc le disque est entraîné en **prise mécanique positive** ;
- il sert d'**appui** — il ne reste plus qu'un écrou à ajouter.

Bilan : **22 mm consommés** (6 de disque + 16 de contre-écrou) au lieu de 38. La coiffe, elle,
ne coûte rien en longueur : elle enveloppe un écrou qui était déjà là.

### Pourquoi PAS sur les 3 boulons de la couronne (la piste évidente, et le piège)

C'était tentant : trois boulons déjà là, un grand cercle de perçage, un grand rayon de lecture
donc une belle résolution. **Non.** Ces trois boulons sont le **chemin de couple** de la roue :
tout ce qui fait avancer 50 kg de robot passe par eux. Y ajouter une pièce impose des vis plus
longues, un nouveau serrage, un frein-filet refait — donc de remettre en cause une liaison qui
fonctionne, pour un capteur en lecture seule. La règle du projet vaut ici comme ailleurs : on
ne touche pas au chemin roues sans nécessité. Il n'y en a aucune.

### Pourquoi un seul contre-écrou suffit largement

Parce que **le disque ne transmet aucun couple** : il ne fait que tourner. Rien ne le freine,
rien ne le pousse. Le seul effort est son inertie propre — quelques dizaines de grammes.

Le seul vrai risque est qu'il **patine**, et il faut le prendre au sérieux : *une odométrie qui
patine ment sans prévenir*, et le robot croit avoir parcouru une distance qu'il n'a pas faite.
D'où deux remparts :

1. **L'empreinte hexagonale de la coiffe** : le disque est entraîné par l'écrou lui-même, en
   **prise mécanique positive**, pas par la seule friction d'un serrage sur du plastique.
2. **Un repère fraisé sur la tranche** : d'un coup d'œil, roue en main, on voit si le disque a
   tourné sur son axe.

### La cible : des têtes de vis M8, pas des lumières découpées

Un inductif ne voit **que le métal** — le plastique lui est parfaitement transparent. Le disque
imprimé n'est donc pas un pis-aller : c'est un **porte-cibles**. Ce que le capteur voit, ce sont
**15 têtes de vis M8 en acier** (Ø 15 mm sur angles ≥ 3 × Sn, la règle des inductifs), montées
tête côté capteur, **écrou noyé côté couronne**. Imperdables, épaisses, et elles ne se décollent
pas sous vibrations — ce que des rondelles collées feraient tôt ou tard.

Écrous **normaux + frein-filet**, pas des nylstop : un nylstop M8 fait 8 mm de haut et ne
rentrerait pas dans le lamage.

Conséquence heureuse : **la géométrie validée en plastique est exactement celle qu'on gravera
dans l'acier**. Le prototype n'est pas une approximation du disque final, il en est le plan.

## 4. Le capteur — DÉCIDÉ : LJ12A3-4-Z/BX

Capteur de proximité **inductif** M12, **NPN NO**, 6–36 V DC, portée 4 mm, 500 Hz.
~2,35 € pièce (AliExpress, TENSTAR ROBOT). Ce n'est pas un « capteur de vitesse » automobile :
c'est un détecteur de métal industriel, et c'est exactement ce qu'il nous faut.

**Ce qu'il ne faut PAS acheter**, parce que la recherche « capteur de vitesse » n'y mène que :

- **Capteurs ABS / boîte de vitesses** : soit à réluctance variable — ils sortent une
  sinusoïde dont l'amplitude *croît avec la vitesse*, donc **rien du tout à basse vitesse**,
  or c'est précisément là que Didier vit ; soit actifs à sortie en courant (7/14 mA), qui
  exigent un circuit de conditionnement dédié.
- **Capteurs de vélo (Magene…)** : Bluetooth, et une impulsion par tour.
- **Kits e-bike (BAFANG…)** : leur fiche annonce « 1 pulse/cycle ». Une impulsion par tour.

### Deux pièges irréversibles

**⚠️ NPN, et JAMAIS PNP.** La variante `/BY` est PNP et se cache dans le *sélecteur de
couleur* de la même annonce. Une sortie NPN est un collecteur ouvert : elle ne fait que
**tirer vers la masse**, donc un rappel vers le 3,3 V du Pico donne un signal propre 0/3,3 V
alors même que le capteur est alimenté en 12 ou 24 V. Une sortie PNP **pousse la tension
d'alimentation** : elle enverrait 24 V dans un GPIO 3,3 V et tuerait le microcontrôleur.
Vérifier la variante dans le panier, pas dans le titre.

**⚠️ Mesurer avant de brancher.** Sur une pièce à 2 €, ne pas parier le Pico sur la fiche
technique : alimenter le capteur seul, et vérifier au multimètre que le fil noir **ne monte
jamais** à la tension d'alimentation. Puis optocoupler quand même (§5).

### Vérification de fréquence (rassurante)

Roue Ø 250 mm (à confirmer), 24 lumières, 1 m/s → **30 Hz**. Le capteur tient 500 Hz. Marge
d'un facteur 15 : même le capteur le moins cher est très largement assez rapide. Inutile de
payer plus.

## 5. L'isolation — DÉCIDÉ : 4 PC817 sur supports, sur la carte

Le châssis est électriquement hostile : deux moteurs **à balais** de 250 W (les balais
**arcent** en permanence), un ampli de sono, des rubans LED à fronts raides. On n'attaque pas
un GPIO en direct là-dedans.

**Quatre PC817 individuels (DIP-4), sur supports tulipe.** Le PC847 (quatre PC817 dans un seul
DIP-16) a d'abord été retenu, puis écarté : à 7 centimes la puce (lot de 20 pour 1,33 €), des
DIP-4 séparés se remplacent **un par un** dans une loge, sans fer à souder — même logique que le
Pico sur supports. Un PC847 grillé, c'est trois canaux sains jetés avec le quatrième. Le seul coût
est un peu de surface de carte : sans objet ici.

Surtout **pas** un module tout fait empilé en mezzanine : deux cartes, deux fixations, un
connecteur de plus à vibrer. Et le module d'établi devient inutile lui aussi — avec les puces
nues, **c'est nous qui choisissons la résistance série**, donc ce qu'on valide sur l'établi est
*exactement* ce qui partira sur le PCB. (Le module Keshy, lui, a une résistance d'entrée inconnue.)

**L'ISO1540 existant n'est PAS réutilisable** (la question s'est posée). C'est un isolateur
**I²C** bidirectionnel : ses deux canaux sont pris (SDA + SCL), ce n'est pas le bon type de
circuit, il est du mauvais côté du robot (les capteurs parlent au **Pico**, pas au Pi), et il
est **sur le chemin des actionneurs** — le bricoler imposerait de repasser le protocole
caméra. Pour économiser 2 €, c'est absurde.

### Câblage d'un canal

La LED de l'optocoupleur se branche « à l'envers » de l'intuition, parce que le capteur NPN
ne *pousse* rien : il **tire vers la masse**. C'est donc lui qui ferme le circuit de la LED.

```
   +12 V ──────┬───────────────────────────┬── IN+ ─┐
               │                           │        │
        (brun) │                           │     ┌──┴──────────┐
          ┌────┴─────────┐                 │     │   PC817     │
          │   CAPTEUR    │      (noir)     │     │   canal n   │
          │ LJ12A3-4-Z/BX├─────────────────┴── IN-│             │
          │     NPN      │                        │  OUT ───────┼──→ GPIO Pico
          └────┬─────────┘                        │  (rappel 10k vers 3,3 V)
        (bleu) │                                  └─────────────┘
    GND 12 V ──┘
        ◄──── domaine 12 V ────►  ┊  ◄──── domaine 3,3 V ────►
                                  ┊
                    BARRIÈRE : les deux masses ne se rejoignent NULLE PART.
                    Sur le PCB : fente fraisée sous les PC817.
```

- **Alimenter les capteurs en 12 V**, pas en 24 V (le rail Mean Well 12 V existe). Ils
  acceptent 6–36 V : c'est gratuit, ça réduit l'énergie qu'un défaut peut pousser dans le
  circuit, et l'immunité au bruit reste excellente.
- Résistance série : `(12 − 1,2) / 2200 ≈ 4,9 mA` dans la LED — largement assez pour un
  PC817 — et **0,05 W** dissipés. (C'est ce calcul que ratent les modules chinois à 1 kΩ
  quand on les attaque en 24 V : 0,5 W dans une résistance prévue pour 0,125 W. Elle noircit.)
- Rappel de sortie : **10 kΩ vers le 3,3 V**.
- **Conséquence logicielle : métal détecté = niveau BAS.** La logique est inversée.
- **Vitesse de l'optocoupleur** : un PC817 commute en quelques dizaines de µs, le signal
  plafonne à 30–60 Hz. Facteur mille de marge, ce n'est pas un sujet.
- **Test d'acceptation de l'isolation** : en continuité, entre la masse d'entrée et la masse
  de sortie, on doit lire un **circuit ouvert**. Si ça bipe, la carte n'isole rien.

## 6. L'architecture — DÉCIDÉ

### Deux capteurs PAR ROUE, donc quatre

Trois raisons indépendantes, chacune suffisante :

1. **Chaque roue a besoin de sa propre mesure.** Une traction différentielle tourne
   *précisément parce que* ses deux roues diffèrent.
2. **Un capteur seul ne sait pas dire l'avant de l'arrière.** Il voit du métal défiler,
   point : le train d'impulsions est identique dans les deux sens. Deux capteurs décalés
   donnent la **quadrature** — celui qui voit la lumière en premier révèle le sens — et
   exploiter les 4 fronts au lieu de 2 **quadruple la résolution**, gratuitement.
3. **Le sens doit être MESURÉ par roue, jamais déduit de la commande PWM.** En pivot sur
   place, une roue recule pendant que l'autre avance : supposer un signe commun ferait lire
   un pivot comme une ligne droite. Et un robot de 50 kg redescend seul une scène en pente.

**⚠️ Piège d'entraxe** : un quart de pas fait ~6 mm, un corps M12 en fait 12 — les deux
capteurs se rentreraient dedans. On les espace d'**un pas ET quart** : la phase électrique
est rigoureusement identique (c'est un modulo — le capteur ignore combien de lumières
entières le séparent de son voisin), et les corps ont la place.

### La carte va à côté du Pi, PAS près des roues

Contre-intuitif, et pourtant décisif. Le câble capteur porte un signal **12 V à collecteur
ouvert** : basse impédance, forte amplitude — une brute, quasi insensible aux parasites
(c'est pour ça que l'industrie l'utilise dans des armoires bourrées de variateurs). Le lien
Pico → Pi, lui, est du **3,3 V logique** : fragile.

Donc on fait porter la longue distance au signal robuste. La carte se monte **dans le boîtier
électronique**, le lien fragile fait 15 cm, et les câbles capteurs (1–2 m) partent vers les
roues. Les router **loin des câbles moteur et ampli** ; croiser à 90° si inévitable.

### Comptage : un Raspberry Pi Pico, pas le Pi

Python sur le Pi 4 perdrait des fronts. Le **PIO du RP2040 décode la quadrature en
matériel**, sans faute, et la carte sert au passage de tampon électrique.

### Lien Pico ↔ Pi : UART — DÉCIDÉ le 2026-07-14 (l'USB était le premier choix)

**J6, 4 broches : `+5V` · `TX` · `RX` · `GND`.** Le Pico est alimenté par le rail 5 V du robot
via une Schottky (D13) sur `VSYS`. L'USB **reste branchable**, mais seulement pour flasher le
Pico à l'atelier : il ne porte plus le lien opérationnel.

Pourquoi ce revirement : un connecteur **micro-USB sur un châssis de 50 kg qui part en tournée**
est le point faible du montage, et le nom du périphérique (`/dev/ttyACM0` ou `1`…) est une
loterie. L'UART donne un chemin fixe et un bornier qui ne se déboîte pas.

**La Schottky D13** aiguille le 5 V : le rail du robot entre par `VSYS`, mais ne peut pas
*remonter* dans le port USB du PC quand on flashe. Montage prescrit par la fiche du Pico ;
vérifié sur la netlist (`VBUS` reste isolée de `VSYS`).

### ⚠️ L'I²C est INTERDIT — et ce n'est pas une question de procédure

La question s'est posée (« l'USB me gêne, peut-on faire de l'I²C ? »). La réponse est non, et la
raison est un **scénario d'emballement**, pas une contrainte administrative :

`wheels_node.stop()` **écrit le PWM par le bus I²C** (`robot/actions/wheels.py` → PCA9685). Un
esclave I²C qui plante en tenant SDA à la masse **fige le bus entier**. Enchaînement :

> bus mort → `stop()` ne peut plus écrire → **le PCA9685 conserve sa dernière consigne** → les
> roues continuent de tourner.

Le deadman de 400 ms s'exécuterait, croirait avoir arrêté le robot, et n'aurait rien arrêté. Le
Pico serait le **seul composant du robot capable de tuer le frein**.

Un bus I²C **dédié** (le Pi 4 sait activer `i2c-3` à `i2c-6` par dtoverlay) contiendrait le
risque — un bus figé ne tuerait que l'odométrie. Mais il reste mauvais : le contrôleur I²C du Pi
a un **bug documenté d'étirement d'horloge** qui mord précisément sur les esclaves *logiciels*
(ce qu'est un RP2040 en mode esclave), et l'I²C est le bus le plus sensible aux parasites de ce
châssis — qui a **déjà produit un incident**
(`docs/incidents/2026-07-13-glitch-visage-driver-led.md`).

### Inconnue côté Pi

**Quel UART ?** Le primaire (GPIO14/15) est encombré par la console série et le Bluetooth. Un
UART dédié activé par `dtoverlay` (`uart2`…`uart5`) donnerait un `/dev/ttyAMA*` stable — **à
condition que ses GPIO soient libres sur la carte principale**, ce qui n'est pas encore vérifié.
À trancher avant de câbler.

### Protocole série

Une trame à 50 Hz, avec **numéro de séquence** et **somme de contrôle** :

```
ODO <seq> <ticks_gauche> <ticks_droite> <crc>\n
```

Le numéro de séquence n'est pas décoratif : c'est lui qui permet de détecter un lien mort ou
des trames perdues. Côté Pi, un nœud ROS 2 Python lit le port série et publie. Débogable à la
main par un simple `cat /dev/didier-odom`.

### ⚠️ Règle non négociable : le Pico ne commande RIEN

Il lit, il compte, il rapporte. Il n'est **pas** sur le chemin de commande des roues.

Conséquence à écrire noir sur blanc : **si le lien série meurt, on perd l'odométrie — donc la
navigation autonome s'arrête — mais aucun rempart de sécurité ne tombe.** Le deadman 400 ms
de `wheels_node` reste intact. Une panne d'odométrie ne peut produire qu'un arrêt, jamais un
emballement.

## 7. Inconnues à lever

Relevé du 14/07 — **six inconnues levées**, il en reste **trois**, et **plus aucune ne bloque** :

| Cote | Statut | Valeur |
|---|---|---|
| Pas de chaîne | ✅ levé (marquage 428) | 12,7 mm |
| Ø de l'axe + écrou | ✅ mesuré au mètre | **tige filetée M20**, écrou 30 sur plats / 16 de haut |
| Filetage nu au-delà de l'écrou | ✅ mesuré | **~30 mm** (de la visserie peut être ajoutée) |
| L'axe tourne-t-il avec la roue ? | ✅ vérifié au feutre | **oui** — postulat de tout le montage |
| Garde axe → bas de caisse | ✅ mesuré | **30 mm** — ne contraint que la coiffe (R=22), pas le disque |
| Créneau caisse ↔ couronne | ✅ mesuré | **30 mm** — et il est plein à 27,8 |
| Ø de la couronne (donc de la chaîne) | ✅ mesuré | **Ø 110** → chaîne à R=55. Le disque déborde, mais passe **devant** (jupe de 10 mm) |
| Écrou M20 du moyeu | ✅ vérifié | **standard, AVEC rondelle** — la rondelle est la face d'appui de la jupe |
| Épaisseur de cette rondelle | à confirmer | *hyp. 3 mm* — fixe la hauteur de jupe, donc la position du disque |
| Ø extérieur du pneu | à mesurer | *hyp. 250 mm* — convertit les ticks en mètres |
| **Entraxe des deux roues** | à mesurer | `wheel_separation` — indispensable à l'odométrie différentielle |
| Fixations sous la caisse + trajet de la chaîne | à relever | interface du support capteurs |

Fiche de relevé : **`plans/odometrie/MESURES.md`**.

Plus rien ne bloque l'impression du disque. L'épaisseur de la rondelle est la seule cote qui
puisse encore décaler la pièce (2 mm d'erreur sont absorbables, 5 mm non). Le pneu et l'entraxe
des roues sont les **deux seules constantes** qui convertissent les impulsions en mètres et en
radians : fausses, l'odométrie ment silencieusement et nav2 part de travers sans se plaindre.

Contraintes de dimensionnement, toutes **codées en `assert()`** dans
`plans/odometrie/parametres.scad` — une géométrie fausse **refuse de compiler** :
**pas de lecture ≥ 2 × Ø du nez** (sinon le capteur voit deux cibles à la fois), **cible ≥ 3 × Sn**,
**vide entre cibles ≥ 3 × Sn** (sans quoi le capteur reste collé à l'état « métal » et le train
d'impulsions disparaît), la coiffe qui passe sous la caisse, le disque hors du plan de la chaîne,
et l'encombrement du créneau.

**Géométrie retenue : 15 cibles à R = 65 mm**, disque **Ø 155 mm**, décalé de 10 mm, pas de
lecture 27,2 mm (métal 15 / vide 12,2), entraxe des capteurs 30°.
Après décodage ×4 : **13,1 mm de résolution au sol** — suffisant pour nav2 (l'EKF et le lidar
corrigent) et correct pour asservir la vitesse à 20 Hz.

Le contraste mérite d'être noté, parce qu'il justifie deux fois le même raisonnement : un disque
résigné à tenir **sous la caisse** aurait été plafonné à R = 25 (4 cibles, 49 mm/front) ; un
disque résigné à rentrer **dans le cercle de la chaîne** aurait été plafonné à R = 50 (9 cibles,
22 mm/front). Dans les deux cas, pas même une impulsion par période de contrôle à 20 Hz :
**inasservissable**. C'est d'avoir cherché la place *à côté* — dans le créneau, puis *devant* le
plan de la chaîne — qui sauve le chantier.

## 8. Plan de mise en œuvre — par étapes, du sûr vers le risqué

L'ordre n'est pas négociable : **on ne grave un PCB que quand on a déjà vu le système
fonctionner.** Le prototype EST le cahier des charges de la carte.

### Étape 1 — Établi, sans robot (zéro risque)

Banc de test : une chute de bois, des **rondelles d'acier vissées tous les 25 mm**, passée à
la main devant deux capteurs. Linéaire au lieu de rotatif, mais ça teste exactement la même
chose — et comme on peut la faire **aller et venir**, ça teste le **sens**, qui est tout
l'enjeu.

Valide : la détection, l'entrefer réel obtenu, la logique inversée, la quadrature, le
décodage ×4, le firmware Pico, le nœud ROS. Tout le logiciel se débogue là, sans robot.

### Étape 2 — Carte dédiée provisoire (plaque à trous)

La même chose soudée sur plaque à trous, avec le **brochage DÉFINITIF** (mêmes GPIO, mêmes
borniers, même ordre des capteurs). Ainsi le firmware et le nœud ROS écrits à l'étape 1 sont
*exactement* ceux qui tourneront sur le PCB : la vérification exécute le même code que la
prod.

Les composants sont les **mêmes qu'au PCB final** (PC817 nus + résistances choisies), pas un
module tout fait : ce qu'on valide sur l'établi est alors *exactement* ce qui sera gravé.

Le schéma KiCad de cette carte est fait et vérifié :
`~/Nextcloud/dev/didier/pcb/kicad/wheel-odometry/` (ERC 0 violation, netlist contrôlée,
plan de câblage plaque à trous dans son `DESIGN.md`).

### Étape 3 — Robot, ROUES HORS SOL, protocole caméra

Roue phonique et support capteurs **imprimés** (`plans/odometrie/`, cf. §3 bis), **roues hors
sol**, webcam USB, captures ffmpeg.

C'est ici qu'on mesure **enfin la vraie vitesse pour un PWM donné** — la première mesure
objective du chemin roues depuis le début du projet. Rejouer
`conf/scripts/validate-cmdvel-protocol.sh` en enregistrant l'odométrie en parallèle.

### Étape 4 — PCB KiCad

Seulement là, et seulement si les étapes 1–3 sont vertes. Fente fraisée sous les PC817, Pico
sur **supports tulipe** (un Pico grillé se change en dix secondes dans une loge, sans fer à
souder), **une LED de diagnostic par canal** (on *voit* un capteur mort ou un câble coupé
sans brancher d'ordinateur — utile sur un plateau, et ça alimente le chantier télédiagnostic).

### Étape 5 — Aval (hors périmètre de cette étude)

`ros2_control` / `diff_drive_controller`, EKF `robot_localization` (encodeurs pour la
translation + IMU BNO055 pour le yaw), puis nav2. À noter : **le BNO055 existe déjà dans le
code** (`robot/move/bno_055_extended.py`, `Wheels.set_9dof()`) mais **personne ne l'appelle
en production** — seulement dans `robot/tests/sandbox/`. Vérifier s'il est encore
physiquement sur le robot.

## 9. Nomenclature

### Achat immédiat (étapes 1–3)

| Pièce | Qté | Prix unitaire |
|---|---|---|
| Capteur inductif `LJ12A3-4-Z/BX` **NPN** (TENSTAR ROBOT) | 6 (4 + 2 rechange) | 2,35 € |
| **PC817C DIP-4**, lot de 20 (TriArk) — sert au prototype ET au PCB | 1 lot | 1,33 € |
| Supports tulipe DIP-4 | 4+ | qques centimes |
| Raspberry Pi Pico | 2 | ~5 € |
| Plaque à trous, borniers à vis 3 pôles, résistances 10 kΩ | — | qques € |

⚠️ **Grouper la commande** : capteurs et optocoupleurs viennent de vendeurs différents, donc deux
ports. Viser les seuils de livraison gratuite (10 € chez chacun), sinon le port coûtera plus cher
que les composants.

### PCB final (étape 4)

| Pièce | Qté |
|---|---|
| **PC817C** (DIP-4) + support tulipe | 4 (+ rechanges) |
| Résistances 2,2 kΩ (série LED, calibrées 12 V) | 4 |
| Résistances 10 kΩ (rappel vers 3,3 V) | 4 |
| Raspberry Pi Pico + supports tulipe | 1 |
| Bornier à vis 3 pôles (capteurs) | 4 |
| Bornier 2 pôles + fusible réarmable + TVS (entrée 12 V) | 1 |
| LED + résistance (diagnostic) | 4 |
| Disque phonique acier 3 mm, découpe laser — *même géométrie que le disque imprimé validé* | 2 |

~~Bague de serrage fendue Ø 20 mm~~ — **supprimée** : il n'y a pas d'axe Ø 20 lisse (§2). Le
disque se serre entre **deux écrous** sur la tige filetée. Ce qu'il faut acheter à la place,
pour l'étape 3 :

| Pièce | Qté |
|---|---|
| **Écrou M20** + rondelle large M20 (le contre-écrou du disque — *un seul par roue*, l'autre est déjà sur le robot) | 2 + 2 |
| Vis M8×16 tête H + écrous nylstop (les **cibles**) | 24 + 24 |
| Impression PETG : 2 disques, 2 supports, 1 banc | — |

## 10. Pédagogie

Une maquette 3D interactive explique le principe (le capteur est fixe, ce sont les dents qui
défilent ; un capteur seul ne connaît pas le sens ; la roue phonique lue à l'horizontale) :
`/home/dadou/capteur-dents.html` — page autonome, à ouvrir dans un navigateur.
