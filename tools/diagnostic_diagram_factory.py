from pathlib import Path
import sys

# Ajoute la racine du projet au PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parent.parent))

from services.pdf_layout_reader import lire_mots
from services.diagram_factory import DiagramFactory


def main() -> None:
    pdf_path = Path("catalogues/Catalogue JS DI(2).pdf")
    if not pdf_path.exists():
        print(f"PDF introuvable : {pdf_path}")
        return

    mots = lire_mots(str(pdf_path))
    factory = DiagramFactory()
    diagrams = factory.create_diagrams(mots)

    mots_non_affectes = set(mots)
    anomalies: list[str] = []

    print("Diagrammes détectés :")

    for diagram in diagrams:
        if len(diagram) == 0:
            anomalies.append(f"Diagramme vide détecté : {diagram.code} page {diagram.page}")

        page_words = [mot for mot in mots if mot.page == diagram.page]
        for mot in diagram.mots:
            mots_non_affectes.discard(mot)

        premier = diagram.mots[0].text if diagram.mots else "<aucun>"
        dernier = diagram.mots[-1].text if diagram.mots else "<aucun>"

        print(
            f"- {diagram.code} | page {diagram.page} | mots={len(diagram)} | bbox={diagram.bbox} | "
            f"premier={premier} | dernier={dernier}"
        )

    pages_diagrams: dict[int, list[tuple[float, float, str]]] = {}
    for diagram in diagrams:
        pages_diagrams.setdefault(diagram.page, []).append(
            (diagram.bbox[1], diagram.bbox[3], diagram.code)
        )

    for page, intervals in pages_diagrams.items():
        intervals.sort()
        for index in range(len(intervals) - 1):
            current_end = intervals[index][1]
            next_start = intervals[index + 1][0]
            if next_start < current_end:
                anomalies.append(
                    f"Chevauchement vertical sur page {page} : "
                    f"{intervals[index][2]} ({current_end:.1f}) / "
                    f"{intervals[index + 1][2]} ({next_start:.1f})"
                )

    if mots_non_affectes:
        anomalies.append(
            f"Mots non affectés à un diagramme : {len(mots_non_affectes)}"
        )

    print(f"\nTotal diagrammes : {len(diagrams)}")

    if not anomalies:
        print("OK : aucune anomalie détectée")
    else:
        print("Anomalies détectées :")
        for anomaly in anomalies:
            print(f"- {anomaly}")
