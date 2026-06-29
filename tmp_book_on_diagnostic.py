from pathlib import Path
from services.pdf_layout_reader import lire_mots
from services.diagram_factory import DiagramFactory

pdfs = sorted(Path('catalogues').glob('*.pdf'))
summary = []
for p in pdfs:
    mots = lire_mots(str(p))
    factory = DiagramFactory()
    diagrams = factory.create_diagrams(mots)
    valid = [d for d in diagrams if d.book_on is not None]
    missing = [d for d in diagrams if d.book_on is None]
    summary.append((p.name, len(diagrams), len(valid), len(missing), [d.code for d in missing]))

for name, total, valid, missing, missing_codes in summary:
    print(f"{name}: diagrams={total}, book_on_valid={valid}, book_on_missing={missing}")
    if missing:
        print('   missing codes:', ', '.join(missing_codes[:20]))

print('TOTAL diagrams', sum(total for _, total, _, _, _ in summary))
print('TOTAL book_on_valid', sum(valid for _, _, valid, _, _ in summary))
print('TOTAL book_on_missing', sum(missing for _, _, _, missing, _ in summary))
