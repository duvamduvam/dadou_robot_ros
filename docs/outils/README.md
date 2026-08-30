# Outils d'atelier

Petits utilitaires hors robot, utiles pour documenter le matériel.

## Feuille millimétrée (photos de matériel)

Fond quadrillé à imprimer pour photographier une pièce, une carte ou un
connecteur **avec une échelle** : on peut relire une cote sur la photo des mois
plus tard, sans avoir à ressortir la pièce.

- `feuille-millimetree-A4.pdf` — A4, page 1 portrait (grille 190 × 258 mm),
  page 2 paysage (270 × 178 mm).
- `feuille-millimetree-A3.pdf` — idem en A3, pour les grosses pièces.
- `feuille-millimetree.py` — le générateur (Python 3, aucune dépendance).

### Impression — le seul piège

**Imprimer à « taille réelle » / 100 %, jamais « ajuster à la page ».** Le
pilote réduit sinon de ~4 % pour rentrer dans les marges, et le millimétrage
devient faux *sans que rien ne le signale*. D'où la barre témoin en bas de
page : elle doit mesurer exactement 100 mm au réglet. Si ce n'est pas le cas,
la feuille est bonne à jeter.

### Protocole photo

1. Poser la pièce sur la feuille, à plat, sans masquer les 4 mires noires.
2. Photographier **à l'aplomb** (l'appareil au-dessus du centre) : une prise de
   biais fausse les distances lues, la grille sert alors seulement à corriger.
3. Les 4 mires sont des points de référence à distance connue (rappelée en bas
   de page) : elles permettent de redresser la perspective a posteriori.
4. Lumière rasante = ombres portées qui décalent les bords apparents ;
   préférer un éclairage diffus.

### Régénérer / adapter

```bash
python3 feuille-millimetree.py                          # A4 portrait + paysage
python3 feuille-millimetree.py --format A3              # A3
python3 feuille-millimetree.py --format A5 --orientation portrait
python3 feuille-millimetree.py --couleur gris           # au lieu du bleu
python3 feuille-millimetree.py --sortie /tmp/essai.pdf
```

Le PDF est vectoriel (écrit octet par octet, sans bibliothèque) : il reste net
à n'importe quelle résolution d'imprimante. Les réglages fins — marge,
palettes, épaisseurs de trait, taille des mires — sont des constantes en tête
du script, chacune commentée avec la contrainte qui l'a fixée.
