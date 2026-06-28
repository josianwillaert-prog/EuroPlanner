from dataclasses import dataclass, field

from services.pdf_layout_reader import PageWord


@dataclass(slots=True)
class PageColumn:

    page: int

    x0: float
    x1: float

    words: list[PageWord] = field(default_factory=list)

    def ajouter(self, mot: PageWord):

        self.words.append(mot)

        self.x0 = min(self.x0, mot.x0)
        self.x1 = max(self.x1, mot.x1)

    @property
    def texte(self):

        return "\n".join(
            mot.text
            for mot in sorted(
                self.words,
                key=lambda m: (m.top, m.x0),
            )
        )