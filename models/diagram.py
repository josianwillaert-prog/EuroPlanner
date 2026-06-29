from dataclasses import dataclass, field

from services.pdf_layout_reader import PageWord
from typing import Optional, List
import re


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

        # lazy cache and indexes (internal, not part of public API)
        object.__setattr__(self, "_cache", {})
        object.__setattr__(self, "_index", None)

    # --- internal helpers for lazy evaluation ---
    def _ensure_index(self) -> None:
        """Build lightweight indexes over `self.mots` once and cache them.

        The index is intentionally minimal to avoid re-scanning PageWord
        collections in each property. It is built on first demand.
        """
        if getattr(self, "_index", None) is not None:
            return

        texts = [w.text for w in self.mots]
        centers = [((w.x0 + w.x1) / 2.0, (w.top + w.bottom) / 2.0) for w in self.mots]
        tops = [w.top for w in self.mots]

        idx = {
            "words": self.mots,
            "texts": texts,
            "centers": centers,
            "tops": tops,
        }

        object.__setattr__(self, "_index", idx)

    def _cache_get(self, key, compute_fn):
        cache = self._cache
        if key in cache:
            return cache[key]
        val = compute_fn()
        cache[key] = val
        return val

    _TIME_RE = re.compile(r"^([0-2]?\d):([0-5]\d)$")

    @staticmethod
    def _parse_time_token(token: str) -> Optional[int]:
        m = Diagram._TIME_RE.match(token)
        if not m:
            return None
        h = int(m.group(1))
        m12 = int(m.group(2))
        return h * 60 + m12

    def __len__(self) -> int:
        return len(self.mots)

    # The cache/index infrastructure above is preserved for future lazy
    # extraction. The Diagram object itself does not implement business
    # extraction heuristics here. Instead, we provide private helpers that
    # will locate sections inside the diagram structure; they currently
    # act as placeholders and return None.

    def _find_book_on_section(self):
        """Locate the section likely containing book-on information.

        Returns a lightweight descriptor or None. Placeholder — no heuristics.
        """
        self._ensure_index()
        return None

    def _find_book_off_section(self):
        """Locate the section likely containing book-off information."""
        self._ensure_index()
        return None

    def _find_duration_section(self):
        """Locate the section likely containing duration data."""
        self._ensure_index()
        return None

    def _find_effective_working_time_section(self):
        self._ensure_index()
        return None

    def _find_break_section(self):
        self._ensure_index()
        return None

    def _find_trains_section(self):
        self._ensure_index()
        return None

    def _find_observations_section(self):
        self._ensure_index()
        return None

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
