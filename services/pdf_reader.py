import pdfplumber


def lire_pdf(chemin_pdf: str) -> list[str]:
    """
    Lit un catalogue PDF et renvoie le texte de chaque page.

    Retour :
        [
            "texte page 1",
            "texte page 2",
            ...
        ]
    """

    pages = []

    with pdfplumber.open(chemin_pdf) as pdf:

        for page in pdf.pages:

            texte = page.extract_text()

            if texte is None:
                texte = ""

            pages.append(texte)

    return pages


def lire_catalogues(fichiers: list[str]) -> list[str]:
    """
    Lit plusieurs catalogues.

    Retour :
        [
            texte page 1 catalogue A,
            texte page 2 catalogue A,
            texte page 1 catalogue B,
            ...
        ]
    """

    resultat = []

    for fichier in fichiers:

        resultat.extend(
            lire_pdf(fichier)
        )

    return resultat