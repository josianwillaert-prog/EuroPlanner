from dataclasses import dataclass

import pdfplumber


@dataclass(slots=True)
class PageWord:
    text: str
    page: int
    x0: float
    x1: float
    top: float
    bottom: float


@dataclass(slots=True)
class PageLine:
    page: int
    top: float
    bottom: float
    words: list[PageWord]

    @property
    def text(self) -> str:
        return " ".join(w.text for w in self.words)


def lire_mots(pdf_path: str) -> list[PageWord]:

    resultat = []

    with pdfplumber.open(pdf_path) as pdf:

        for numero_page, page in enumerate(pdf.pages, start=1):

            for mot in page.extract_words(
                use_text_flow=True,
                keep_blank_chars=False,
            ):

                resultat.append(
                    PageWord(
                        text=mot["text"],
                        page=numero_page,
                        x0=float(mot["x0"]),
                        x1=float(mot["x1"]),
                        top=float(mot["top"]),
                        bottom=float(mot["bottom"]),
                    )
                )

    return resultat


def regrouper_par_ligne(
    mots: list[PageWord],
    tolerance: float = 2.0,
) -> list[PageLine]:

    lignes = []

    for mot in sorted(
        mots,
        key=lambda m: (m.page, m.top, m.x0),
    ):

        if (
            not lignes
            or lignes[-1].page != mot.page
            or abs(lignes[-1].top - mot.top) > tolerance
        ):

            lignes.append(
                PageLine(
                    page=mot.page,
                    top=mot.top,
                    bottom=mot.bottom,
                    words=[mot],
                )
            )

        else:

            ligne = lignes[-1]

            ligne.words.append(mot)
            ligne.bottom = max(
                ligne.bottom,
                mot.bottom,
            )

    for ligne in lignes:
        ligne.words.sort(key=lambda m: m.x0)

    return lignes


def lire_lignes(pdf_path: str) -> list[PageLine]:

    return regrouper_par_ligne(
        lire_mots(pdf_path)
    )


def lire_catalogues(
    fichiers: list[str],
) -> list[PageLine]:

    lignes = []

    for fichier in fichiers:
        lignes.extend(
            lire_lignes(fichier)
        )

    return lignes