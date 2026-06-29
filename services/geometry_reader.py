import re
from typing import List, Pattern, Union

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

    def premier_horaire_a_droite(
        self,
        mots: list[PageWord],
        reference: PageWord,
        delta_y: float = 15,
    ) -> str:

        candidats: list[PageWord] = []

        for mot in mots:

            if mot.page != reference.page:
                continue

            if mot.x0 <= reference.x1:
                continue

            if abs(mot.top - reference.top) > delta_y:
                continue

            if self.HEURE.fullmatch(mot.text):

                candidats.append(mot)

        if not candidats:
            return ""

        candidats.sort(key=lambda m: (m.x0, abs(m.top - reference.top)))

        return candidats[0].text

    def premier_texte_a_droite(
        self,
        mots: list[PageWord],
        reference: PageWord,
        delta_y: float = 15,
    ) -> str:

        candidats: list[PageWord] = []

        for mot in mots:

            if mot.page != reference.page:
                continue

            if mot.x0 <= reference.x1:
                continue

            if abs(mot.top - reference.top) > delta_y:
                continue

            candidats.append(mot)

        if not candidats:
            return ""

        candidats.sort(key=lambda m: (m.x0, abs(m.top - reference.top)))

        return candidats[0].text

    def premier_mot_regex(
        self,
        mots: list[PageWord],
        reference: PageWord,
        motif: Union[Pattern[str], str],
        delta_y: float = 30,
    ) -> str:

        regex = motif if isinstance(motif, re.Pattern) else re.compile(motif)

        candidats: list[PageWord] = []

        for mot in mots:

            if mot.page != reference.page:
                continue

            if mot.top < reference.top:
                continue

            if mot.top == reference.top and mot.x0 <= reference.x1:
                continue

            if abs(mot.top - reference.top) > delta_y:
                continue

            if regex.search(mot.text):
                candidats.append(mot)

        if not candidats:
            return ""

        candidats.sort(key=lambda m: (m.top, m.x0))

        return candidats[0].text

    def mots_dans_rectangle(
        self,
        mots: list[PageWord],
        page: int,
        x0: float,
        y0: float,
        x1: float,
        y1: float,
    ) -> List[PageWord]:

        resultat: list[PageWord] = []

        for mot in mots:

            if mot.page != page:
                continue

            if mot.x0 < x0:
                continue

            if mot.x1 > x1:
                continue

            if mot.top < y0:
                continue

            if mot.bottom > y1:
                continue

            resultat.append(mot)

        resultat.sort(key=lambda m: (m.top, m.x0))

        return resultat