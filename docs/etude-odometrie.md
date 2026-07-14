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
  pneu │ jante │ COURONNE 428 │ écrou+rondelle │ FILETAGE NU │ ÉTRIER alu + ROULEMENT │ châssis
                                                      ↑
                                       ~30 mm de tige filetée libre
```

- **L'axe est une TIGE FILETÉE** (Ø ~12–14, à confirmer au pied à coulisse), pas un rond lisse.
  Elle **tourne avec la roue**, dans un roulement logé dans un **étrier alu en U** usiné, lui-même
  boulonné au châssis.
- **La chaîne est marquée 428** → pas de **12,7 mm** confirmé (l'étude le supposait).
- La **couronne est boulonnée à la jante par 3 boulons**, freinés au fil.
- Il reste **~30 mm de filetage nu** entre l'étrier et l'écrou de moyeu.

Cette tige filetée n'est pas une contrainte : c'est un **cadeau**. Un filetage est une interface
de fixation gratuite, réglable et démontable — voir §3 bis.

## 3. La cible — DÉCIDÉ : roue phonique, lue par la FACE

Un **disque d'acier** serré sur l'axe Ø 20 par une bague fendue, découpé de **lumières
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

## 3 bis. La FIXATION — DÉCIDÉ (2026-07-14, après photos) : deux écrous sur la tige filetée

Le disque se serre **entre deux écrous, sur le filetage nu de l'axe**, dans le créneau de
~30 mm qui reste entre l'étrier de palier et l'écrou de moyeu. Rien d'autre. Pas de perçage,
pas de soudure, pas de collier, pas une seule pièce du robot démontée.

### Pourquoi PAS sur les 3 boulons de la couronne (la piste évidente, et le piège)

C'était tentant : trois boulons déjà là, un grand cercle de perçage, un grand rayon de lecture
donc une belle résolution. **Non.** Ces trois boulons sont le **chemin de couple** de la roue :
tout ce qui fait avancer 50 kg de robot passe par eux. Y ajouter une pièce impose des vis plus
longues, un nouveau serrage, un frein-filet refait — donc de remettre en cause une liaison qui
fonctionne, pour un capteur en lecture seule. La règle du projet vaut ici comme ailleurs : on
ne touche pas au chemin roues sans nécessité. Il n'y en a aucune.

### Pourquoi le serrage par écrous suffit largement

Parce que **le disque ne transmet aucun couple** : il ne fait que tourner. Rien ne le freine,
rien ne le pousse. Le seul effort est son inertie propre — quelques dizaines de grammes.

Le seul vrai risque est qu'il **patine** sur la tige, et il faut le prendre au sérieux : *une
odométrie qui patine ment sans prévenir*, et le robot croit avoir parcouru une distance qu'il
n'a pas faite. D'où deux remparts :

1. **Une empreinte hexagonale dans le moyeu**, qui vient sur un écrou de l'axe : le disque est
   entraîné en **prise mécanique positive**, pas par la seule friction du serrage.
2. **Un repère fraisé sur la tranche** : d'un coup d'œil, roue en main, on voit si le disque a
   tourné sur son axe.

### La cible : des têtes de vis M8, pas des lumières découpées

Un inductif ne voit **que le métal** — le plastique lui est parfaitement transparent. Le disque
imprimé n'est donc pas un pis-aller : c'est un **porte-cibles**. Ce que le capteur voit, ce sont
**12 têtes de vis M8 en acier** (Ø 15 mm sur angles ≥ 3 × Sn, la règle des inductifs), montées
tête côté capteur. Imperdables, épaisses, et elles ne se décollent pas sous vibrations — ce que
des rondelles collées feraient tôt ou tard.

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
          ┌────┴─────────┐                 │     │   PC847     │
          │   CAPTEUR    │      (noir)     │     │   canal n   │
          │ LJ12A3-4-Z/BX├─────────────────┴── IN-│             │
          │     NPN      │                        │  OUT ───────┼──→ GPIO Pico
          └────┬─────────┘                        │  (rappel 10k vers 3,3 V)
        (bleu) │                                  └─────────────┘
    GND 12 V ──┘
        ◄──── domaine 12 V ────►  ┊  ◄──── domaine 3,3 V ────►
                                  ┊
                    BARRIÈRE : les deux masses ne se rejoignent NULLE PART.
                    Sur le PCB : fente fraisée sous le PC847.
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

### Lien Pico ↔ Pi : USB

Un câble USB court : alimentation et données dans le même fil, `/dev/ttyACM0` côté Pi.

- **Figer le nom** par une règle udev sur le numéro de série → `/dev/didier-odom`, passé au
  conteneur robot dans le `docker-compose` (déployé par Ansible comme le reste).
- **Prévoir 3 pastilles UART sur le PCB** : ça coûte zéro, et si l'USB s'avère capricieux en
  tournée (le micro-USB du Pico est son point faible), on bascule sans refaire la carte.
- **Surtout pas d'I²C** : ce bus est celui des actionneurs, il est isolé par l'ISO1540, et il
  a déjà produit un incident (`docs/incidents/2026-07-13-glitch-visage-driver-led.md`). Y
  ajouter un participant imposerait de repasser le protocole caméra, pour un capteur en
  lecture seule.

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

Conséquence à écrire noir sur blanc : **si le lien USB meurt, on perd l'odométrie — donc la
navigation autonome s'arrête — mais aucun rempart de sécurité ne tombe.** Le deadman 400 ms
de `wheels_node` reste intact. Une panne d'odométrie ne peut produire qu'un arrêt, jamais un
emballement.

## 7. Inconnues à lever

Le **pas de chaîne est levé** (428 → 12,7 mm) et la **place sur l'axe** est cadrée (~30 mm de
filetage nu). Restent **cinq cotes au pied à coulisse**, et une seule est bloquante :

| # | Cote | Pourquoi elle compte | Hypothèse |
|---|---|---|---|
| 1 | **Garde axe → châssis** (au-dessus) | ⚠️ **BLOQUANTE** : elle plafonne le rayon du disque, donc la résolution | 70 mm |
| 2 | Ø de la tige filetée + cote sur plats de son écrou | trou central et empreinte hexagonale du moyeu | M12 / 19 mm |
| 3 | Longueur exacte de filetage nu | le moyeu + 2 écrous doivent y tenir | 30 mm |
| 4 | Ø extérieur du pneu | conversion ticks → mètres (rien d'autre) | 250 mm |
| 5 | Ø et entraxe des vis du châssis | interface du support capteurs | M6 / 40 mm |

Contrainte de dimensionnement, inchangée : **pas de lecture ≥ 2 × le diamètre du nez** (M12 →
≥ 24 mm), sinon le capteur voit deux cibles à la fois et ne distingue plus rien. S'y ajoutent
deux règles d'inductif que le §3 passait sous silence : **cible ≥ 3 × Sn** (12 mm) et **vide
entre cibles ≥ 3 × Sn** — sans vide suffisant, le capteur reste collé à l'état « métal » et le
train d'impulsions disparaît purement et simplement.

Ces quatre contraintes sont **codées en `assert()`** dans `plans/odometrie/parametres.scad` :
une géométrie fausse **refuse de compiler**, au lieu de produire un STL qu'on ne découvrirait
mauvais que sur le robot.

Géométrie retenue (avec les hypothèses ci-dessus) : **12 cibles à R = 52 mm**, disque Ø 129 mm,
pas de lecture 27,2 mm (métal 15 / vide 12,2), entraxe des capteurs 37,5°.
Après décodage ×4 : **16,4 mm de résolution au sol**. C'est moins que les 10 mm visés — la
garde au châssis interdit un grand disque — mais cela reste largement suffisant pour nav2
(l'EKF et le lidar corrigent) et correct pour asservir la vitesse à 20 Hz. Si la mesure #1
donne plus de place, augmenter `R_LECTURE` et `N_CIBLES` : la résolution suit.

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

Seulement là, et seulement si les étapes 1–3 sont vertes. Fente fraisée sous le PC847, Pico
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
| Écrous + rondelles larges au Ø de l'axe (M12 ?) | 6 |
| Vis M8×16 tête H + écrous nylstop (les **cibles**) | 24 + 24 |
| Impression PETG : 2 disques, 2 supports, 1 banc | — |

## 10. Pédagogie

Une maquette 3D interactive explique le principe (le capteur est fixe, ce sont les dents qui
défilent ; un capteur seul ne connaît pas le sens ; la roue phonique lue à l'horizontale) :
`/home/dadou/capteur-dents.html` — page autonome, à ouvrir dans un navigateur.
