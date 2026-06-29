from dataclasses import dataclass, field

from services.pdf_layout_reader import PageWord


@dataclass(slots=True, frozen=True)
class Diagram:
    code: str
    page: int
    mots: tuple[PageWord, ...]
    x_min: float = field(init=False)
    x_max: float = field(init=False)
    y_min: float = field(init=False)
    y_max: float = field(init=False)

    def __post_init__(self):
        mots = tuple(self.mots)
        object.__setattr__(self, "mots", mots)

        if mots:
            object.__setattr__(self, "x_min", min(mot.x0 for mot in mots))
            object.__setattr__(self, "x_max", max(mot.x1 for mot in mots))
            object.__setattr__(self, "y_min", min(mot.top for mot in mots))
            object.__setattr__(self, "y_max", max(mot.bottom for mot in mots))
        else:
            object.__setattr__(self, "x_min", 0.0)
            object.__setattr__(self, "x_max", 0.0)
            object.__setattr__(self, "y_min", 0.0)
            object.__setattr__(self, "y_max", 0.0)

    def __len__(self) -> int:
        return len(self.mots)

    @property
    def est_valide(self) -> bool:
        return bool(self.code and self.page > 0 and len(self.mots) > 0)

    @property
    def bbox(self) -> tuple[float, float, float, float]:
        """
        Retourne la boîte englobante du diagramme sous la forme :
        (x_min, y_min, x_max, y_max)
        """
        return (
            self.x_min,
            self.y_min,
            self.x_max,
            self.y_max,
        )

    def __str__(self) -> str:
        return (
            f"Diagram(code={self.code!r}, page={self.page}, "
            f"mots={len(self.mots)}, bounds=({self.x_min:.1f}, {self.y_min:.1f})-({self.x_max:.1f}, {self.y_max:.1f}))"
        )
