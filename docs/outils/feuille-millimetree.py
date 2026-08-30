#!/usr/bin/env python3
"""Génère une feuille millimétrée PDF à imprimer, pour photographier du matériel
avec une échelle lisible (mesurer une pièce a posteriori sur la photo).

Aucune dépendance : le PDF est écrit à la main (vectoriel, donc net à
n'importe quelle imprimante, contrairement à une image tramée).

Usage :
    python3 feuille-millimetree.py                       # A4 portrait + paysage
    python3 feuille-millimetree.py --format A3 --orientation paysage
    python3 feuille-millimetree.py --couleur gris        # au lieu du bleu

PIÈGE D'IMPRESSION : imprimer à *taille réelle / 100 %*, JAMAIS « ajuster à la
page » (le pilote réduit de ~4 % pour rentrer dans les marges, et le
millimétrage devient faux sans qu'on le voie). La barre témoin de 100 mm en bas
de page sert à vérifier au réglet avant de photographier quoi que ce soit.
"""

from __future__ import annotations

import argparse
from pathlib import Path

# --- Unités -----------------------------------------------------------------
# Le PDF raisonne en points typographiques (1 pt = 1/72 pouce). Tout le reste du
# script raisonne en millimètres : une seule conversion, au moment d'écrire.
MM = 72.0 / 25.4

# Formats papier en mm (largeur, hauteur) en portrait.
FORMATS = {
    "A5": (148.0, 210.0),
    "A4": (210.0, 297.0),
    "A3": (297.0, 420.0),
}

# Marge non imprimable : la plupart des imprimantes domestiques ne descendent
# pas sous ~5 mm. On prend 8 mm, puis on recale la grille sur un multiple de
# 10 mm pour que les graduations tombent rond.
MARGE_MM = 8.0

# Palettes (r, g, b) pour les traits 1 mm / 5 mm / 10 mm.
# Le bleu est le classique du papier millimétré : il se distingue bien du
# matériel photographié (souvent noir, gris ou métal) sans manger le contraste.
# Le 1 mm est volontairement TRÈS clair : trop appuyé, il noie le pas de 5 mm et
# la feuille devient illisible sur une photo.
PALETTES = {
    "bleu": ((0.80, 0.87, 0.95), (0.50, 0.66, 0.86), (0.13, 0.35, 0.66)),
    "gris": ((0.85, 0.85, 0.85), (0.60, 0.60, 0.60), (0.25, 0.25, 0.25)),
}

# Épaisseurs de trait en points. En dessous de ~0.15 pt, un jet d'encre laisse
# des traits fantômes : 0.18 est le plancher pratique pour le pas de 1 mm.
EP_1MM, EP_5MM, EP_10MM = 0.18, 0.4, 0.7

# Côté des mires de coin, en mm.
MIRE_MM = 4.0


def flottant(valeur: float) -> str:
    """Formate un nombre pour le PDF (3 décimales, sans zéros inutiles)."""
    return f"{valeur:.3f}".rstrip("0").rstrip(".") or "0"


def echappe(texte: str) -> str:
    """Échappe une chaîne pour un littéral PDF ( ... ), encodé cp1252."""
    return texte.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")


