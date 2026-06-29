import re

from services.pdf_layout_reader import PageWord


class GeometryReader:

    HEURE = re.compile(r"^\d{1,2}:\d{2}(:\d{2})?$")

    def _chercher(
        self,
        mots: list[PageWord],
        page: int,
        x: float,
        y: float,
        texte: str,
        dx: float = 5,
        dy: float = 30,
    ):

        for mot in mots:

            if mot.page != page:
                continue

            if abs(mot.x0 - x) > dx:
                continue

            if abs(mot.top - y) > dy:
                continue

            if mot.text == texte:
                return mot

        return None

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

    def lire_book_on(
        self,
        mots: list[PageWord],
        page: int,
        top: float,
    ) -> str:

        mot = self._chercher(
            mots,
            page,
            82,
            top,
            "Book-on:",
            dx=10,
            dy=5,
        )

        if mot is None:
            return ""

        return self.premier_horaire_en_dessous(mots, mot)

    def lire_book_off(
        self,
        mots: list[PageWord],
        page: int,
        top: float,
    ) -> str:

        mot = self._chercher(
            mots,
            page,
            82,
            top + 25,
            "Book-off:",
            dx=10,
            dy=15,
        )

        if mot is None:
            return ""

        return self.premier_horaire_en_dessous(mots, mot)

    def lire_duration(
        self,
        mots: list[PageWord],
        page: int,
        top: float,
    ) -> str:

        mot = self._chercher(
            mots,
            page,
            686,
            top + 25,
            "Duration:",
            dx=10,
            dy=15,
        )

        if mot is None:
            return ""

        return self.premier_horaire_en_dessous(
            mots,
            mot,
            delta_x=10,
            delta_y=20,
        )

    def lire_effective(
        self,
        mots: list[PageWord],
        page: int,
        top: float,
    ) -> str:

        mot = self._chercher(
            mots,
            page,
            686,
            top + 40,
            "Effective",
            dx=10,
            dy=25,
        )

        if mot is None:
            return ""

        return self.premier_horaire_en_dessous(
            mots,
            mot,
            delta_x=10,
            delta_y=20,
        )