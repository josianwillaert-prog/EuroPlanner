import re

from models.journee_service import JourneeService
from services.pdf_layout_reader import (
    lire_mots,
    lire_lignes,
)


class Catalogue:

    def __init__(self, chemin_pdf: str):

        self.chemin_pdf = chemin_pdf

        self.mots = lire_mots(chemin_pdf)
        self.lignes = lire_lignes(chemin_pdf)

        self.journees: dict[str, JourneeService] = {}

        self._analyser()

    def _analyser(self):

        bloc = []

        for ligne in self.lignes:

            if ligne.text.startswith("Nr diagram:"):

                self._analyser_bloc(bloc)
                bloc = []

            bloc.append(ligne.text)

        self._analyser_bloc(bloc)

    def _analyser_bloc(self, lignes: list[str]):

        if not lignes:
            return

        texte = "\n".join(lignes)

        m = re.search(r"([JG]\d{3}[ab]?)", texte)

        if not m:
            return

        code = m.group(1).upper()

        journee = JourneeService(code=code)

        m = re.search(r"Book-on:\s*([0-9]{1,2}:[0-9]{2})", texte)
        if m:
            journee.prise = m.group(1)

        m = re.search(r"Book-off:\s*([0-9]{1,2}:[0-9]{2})", texte)
        if m:
            journee.fin = m.group(1)

        m = re.search(r"Duration:\s*([0-9:]+)", texte)
        if m:
            journee.duree = m.group(1)

        texte = texte.replace("Ef f ectiv e", "Effective")

        m = re.search(
            r"Effective working time:\s*([0-9:]+)",
            texte,
        )
        if m:
            journee.travail = m.group(1)

        if "Out of home" in texte:

            journee.decoucher = True

            m = re.search(
                r"Out of home (?:start|end):\s*([JG]\d{3}[ab]?)",
                texte,
            )

            if m:
                journee.code_decoucher = m.group(1).upper()

        self.journees[code] = journee

    def get(self, code: str):

        return self.journees.get(code.upper())

    def __getitem__(self, code: str):

        return self.journees[code.upper()]

    def __contains__(self, code: str):

        return code.upper() in self.journees

    def __len__(self):

        return len(self.journees)