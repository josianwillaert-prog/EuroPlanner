from models.journee_service import JourneeService

from services.pdf_layout_reader import lire_catalogues
from services.diagram_parser import analyser_pdf


class CatalogueService:

    def __init__(self):
        self.journees: dict[str, JourneeService] = {}

    def charger(self, fichiers: list[str]) -> None:

        self.journees.clear()

        lignes = lire_catalogues(fichiers)

        self.journees = analyser_pdf(lignes)

    def get(self, code: str) -> JourneeService | None:

        return self.journees.get(code.upper())

    def contient(self, code: str) -> bool:

        return code.upper() in self.journees

    def __len__(self):

        return len(self.journees)

    def __contains__(self, code: str):

        return self.contient(code)