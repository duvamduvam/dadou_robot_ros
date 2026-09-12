# Alimentation 5 V dédiée du Raspberry Pi 5 (Mean Well SD-50B-5)

*Ouvert le 2026-09-12. Deux SD-50B-5 commandés par David (livraison annoncée 21-26/09).*

## 1. Pourquoi ce chantier n'est pas de la mécanique

C'est **l'exécution de la prochaine action du chantier 0** (`docs/chantiers.md`), donc de la
priorité de tête du projet. Rappel du verrou : le 2026-08-30, le ronflement qui rend la
conversation impossible a été attribué à **l'alimentation du Pi 5**, et le diagnostic a été
tranché en trente secondes — Pi 5 basculé sur batterie, le bruit disparaît. Raie dominante à
150 Hz (3ᵉ harmonique du 50 Hz) : c'est du **secteur**, pas du souffle.

Alimenter le Pi 5 depuis la batterie 24 V via un convertisseur DC/DC, **c'est supprimer la
liaison secteur par construction**. Ce support imprimé est donc le geste qui débloque
`chat_node` V2, pas un rangement d'atelier.

> ⚠️ **Le secteur peut revenir par la porte de derrière.** Le bénéfice n'existe que si la
> batterie n'est **pas en charge** pendant l'écoute : chargeur Victron branché = le secteur
> est de nouveau dans la boucle. À vérifier explicitement pendant les mesures avant/après,
> sinon on conclura à tort que la bascule n'a rien changé.

## 2. La référence — vérifiée, pas supposée

David a commandé **SD-50B-5**. La capture AliExpress transmise le 12/09 affichait
« SD-50C-24 » dans le sélecteur : c'était la variante par défaut de la fiche produit, David a
confirmé que la commande porte bien le B-5. L'écart méritait d'être levé, les deux axes de la
référence comptant :

| Suffixe | Plage d'entrée DC | Pertinent ici ? |
|---|---|---|
| SD-50**A** | 9,2 ~ 18 V | non |
| SD-50**B** | **19 ~ 36 V** | ✅ c'est la plage de la batterie 24 V |
| SD-50**C** | 36 ~ 72 V | non — **ne démarrerait pas** sur 24 V |

Le chiffre final est la tension de sortie : **-5 = 5 V**, -12, -24. Un SD-50C-24 aurait donc
été faux deux fois.

**SD-50B-5** : entrée 19-36 VDC, sortie **5 V / 10 A / 50 W**. Le Pi 5 tire environ 25 W au
pire, soit **~50 % de charge** — marge confortable, y compris en température (§4).

## 3. Cotes du boîtier (Case No. 901)

Source : **datasheet officielle Mean Well**, `docs/hardware/datasheets/SD-50-SPEC-2024-11-22.pdf`
(révision imprimée `SD-50-SPEC 2024-11-22`, récupérée le 2026-09-12 sur meanwell.com).
Les cotes ci-dessous ont été lues sur le **dessin vectoriel de la page 2 rendu en image**,
pas sur une extraction de texte — l'extraction texte ne conserve pas la géométrie des lignes
de cote et ne permet pas de savoir quel nombre appartient à quel trou.

**Tolérance annoncée par le constructeur : ± 1 mm.** Le support doit donc avoir du jeu.

### Hors-tout
**159 × 97 × 38 mm** (L × l × H). Le capot mesure 152,5 ; la semelle dépasse en pattes.

### Trous de fixation — deux jeux, tous **M3 taraudés**

**Fond (semelle) — `2-M3`**, alignés :
- à **24 mm** du petit côté porte-bornier, puis **78 mm d'entraxe** (donc 24 et 102) ;
- sur une ligne à **65 mm** d'un grand côté (soit 32 mm de l'autre).

⚠️ Deux vis **alignées** ne bloquent pas la rotation autour de leur axe. Fixer l'alim par le
fond seul exige que le support l'épaule par ailleurs.

