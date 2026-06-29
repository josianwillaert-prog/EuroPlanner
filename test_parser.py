from services.pdf_reader import lire_pdf
from services.diagram_parser import analyser_pdf

texte = lire_pdf("catalogues/C2 - Je.pdf")

journees = analyser_pdf(texte)

for j in journees:
    print(j)