from services.pdf_layout_reader import lire_mots_pdf

mots = lire_mots_pdf("catalogues/C2 - Je.PDF")

for mot in mots[:100]:
    print(mot)