**Chaque flanc — `3-M3`, en triangle** (repères depuis le coin haut, côté bornier) :
- (**22** ; **18,5**)
- (**139** ; **9**) — soit 22 + 117
- (**139** ; **27**) — le troisième est 18 mm sous le précédent

Ce triangle est la **bonne prise** : trois points non alignés, blocage complet, vis M3 courtes.

**Trous de passage ø3,5** dans les pattes de semelle, à 4,5 mm du bord.

### Bornier
5 points sur un petit côté, en léger retrait (152,5 vs 159) :

| Broche | Fonction | Broche | Fonction |
|---|---|---|---|
| 1 | DC INPUT V+ | 4 | DC OUTPUT −V |
| 2 | DC INPUT V− | 5 | DC OUTPUT +V |
| 3 | FG (masse châssis) | | |

**FG n'est pas le 0 V.** C'est la masse de châssis — son traitement n'est pas neutre sur un
robot dont le chantier ouvert est un problème de masse audio.

### Profondeur de vissage M3
**Non donnée par la datasheet.** Une vis trop longue dans un flanc touche l'électronique :
à mesurer sur la pièce en main avant de choisir la longueur.

## 4. Thermique — le montage vertical gagne 5 °C

La courbe de derating porte **deux échelles de température distinctes**, libellées
`(VERTICAL)` et `(HORIZONTAL)` : à charge égale, le boîtier monté **vertical** tolère **5 °C
d'ambiance de plus** que monté à plat (60 vs 55 °C en bout d'échelle). Le SD-50B tient 100 %
de charge jusqu'à ~40 °C avant de dérater.

Conséquences retenues pour le dessin :
- **orienter le boîtier verticalement**, ouïes dans le sens de la convection ;
- **ne pas masquer les ouïes** : elles sont sur les flancs et le capot, donc les joues du
  support ne doivent couvrir que les zones de perçage ;
- **décoller l'alim du bois** par des bossages — air et découplage des vibrations ;
- **PETG, pas PLA** : le PLA flue vers 60 °C, ce qui est précisément la plage de travail.

## 5. Décisions de conception du support

| Point | Décision | Raison |
|---|---|---|
| Prise sur l'alim | **les 3 M3 d'un flanc** (ou des deux) | triangle = pas de rotation, contrairement aux 2 M3 alignés du fond |
| Fixation au bois | **vis à bois directes** à travers des pattes | choix de David ; simple et solide sur panneau |
| Matière | **PETG** | tenue en température |
| Entrefer paroi | bossages, jamais à plat | convection + vibrations |
| Emplacement | **au plus court du Pi** | 5 V/10 A : la chute en ligne n'est pas anecdotique |

## 6. Ce qui bloque encore le dessin

**Mesures à relever sur le robot** (le plan Mean Well ne les donnera jamais) :

1. **Largeur utile du pan** entre montants — il faut ≥ 159 mm **plus** le dégagement pour
   visser le bornier — et **hauteur libre**.
2. **Épaisseur et nature du panneau** (CP, MDF, aggloméré) : fixe la vis à bois. Du MDF ne
   tient pas une vis dans le chant.
3. **Dégagement devant** l'alim, pour accéder au bornier une fois montée.

**À confirmer la pièce en main, à réception** (10 secondes chacun) :

