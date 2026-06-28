import sys

import pdfplumber


def afficher_diagramme(pdf_path, code):

    with pdfplumber.open(pdf_path) as pdf:

        for numero_page, page in enumerate(pdf.pages, start=1):

            mots = page.extract_words(
                use_text_flow=True,
                keep_blank_chars=False,
            )

            debut = None

            for i, mot in enumerate(mots):

                if (
                    mot["text"] == code
                    and i >= 2
                    and mots[i - 2]["text"] == "Nr"
                    and mots[i - 1]["text"] == "diagram:"
                ):
                    debut = i - 2
                    break

            if debut is None:
                continue

            fin = len(mots)

            for j in range(debut + 1, len(mots) - 2):

                if (
                    mots[j]["text"] == "Nr"
                    and mots[j + 1]["text"] == "diagram:"
                ):
                    fin = j
                    break

            print("=" * 80)
            print(f"Diagramme {code}")
            print(f"Page {numero_page}")
            print("=" * 80)

            for mot in mots[debut:fin]:

                print(
                    f'{mot["text"]:<18}'
                    f'x={mot["x0"]:>7.1f} '
                    f'y={mot["top"]:>7.1f}'
                )

            return

    print("Diagramme introuvable.")


if __name__ == "__main__":

    if len(sys.argv) != 3:

        print("Usage :")
        print(
            "python tools/debug_pdf.py "
            '"catalogues/Catalogue JS LU.pdf" J491a'
        )
        sys.exit()

    afficher_diagramme(
        sys.argv[1],
        sys.argv[2],
    )