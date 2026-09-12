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

- **Chute de tension** : le Pi 5 passe en sous-tension bien avant 5 V. Câble **court et de
  forte section**, et réglage de la sortie **mesuré au connecteur du Pi**, pas au bornier de
  l'alim. (Présence d'un ajustement de sortie sur le SD-50 : à vérifier sur la pièce.)
- **Alimenter un Pi 5 hors USB-C PD** a des conséquences documentées par la fondation
  (bridage des ports USB, protections contournées si on passe par le GPIO) — *section à
  compléter, vérification en cours.*
- **FG** : voir §3, à trancher avec le chantier ronflement en tête.
