from models.catalogue import Catalogue
from services.ics_generator import generer_ics

catalogue = Catalogue("catalogues/C2 - Je.PDF")

planning = [
    ("27/07/2026", "J301a"),
    ("28/07/2026", "J321a"),
    ("29/07/2026", "J481a"),
]

generer_ics(planning, catalogue)