from dataclasses import dataclass, field

from models.page_column import PageColumn


@dataclass(slots=True)
class DiagramBlock:

    code: str = ""

    colonne: PageColumn | None = None

    lignes: list[str] = field(default_factory=list)

    def ajouter(self, texte: str):

        self.lignes.append(texte)

    @property
    def texte(self):

        return "\n".join(self.lignes)