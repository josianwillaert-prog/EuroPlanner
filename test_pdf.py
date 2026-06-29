from services.pdf_reader import lire_pdf

texte = lire_pdf("catalogues/C2 - Je.pdf")

i = texte.find("Nr diagram:")

print(texte[i:i+300])