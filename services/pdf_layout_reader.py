from dataclasses import dataclass

import pdfplumber


@dataclass
class PageWord:
    text: str
    page: int
    x0: float
    x1: float
    top: float
    bottom: float


@dataclass
class PageLine:
    page: int
    top: float
    words: list[PageWord]

    @property
    def text(self) -> str:
        return " ".join(word.text for word in self.words)


def lire_mots(pdf_path: str) -> list[PageWord]:

    resultat = []

    with pdfplumber.open(pdf_path) as pdf:

        for numero_page, page in enumerate(pdf.pages, start=1):

            mots = page.extract_words(
                use_text_flow=True,
                keep_blank_chars=False,
            )

            for mot in mots:

                resultat.append(
                    PageWord(
                        text=mot["text"],
                        page=numero_page,
                        x0=mot["x0"],
                        x1=mot["x1"],
                        top=mot["top"],
                        bottom=mot["bottom"],
                    )
                )

    return resultat


def lire_lignes(pdf_path: str) -> list[PageLine]:

    mots = lire_mots(pdf_path)

    lignes = []

    courant = []

    page = None
    top = None

    for mot in mots:

        if (
            page != mot.page
            or top is None
            or abs(mot.top - top) > 2
        ):

            if courant:
                lignes.append(
                    PageLine(
                        page=page,
                        top=top,
                        words=courant,
                    )
                )

            courant = [mot]
            page = mot.page
            top = mot.top

        else:

            courant.append(mot)

    if courant:
        lignes.append(
            PageLine(
                page=page,
                top=top,
                words=courant,
            )
        )

    return lignes


def lire_catalogues(fichiers: list[str]) -> list[PageLine]:

    resultat = []

    for fichier in fichiers:
        resultat.extend(
            lire_lignes(fichier)
        )

    return resultat