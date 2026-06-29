from models.page_column import PageColumn


class ColumnParser:

    def __init__(self, mots):

        self.mots = mots

    def extraire(self, tolerance=20):

        colonnes = []

        for mot in sorted(
            self.mots,
            key=lambda m: (m.page, m.x0, m.top),
        ):

            trouve = False

            for colonne in colonnes:

                if (
                    colonne.page == mot.page
                    and abs(colonne.x0 - mot.x0) < tolerance
                ):

                    colonne.ajouter(mot)
                    trouve = True
                    break

            if not trouve:

                colonnes.append(
                    PageColumn(
                        page=mot.page,
                        x0=mot.x0,
                        x1=mot.x1,
                        words=[mot],
                    )
                )

        return sorted(
            colonnes,
            key=lambda c: (c.page, c.x0),
        )