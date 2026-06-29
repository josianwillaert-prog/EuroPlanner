import re

from services.pdf_layout_reader import PageWord


class GeometryReader:

    HEURE = re.compile(r"^\d{1,2}:\d{2}(:\d{2})?$")

    def premier_horaire_en_dessous(
        self,
        mots: list[PageWord],
        reference: PageWord,
        delta_x: float = 5,
        delta_y: float = 30,
    ) -> str:

        candidats = []

        for mot in mots:

            if mot.page != reference.page:
                continue

            if abs(mot.x0 - reference.x0) > delta_x:
                continue

            if mot.top <= reference.top:
                continue

            if mot.top - reference.top > delta_y:
                continue

            if self.HEURE.fullmatch(mot.text):

                candidats.append(mot)

        if not candidats:
            return ""

        candidats.sort(key=lambda m: m.top)

        return candidats[0].text