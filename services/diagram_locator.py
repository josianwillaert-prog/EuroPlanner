import re

from services.pdf_layout_reader import PageWord


class DiagramLocation:

    def __init__(
        self,
        code: str,
        page: int,
        top: float,
        bottom: float,
        x0: float,
        x1: float,
    ):
        self.code = code
        self.page = page
        self.top = top
        self.bottom = bottom
        self.x0 = x0
        self.x1 = x1

    def __repr__(self):

        return (
            f"{self.code}"
            f" page={self.page}"
            f" y={self.top:.1f}"
        )


class DiagramLocator:

    REGEX = re.compile(r"^[JG]\d{3}[ABab]?$")

    def locate(
        self,
        mots: list[PageWord],
    ) -> list[DiagramLocation]:

        resultat = []

        for mot in mots:

            texte = mot.text.upper()

            if not self.REGEX.fullmatch(texte):
                continue

            resultat.append(
                DiagramLocation(
                    code=texte,
                    page=mot.page,
                    top=mot.top,
                    bottom=mot.bottom,
                    x0=mot.x0,
                    x1=mot.x1,
                )
            )

        resultat.sort(
            key=lambda d: (
                d.page,
                d.top,
                d.x0,
            )
        )

        return resultat