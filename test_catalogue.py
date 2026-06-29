from models.catalogue import Catalogue

catalogue = Catalogue("catalogues/C2 - Je.PDF")

for code in sorted(catalogue.journees):

    j = catalogue[code]

    print(f"{code:6}  {j.prise:5}  {j.fin}")