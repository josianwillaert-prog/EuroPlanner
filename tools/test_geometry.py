from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from services.geometry_reader import GeometryReader
from services.pdf_layout_reader import lire_mots

PDF = (
    Path(__file__).resolve().parent.parent
    / "catalogues"
    / "Catalogue JS DI.pdf"
)

mots = lire_mots(str(PDF))

reader = GeometryReader()

diagramme = "G837B"

book_on = None
book_off = None
duration = None

for mot in mots:

    if mot.text.upper() != diagramme:
        continue

    page = mot.page
    y = mot.top

    for m in mots:

        if m.page != page:
            continue

        if abs(m.top - y) > 40:
            continue

        if m.text == "Book-on:":
            book_on = m

        elif m.text == "Book-off:":
            book_off = m

        elif m.text == "Duration:":
            duration = m

    break

print("=" * 60)
print(diagramme)
print("=" * 60)

print("Book-on :", reader.premier_horaire_en_dessous(mots, book_on))
print("Book-off:", reader.premier_horaire_en_dessous(mots, book_off))
print("Duration:", reader.premier_horaire_en_dessous(mots, duration))