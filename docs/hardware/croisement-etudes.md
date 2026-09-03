# Croisement de l'inventaire avec les études (2026-09-03)

Passe faite après la passe complète du dépouillement : `docs/hardware/inventaire-stock.md`
confronté aux études du dépôt, pour chercher d'autres cas de **« on s'apprête à acheter ce
qu'on possède déjà »**. Le chantier est né de deux cas avérés (74AHCT125, PC817), un
troisième a été trouvé au dépouillement (RP2040).

**Résultat global, dit franchement : aucun nouveau démenti de liste de courses.**
Sur les quatre études croisées, **zéro remplacement direct**. Ce n'est pas un échec — c'est
une information : les gros gisements d'économie étaient sur l'odométrie (seule étude à avoir
une vraie nomenclature d'achat), et ils ont été exploités. Ce que cette passe apporte est
ailleurs, et vaut la peine d'être lu : **trois mises en garde**, **une pièce à chercher**, et
**la liste de ce qu'il faudra vraiment acheter**.

---

## 1. ⚠️ Sécurité — le stock ne contient AUCUN arrêt d'urgence

C'est le résultat le plus important de cette passe, et il va à contre-courant de l'espoir de
départ.

`CLAUDE.md` note que **`e_stop` n'a aucune source** et que c'est à câbler. L'étude interface
web (§2, l. 28-32) demande un **coup-de-poing sans fil** coupant la puissance roues. On
pouvait espérer que le stock aide. **Il n'aide pas, et se croire couvert serait dangereux.**

**Le piège précis** : l'inventaire liste un « interrupteur-sectionneur à bouton rouge »
`YH02-A`, `AC-3 16A AC250V`, **`IEC60947-3`**, IP55 (repère `t0164`). Rouge, gros, d'aspect
rassurant. Mais :

- **La norme lue est la mauvaise.** `IEC 60947-3` = appareillage de **sectionnement**. Un
  organe d'arrêt d'urgence relève de **`IEC 60947-5-5`** (ouverture positive, verrouillage
  mécanique) et `EN ISO 13850` pour la fonction. **Aucune pièce du stock ne porte 60947-5-5.**
- **Calibre AC seulement** (`AC-3`, catégorie moteur alternatif), **aucune valeur DC lue**.
  Or la puissance roues est du **DC** (Cytron MDDS30, 7-35 V). Couper du DC inductif avec un
  contact dimensionné AC est le piège classique : sans passage par zéro, l'arc ne s'éteint
  pas, **le contact se soude — l'arrêt d'urgence ne coupe plus**.
- Accrochage et configuration NO/NF **non lus**. Et il est **filaire**, donc hors sujet pour
  la ligne « sans fil ».

**Même réserve sur les relais** (`c0372`-`c0376`, `t0481`) : calibre des contacts et tension
de bobine **non lus**, en sachets jamais ouverts. Un module relais logique typique tient
~10 A ; couper l'alimentation d'un robot de 50 kg via un driver 30 A est hors de ce domaine.
Un contact sous-dimensionné sur une chaîne d'arrêt = contact soudé = **arrêt inopérant**.

**Ce qui est quand même utile** : ces relais permettent de **maquetter le schéma sur banc**
(roues hors sol, protocole caméra) pour valider la logique **à manque de courant** — bobine
alimentée en marche normale, passage de puissance par le contact NO, de sorte que toute
perte (bouton enfoncé, pile morte, radio perdue, fil coupé) **retombe en ouverture**. Câblé
à l'envers, une pile morte donne un robot qui roule et un bouton qui ne fait rien.
Le schéma appartient à l'étude (§9.2) ; c'est signalé, pas décidé.

**À ne JAMAIS rapprocher d'une fonction d'arrêt d'urgence**, même sur un banc — la
ressemblance « bouton rouge » rend l'erreur facile : les poussoirs tactiles `t0017`/`t0506`
(momentanés, **50 mA**), les bascules `ZENGTAI` `t0166`, les rockers `c0423` (calibre non
lu), le bloc `I`/`O` `c0161`.

---

## 2. Une pièce à chercher avant tout achat : le ReSpeaker

L'étude déclenchement de conversation (§10.4) parle de la **DoA du ReSpeaker** comme d'une
chose possédée mais « pas fixée ». **Le ReSpeaker n'apparaît nulle part dans l'inventaire.**

Deux lectures : soit il n'est pas là, soit il dort dans un des contenants **jamais ouverts**
de la priorité 0 (colis scellés `c0550`-`c0558`, sachets ESD `c0478`/`c0480`/`c0548`).
C'est le cas d'école qui justifie la priorité 0 : **le chercher là avant toute décision DoA.**

---

## 3. Le FAN HAT Argon : la même pièce, trois avis opposés

Un `Argon Controllable FAN HAT` **neuf sous sachet** (`c0474`) a été rapproché
indépendamment par trois croisements. Les avis divergent, et c'est instructif :

| Étude | Intérêt | Réserve |
|---|---|---|
| Télédiagnostic | `ros2 bag` continu + Claude Code embarqué chauffent le Pi 4 | **Conflit de header 40 br.** : le GPIO porte déjà D16/D20/D21 et deux autres HAT (`SINTRON ST-009`, `clean Power GPIO-04`) |
| Voix | Le Pi 5 est en caisse close avec l'ampli, risque de throttling | Ajouter un ventilateur dans la caisse qui **porte le micro**, c'est injecter du bruit dans le problème qu'on résout |
| Conversation | — | ⚠️ **Contre-indication nette** : monté pendant la campagne D0, il relèverait le plancher de bruit et **fausserait la calibration du VAD** (seuils du §10.4 explicitement adossés à la chaîne actuelle) |

**Conclusion à retenir** : la pièce est là, gratuite, mais **elle ne doit pas être montée
pendant une campagne de mesure audio**. Compatibilité Pi 5 non établie non plus (le Pi 5 a
un connecteur ventilateur PWM dédié, géométrie différente).

---

## 4. Ce qui reste à acheter en entier — aucune contrepartie en stock

Dit explicitement pour que personne ne cherche deux fois :

| Besoin | Étude | Pourquoi rien en stock |
|---|---|---|
| **Routeur 4G/5G** (~50-100 € + forfait) | interface web §4 | Aucun modem cellulaire. Les radios en stock (nRF24, LoRa 868, BT série) ne transportent pas d'IP |
| **Carte SD d'endurance** | télédiagnostic §6 | Aucune carte SD nue. Le `HW-125` est un **lecteur SPI pour microcontrôleur**, il ne stocke rien et ne remplace pas la carte de boot d'un Pi |
| **SBC / RAM Pi 4** | télédiagnostic §8 | Aucun Raspberry Pi 4/5 ni équivalent. Que des MCU (Pico, RP2040, Teensy, Arduino, ESP32). La RAM du Pi 4 est soudée de toute façon |
| **Micro / préampli / array** | conversation §5.5 | **Rien** : aucun micro, aucune capsule électret, aucun préampli, aucune carte son d'entrée |
| **Accélérateur Hailo / Coral** | conversation §5.6 | Rien |
| **Fiches jack 3,5 mm à souder** | voix §6 | Les seuls 3,5 mm du stock sont **montés sur** l'isolateur `c0331` — pas des pièces détachées |
| **Coup-de-poing d'arrêt d'urgence** | interface web §2.2 | Voir §1 ci-dessus |

---

## 5. Ce qui devient actionnable sans rien acheter

- **Banc d'essai de portée radio, gratuit** : nRF24L01 (3-5, versions SMA et PCB), Dragino
  LoRa 868 + Heltec ESP32, plus les MCU aux deux bouts. L'étude web demande un « test de
  portée en salle » (l. 204) — il peut se faire ce week-end. ⚠️ Réserve de fond : l'étude
  exige un dispositif « indépendant de tout logiciel » ; **tout montage maison à base de ces
  modules EST du logiciel**. L'arbitrage produit du commerce vs maison appartient à l'étude.
  Réserve de bande : le 2,4 GHz est saturé en salle de spectacle (public + wifi du lieu) ; le
  868 a une **limite de rapport cyclique** mal adaptée à un lien devant émettre en continu.
- **Banc voix V0 montable sans achat** : fiches jack 6,35 TS/TRS (10-12), fil, gaine, et
  ~50 trimmers pour le pad d'atténuation — **sous réserve de lire leurs valeurs**, jamais
  filmées. Manque uniquement la fiche 3,5 mm côté Pi.
- **A/B manuel au banc** : 100+ micro-interrupteurs SPDT `t0173` permettent l'écoute alternée
  du §7-3 sans toucher aux relais ni au câblage — conforme au « aucune modification
  permanente » du lot V0.
- **Poussoir du bouton START** (télédiagnostic) : 40-60 poussoirs `OFF-(ON) 12VDC 0.05A`,
  cohérents avec une entrée GPIO. ⚠️ Le verrou de l'étude n'est **pas** la pièce, c'est
  qu'**aucun GPIO libre n'est documenté**. Et le sachet est de ceux qui mentent (voir §6).
- **Isolateur audio à transformateurs** (`c0331`) : essai de 10 min contre le ronflement,
  avant d'acheter une DI. Il éclate aussi L/R sur deux connecteurs, ce que demande le câble
  en Y du §6 voix. Ne couvre que le bruit passant par la masse audio.

---

## 6. Deux pièges confirmés par cette passe

1. **Les sachets mentent.** Le sachet `INTER À P…` qui contient les poussoirs est du même
   type que celui étiqueté « INTER A LEVIER » qui contenait des `SN74AHCT125N`. À ouvrir
   avant de s'y fier. (Règle de rangement associée : barrer l'étiquette d'un sachet
   réemployé — `rangement-atelier.md` §3.1e.)