4. Que les `2-M3` sont bien dans la **semelle** et non dans le capot (la vue de dessus
   montre le capot en pointillé, l'interprétation est probable mais pas certaine).
5. La **profondeur de vissage** admissible (§3).
6. Le hors-tout réel, tolérance ± 1 mm oblige.

**Règle du projet applicable** (`feedback-cao-verifier-le-reel`) : vue de montage validée par
David **avant** impression. Les trois erreurs CAO du 16/08 — carter jamais mesuré, trou
bouché, signe du référentiel — ont toutes été vues par l'œil humain, aucune par les asserts.

## 7. Câblage — pièges connus

### 7.1 ⚠️ Sans négociation USB-C PD, le Pi 5 se bride tout seul

Vérifié le 2026-09-12 sur le **white paper officiel** Raspberry Pi *« USB Power Delivery on
Raspberry Pi 5 »* (Release 1, 17/03/2026) et la page de documentation matérielle.

Quelle que soit la voie retenue (broches 5 V du GPIO, ou USB-C alimenté par une source sans
PD), **le Pi 5 ne peut pas savoir de quoi l'alimentation est capable**. Comportement
documenté, par défaut :

> « If USB PD is not present on the supply, the Raspberry Pi SBC will assume a 5V 3A supply
> by default. »

> « If a 5V 5A supply is not detected, Raspberry Pi SBCs automatically limit the total power
> available to the USB ports to 600mA (instead of 1.6A). USB booting is also disabled unless
> the power switch is deliberately pressed, and the desktop will show a warning message
> saying power is limited. »

**Ça nous concerne directement** : l'audio de Didier est en USB (carte C-Media vers la
mixette, micro). **600 mA pour l'ensemble des ports**, c'est le genre de plafond sous lequel
un périphérique décroche par intermittence — un symptôme qu'on mettrait des heures à
attribuer à l'alimentation plutôt qu'au logiciel.

**Remède officiel**, à appliquer le jour de la bascule (deux voies, l'une suffit) :

| Réglage | Où | Effet documenté |
|---|---|---|
| `PSU_MAX_CURRENT=5000` | EEPROM du bootloader (`rpi-eeprom-config`) | saute la négociation PD et assume une source 5 A |
| `usb_max_current_enable=1` | `config.txt` | autorise les ports USB à tirer 1,6 A au lieu de 600 mA |

Ici l'affirmation est **honnête** : le SD-50B-5 sort réellement 10 A. Le réglage ne ment pas
au firmware, il lui dit ce qu'il ne peut pas négocier. À la condition expresse que **le
câblage supporte ces 5 A** — c'est le câble qui devient le maillon faible, pas l'alim.

### 7.2 Tension : viser 5,1 V, mesurée au Pi

La documentation officielle donne **5,1 V** comme tension nominale (pas 5,0), et une
détection de sous-tension qui se déclenche **sous 4,63 V (± 5 %)**. Autrement dit, toute la
marge est consommée par la chute en ligne.

- Câble **court et de forte section** entre l'alim et le Pi.
- Régler la sortie du SD-50 (s'il porte bien un ajustement — **à vérifier sur la pièce**)
  pour lire **~5,1 V au connecteur du Pi, en charge**, jamais au bornier de l'alim.
- Contrôle après coup : `vcgencmd get_throttled` — bit 0 = sous-tension présente,
  bit 16 = sous-tension survenue depuis le démarrage. À relever **après** une séance, pas
  seulement au repos.

### 7.3 Ce qui n'est PAS documenté — à traiter comme un risque, pas comme un fait

La présence d'un **fusible réarmable sur les broches 5 V du GPIO du Pi 5** n'est
**documentée nulle part officiellement**. Les seules affirmations trouvées viennent des
forums Raspberry Pi, au conditionnel (« likely does not have a polyfuse » ; le Pi 4 aurait
supprimé le fusible du header). Le white paper mentionne bien l'alimentation par le GPIO
comme une option envisagée par des utilisateurs, mais **sans aucune consigne de protection**.

Conclusion pratique : entrer par le GPIO, c'est **se passer des protections d'entrée** sans
savoir précisément lesquelles. Puisque rien ne l'interdit ni ne le garantit, la prudence est
de **prévoir nous-mêmes la protection** (fusible et/ou TVS côté 5 V) plutôt que de parier sur
une protection interne dont personne ne peut citer la datasheet.

### 7.4 FG

Voir §3 : la broche 3 est la masse de **châssis**, pas le 0 V. Son raccordement se décide
avec le chantier ronflement en tête, pas par réflexe — c'est précisément un chemin de boucle
de masse. (Un isolateur audio à transformateurs est par ailleurs en stock, repère `c0331` de
`inventaire-stock.md`, si le problème se déplaçait vers la liaison audio.)
