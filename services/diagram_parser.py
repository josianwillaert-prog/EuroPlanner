import re

from models.journee_service import JourneeService


class DiagramParser:

    def parse(self, texte: str) -> JourneeService | None:

        m = re.search(r"([JG]\d{3}[ab]?)", texte)

        if not m:
            return None

        journee = JourneeService(
            code=m.group(1).upper()
        )

        m = re.search(
            r"Book-on:\s*([0-9]{1,2}:[0-9]{2})",
            texte,
        )
        if m:
            journee.prise = m.group(1)

        m = re.search(
            r"Book-off:\s*([0-9]{1,2}:[0-9]{2})",
            texte,
        )
        if m:
            journee.fin = m.group(1)

        m = re.search(
            r"Duration:\s*([0-9:]+)",
            texte,
        )
        if m:
            journee.duree = m.group(1)

        texte = texte.replace(
            "Ef f ectiv e",
            "Effective",
        )

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
                journee.code_decoucher = (
                    m.group(1).upper()
                )

        return journee