2. **Les valeurs manquent partout.** Trimmers sans valeur, fusibles sans calibre, relais sans
   tension de bobine, cosses sans largeur, borniers sans pas. C'est le même angle mort que la
   « limite n° 2 » de l'inventaire (résistances et céramiques jamais filmées). **Une pièce
   dont on ne connaît pas la valeur ne dispense pas d'acheter** — elle oblige juste à
   mesurer avant.

---

## 7. Ce que ça ajoute à la liste atelier

À faire pendant l'étiquetage, le bac en main (s'ajoute à `inventaire-stock.md` §3) :

1. **Ouvrir les colis scellés en cherchant un ReSpeaker** (§2).
2. **Lire sur le `YH02-A`** : accrochage ? contacts NO/NF ? **calibre DC** ? Trois questions
   qui décident s'il a une place quelconque dans un schéma (§1).
3. **Lire sur les modules relais** : calibre des contacts et tension de bobine (§1).
4. **Lire le calibre du coupe-circuit à goujons** `c0163`/`c0165` — c'est potentiellement le
   sectionneur de consignation du robot, gratuitement.
5. **Lire les valeurs des trimmers** `t0147` (~50) — débloque le pad du banc voix.
6. **Filmer le bac de résistances et de céramiques** — débloque à la fois l'odométrie et le
   pad voix. Trente secondes, le meilleur rapport de toute la liste.