def construit_page(largeur_mm: float, hauteur_mm: float, palette: str) -> str:
    """Retourne le flux de contenu PDF d'une page millimétrée.

    Repère PDF : origine en bas à gauche, y vers le haut — c'est aussi le repère
    utilisé ici, donc les graduations verticales se lisent de bas en haut.
    """
    c_1mm, c_5mm, c_10mm = PALETTES[palette]
    ops: list[str] = []

    # Zone quadrillée : on part des marges, puis on arrondit vers l'intérieur au
    # multiple de 10 mm le plus proche. Ainsi la grille commence et finit sur une
    # graduation entière — indispensable pour lire une cote sur la photo.
    x0 = MARGE_MM + (-MARGE_MM % 10)
    y0 = MARGE_MM + (-MARGE_MM % 10)
    x1 = x0 + int((largeur_mm - MARGE_MM - x0) // 10) * 10
    y1 = y0 + int((hauteur_mm - MARGE_MM - y0) // 10) * 10
    # Cartouche du bas (barre témoin + consignes). Les consignes tiennent à
    # droite de la barre sur A4/A3 ; sur un format étroit elles passent dessous,
    # ce qui demande une réserve plus haute — sinon elles sortiraient de la
    # feuille sans qu'on le voie au moment du tirage.
    a_droite = (x1 - (x0 + 104)) >= 72.0
    y0 += 12 if a_droite else 18

    def trace(groupes: list[tuple[float, float, float, float]],
              couleur: tuple[float, float, float], epaisseur: float) -> None:
        if not groupes:
            return
        r, v, b = couleur
        ops.append(f"{flottant(r)} {flottant(v)} {flottant(b)} RG")
        ops.append(f"{flottant(epaisseur)} w")
        for xa, ya, xb, yb in groupes:
            ops.append(
                f"{flottant(xa * MM)} {flottant(ya * MM)} m "
                f"{flottant(xb * MM)} {flottant(yb * MM)} l"
            )
        ops.append("S")

    # Trois passes, du plus clair au plus foncé : le trait fort doit être tracé
    # PAR-DESSUS le trait fin, sinon les fins bavent sur les décimétriques.
    for pas, couleur, epaisseur in (
        (1, c_1mm, EP_1MM),
        (5, c_5mm, EP_5MM),
        (10, c_10mm, EP_10MM),
    ):
        verticales = [
            (x0 + i, y0, x0 + i, y1)
            for i in range(0, int(x1 - x0) + 1, pas)
            # Une ligne appartient au pas le plus grand qui la contient : on
            # saute ici celles qui seront (re)tracées par une passe plus foncée.
            if pas == 10 or (x0 + i) % (pas * 5 if pas == 1 else 10) != 0
        ]
        horizontales = [
            (x0, y0 + i, x1, y0 + i)
            for i in range(0, int(y1 - y0) + 1, pas)
            if pas == 10 or (y0 + i) % (pas * 5 if pas == 1 else 10) != 0
        ]
        trace(verticales + horizontales, couleur, epaisseur)

    # --- Graduations chiffrées (en cm) --------------------------------------
    # Numéroter tous les cm rend la lecture directe sur la photo, sans compter
    # les carreaux. Origine (0,0) = coin bas-gauche de la grille.
    ops.append("BT")
    ops.append("/F1 5 Tf")
    r, v, b = c_10mm
    ops.append(f"{flottant(r)} {flottant(v)} {flottant(b)} rg")

    def etiquette(x_mm: float, y_mm: float, texte: str) -> None:
        ops.append(f"1 0 0 1 {flottant(x_mm * MM)} {flottant(y_mm * MM)} Tm")
        ops.append(f"({echappe(texte)}) Tj")

    # Aux quatre extrémités, l'étiquette tomberait sous une mire de coin : on la
    # décale VERS L'INTÉRIEUR de la grille. Sans ça, le « 0 » — l'origine, donc
    # la graduation la plus utile — disparaît sous le carré noir.
    largeur_cm, hauteur_cm = int(x1 - x0) // 10, int(y1 - y0) // 10
    for i in range(0, largeur_cm + 1):
        decalage = 0.8 if i == 0 else (-3.2 if i == largeur_cm else -1.2)
        for y_txt in (y0 - 3.6, y1 + 1.4):
            etiquette(x0 + i * 10 + decalage, y_txt, str(i))
    for i in range(0, hauteur_cm + 1):
        decalage = 0.8 if i == 0 else (-2.6 if i == hauteur_cm else -0.8)
        etiquette(x0 - 5.0, y0 + i * 10 + decalage, str(i))
        etiquette(x1 + 1.4, y0 + i * 10 + decalage, str(i))
    ops.append("ET")

    # --- Mires de coin -------------------------------------------------------
    # Quatre carrés noirs pleins aux angles de la grille, posés À L'EXTÉRIEUR
    # (leur coin intérieur EST le coin de grille) : ils donnent 4 points de
    # référence à distance connue pour redresser la perspective d'une photo
    # prise de biais, sans recouvrir un seul carreau.
    ops.append("0 0 0 rg")
    for cx, sx in ((x0, -1), (x1, 1)):
        for cy, sy in ((y0, -1), (y1, 1)):
            ops.append(
                f"{flottant(min(cx, cx + sx * MIRE_MM) * MM)} "
                f"{flottant(min(cy, cy + sy * MIRE_MM) * MM)} "
                f"{flottant(MIRE_MM * MM)} {flottant(MIRE_MM * MM)} re f"
            )

    # --- Cartouche bas de page : témoin d'échelle + consigne ----------------
    ty = MARGE_MM + (6.0 if a_droite else 12.0)  # ligne de la barre témoin
    ops.append("0 0 0 RG")
    ops.append("0.8 w")
    # Barre de 100 mm avec ses embouts : à mesurer au réglet après impression.
    ops.append(
        f"{flottant(x0 * MM)} {flottant(ty * MM)} m "
        f"{flottant((x0 + 100) * MM)} {flottant(ty * MM)} l S"
    )
    for x_emb in (x0, x0 + 50, x0 + 100):
        ops.append(
            f"{flottant(x_emb * MM)} {flottant((ty - 1.5) * MM)} m "
            f"{flottant(x_emb * MM)} {flottant((ty + 1.5) * MM)} l S"
        )
    # Trois lignes empilées : à droite de la barre si la largeur le permet,
    # sinon dessous. Tout doit rester entre la marge basse et la première
    # graduation, faute de quoi le texte chevaucherait les chiffres de l'axe.
    tx = (x0 + 104) if a_droite else x0
    # Ancré sur le BAS DE GRILLE (et non sur la barre) : à droite, le texte
    # partage sa bande horizontale avec les chiffres de l'axe X, il doit donc
    # rester sous leur ligne de base — 5.8 mm suffisent pour du 6 pt.
    base = (y0 - 6.6) if a_droite else (ty - 4.0)

    ops.append("BT")
    ops.append("/F1 6 Tf")
    ops.append("0 0 0 rg")
    ops.append(f"1 0 0 1 {flottant(tx * MM)} {flottant(base * MM)} Tm")
    ops.append(
        f"({echappe('Témoin : cette barre doit mesurer 100 mm au réglet.')}) Tj"
    )
    ops.append(f"1 0 0 1 {flottant(tx * MM)} {flottant((base - 3.2) * MM)} Tm")
    ops.append(
        f"({echappe('Sinon : imprimer à 100 % (taille réelle), pas « ajuster à la page ».')}) Tj"
    )
    # Dimensions hors-tout de la grille : utile pour recaler une photo dont les
    # bords sont coupés, ou pour contrôler une correction de perspective.
    ops.append("/F1 5 Tf")
    ops.append("0.45 0.45 0.45 rg")
    ops.append(f"1 0 0 1 {flottant(tx * MM)} {flottant((base - 6.4) * MM)} Tm")
    ops.append(
        f"({echappe(f'Grille {int(x1 - x0)} × {int(y1 - y0)} mm entre mires, pas de 1 mm.')}) Tj"
    )
    ops.append("ET")

    return "\n".join(ops)


def ecrit_pdf(chemin: Path, pages: list[tuple[float, float, str]]) -> None:
    """Écrit un PDF multi-pages.

    `pages` = liste de (largeur_mm, hauteur_mm, flux_de_contenu).

    PIÈGE : la table xref doit contenir l'offset EXACT de chaque objet en octets.
    On construit donc le fichier en bytes au fur et à mesure en relevant les
    positions ; toute écriture « en deux temps » désynchroniserait les offsets et
    produirait un PDF refusé par les visionneuses strictes.
    """
    objets: list[bytes] = []

    def ajoute(corps: str) -> int:
        objets.append(corps.encode("cp1252"))
        return len(objets)  # numéro d'objet (1-indexé)

    # Objet 1 = catalogue, objet 2 = arbre des pages : numéros réservés d'avance
    # car les pages doivent référencer leur parent (2) avant qu'il n'existe.
    objets.append(b"")  # placeholder catalogue
    objets.append(b"")  # placeholder pages
    police = ajoute(
        # WinAnsiEncoding (≡ cp1252) : sans elle, la police Type1 de base
        # utilise StandardEncoding, où les accents français n'existent pas.
        "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica "
        "/Encoding /WinAnsiEncoding >>"
    )

    refs_pages: list[int] = []
    for largeur_mm, hauteur_mm, contenu in pages:
        flux = contenu.encode("cp1252")
        num_flux = ajoute(
            f"<< /Length {len(flux)} >>\nstream\n{contenu}\nendstream"
        )
        num_page = ajoute(
            "<< /Type /Page /Parent 2 0 R "
            f"/MediaBox [0 0 {flottant(largeur_mm * MM)} {flottant(hauteur_mm * MM)}] "
            f"/Resources << /Font << /F1 {police} 0 R >> >> "
            f"/Contents {num_flux} 0 R >>"
        )
        refs_pages.append(num_page)

    kids = " ".join(f"{n} 0 R" for n in refs_pages)
    objets[0] = b"<< /Type /Catalog /Pages 2 0 R >>"
    objets[1] = (
        f"<< /Type /Pages /Count {len(refs_pages)} /Kids [{kids}] >>"
    ).encode("cp1252")

    sortie = bytearray(b"%PDF-1.4\n")
    offsets: list[int] = []
    for numero, corps in enumerate(objets, start=1):
        offsets.append(len(sortie))
        sortie += f"{numero} 0 obj\n".encode("cp1252") + corps + b"\nendobj\n"

    depart_xref = len(sortie)
    sortie += f"xref\n0 {len(objets) + 1}\n".encode("cp1252")
    sortie += b"0000000000 65535 f \n"
    for offset in offsets:
        sortie += f"{offset:010d} 00000 n \n".encode("cp1252")
    sortie += (
        f"trailer\n<< /Size {len(objets) + 1} /Root 1 0 R >>\n"
        f"startxref\n{depart_xref}\n%%EOF\n"
    ).encode("cp1252")

    chemin.write_bytes(sortie)


def main() -> None:
    parseur = argparse.ArgumentParser(description=__doc__)
    parseur.add_argument("--format", default="A4", choices=sorted(FORMATS))
    parseur.add_argument(
        "--orientation", default="les-deux",
        choices=("portrait", "paysage", "les-deux"),
    )
    parseur.add_argument("--couleur", default="bleu", choices=sorted(PALETTES))
    parseur.add_argument(
        "--sortie", type=Path, default=None,
        help="chemin du PDF (défaut : à côté du script)",
    )
    args = parseur.parse_args()

    largeur, hauteur = FORMATS[args.format]
    orientations = (
        ["portrait", "paysage"] if args.orientation == "les-deux"
        else [args.orientation]
    )
    pages = [
        (largeur, hauteur, construit_page(largeur, hauteur, args.couleur))
        if sens == "portrait"
        else (hauteur, largeur, construit_page(hauteur, largeur, args.couleur))
        for sens in orientations
    ]

    sortie = args.sortie or (
        Path(__file__).parent / f"feuille-millimetree-{args.format}.pdf"
    )
    ecrit_pdf(sortie, pages)
    print(f"{sortie} — {len(pages)} page(s), {args.format} {args.couleur}")


if __name__ == "__main__":
    main()
