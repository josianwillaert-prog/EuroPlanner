from services.pdf_layout_reader import PageLine


class DiagramBlockExtractor:

    def extraire(self, lignes: list[PageLine]) -> list[str]:

        blocs = []

        courant = []

        dans_diagramme = False

        for ligne in lignes:

            texte = ligne.text.strip()

            if texte.startswith("Nr diagram:"):

                if courant:
                    blocs.append("\n".join(courant))

                courant = [texte]
                dans_diagramme = True
                continue

            if not dans_diagramme:
                continue

            if texte.startswith("0 1 2 3 4"):
                blocs.append("\n".join(courant))
                courant = []
                dans_diagramme = False
                continue

            courant.append(texte)

        if courant:
            blocs.append("\n".join(courant))

        return blocs