from pathlib import Path
import sys

# Ajoute la racine du projet au PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parent.parent))

from services.diagram_locator import DiagramLocator
from services.pdf_layout_reader import lire_mots

PDF = "catalogues/Catalogue JS DI(2).pdf"

mots = lire_mots(PDF)

locator = DiagramLocator()

diagrammes = locator.locate(mots)

print(f"{len(diagrammes)} diagrammes trouvés\n")

for d in diagrammes:
    print(d)