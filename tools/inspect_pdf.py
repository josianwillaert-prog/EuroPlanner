from pathlib import Path
import sys

# Ajoute la racine du projet au PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parent.parent))

from services.pdf_layout_reader import lire_mots

# Catalogue à analyser
PDF = (
    Path(__file__).resolve().parent.parent
    / "catalogues"
    / "Catalogue JS DI.pdf"
)

CODE = "G837B"

mots = lire_mots(str(PDF))

trouve = False

for mot in mots:

    if mot.text.upper() != CODE:
        continue

    trouve = True

    print("=" * 100)
    print(f"Diagramme : {mot.text}")
    print(f"Page : {mot.page}")
    print(f"x = {mot.x0:.1f}")
    print(f"y = {mot.top:.1f}")
    print("=" * 100)
    print()

    voisins = []

    for voisin in mots:

        if voisin.page != mot.page:
            continue

        # Affiche tous les mots dans une bande verticale de ±120 points
        if abs(voisin.top - mot.top) <= 300:

            voisins.append(voisin)

    voisins.sort(key=lambda w: (w.top, w.x0))

    for v in voisins:

        print(
            f"{v.top:7.1f}  "
            f"{v.x0:7.1f}  "
            f"{v.text}"
        )

if not trouve:
    print(f"{CODE} introuvable.")