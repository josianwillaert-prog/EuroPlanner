import re

from models.journee_service import JourneeService
from services.pdf_layout_reader import PageLine


def analyser_pdf(lignes: list[PageLine]) -> dict[str, JourneeService]:
    """
    Analyse les lignes d'un ou plusieurs catalogues PDF.
    Retourne un dictionnaire indexé par code de journée.
    """

    catalogue = {}

    bloc = []

    def analyser_bloc(bloc_lignes: list[str]):

        if not bloc_lignes:
            return

        texte = "\n".join(bloc_lignes)

        m = re.search(r"([JG]\d{3}[ab]?)", texte)

        if not m:
            return

        code = m.group(1).upper()

        prise = ""
        fin = ""
        duree = ""
        travail = ""
        decoucher = False
        code_decoucher = ""

        m = re.search(r"Book-on:\s*([0-9]{1,2}:[0-9]{2})", texte)
        if m:
            prise = m.group(1)

        m = re.search(r"Book-off:\s*([0-9]{1,2}:[0-9]{2})", texte)
        if m:
            fin = m.group(1)

        m = re.search(r"Duration:\s*([0-9:]+)", texte)
        if m:
            duree = m.group(1)

        m = re.search(
            r"Effective working time:\s*([0-9:]+)",
            texte.replace("Ef f ectiv e", "Effective"),
        )
        if m:
            travail = m.group(1)

        if "Out of home" in texte:
            decoucher = True

            m = re.search(
                r"Out of home (?:start|end):\s*([JG]\d{3}[ab]?)",
                texte,
            )

            if m:
                code_decoucher = m.group(1).upper()

        catalogue[code] = JourneeService(
            code=code,
            prise=prise,
            fin=fin,
            duree=duree,
            travail=travail,
            decoucher=decoucher,
            code_decoucher=code_decoucher,
        )

    for ligne in lignes:

        texte = ligne.text

        if texte.startswith("Nr diagram:"):

            analyser_bloc(bloc)
            bloc = []

        bloc.append(texte)

    analyser_bloc(bloc)

    return catalogue