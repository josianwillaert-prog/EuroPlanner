from services.pdf_layout_reader import (
    lire_mots,
    lire_lignes,
)

from services.diagram_block_extractor import (
    DiagramBlockExtractor,
)

from services.diagram_locator import (
    DiagramLocator,
)

from services.diagram_parser import (
    DiagramParser,
)


class Catalogue:

    def __init__(self, chemin_pdf: str):

        self.chemin_pdf = chemin_pdf

        self.mots = lire_mots(chemin_pdf)
        self.lignes = lire_lignes(chemin_pdf)

        self.journees = {}

        self._charger()

    def _charger(self):

        self.journees = self._charger_par_blocs(
            self.mots,
            self.lignes,
        )

    def _charger_par_blocs(self, mots, lignes):

        locator = DiagramLocator()
        extracteur = DiagramBlockExtractor()
        parser = DiagramParser()

        diagrammes = locator.locate(mots)
        blocs = extracteur.extraire(
            lignes
        )

        print(
            f"Diagrammes trouvés : {len(diagrammes)}"
        )
        print(
            f"Blocs trouvés : {len(blocs)}"
        )

        if len(diagrammes) != len(blocs):
            print(
                "Attention : nombre de diagrammes et de blocs différent"
            )

        journees = {}

        for bloc in blocs:

            journee = parser.parse(bloc)

            if journee is not None:

                journees[
                    journee.code
                ] = journee

        return journees

    def get(self, code: str):

        return self.journees.get(
            code.upper()
        )

    def __getitem__(self, code: str):

        return self.journees[
            code.upper()
        ]

    def __contains__(self, code: str):

        return (
            code.upper()
            in self.journees
        )

    def __len__(self):

        return len(self.journees)

    def values(self):

        return self.journees.values()