from models.train import Train


class TableParser:

    def __init__(self, lignes):
        self.lignes = lignes

    def extraire_trains(self):

        trains = []

        for ligne in self.lignes:

            mots = ligne.words

            if len(mots) < 5:
                continue

            if not mots[0].text.isdigit():
                continue

            if len(mots[0].text) != 4:
                continue

            train = Train()

            train.numero = mots[0].text

            for mot in mots[1:]:

                txt = mot.text

                if txt in ("TD", "TM2"):
                    train.materiel = txt

                elif txt in ("PNO", "LSS", "BRU"):

                    if not train.depart:
                        train.depart = txt
                    else:
                        train.arrivee = txt

                elif ":" in txt:

                    if not train.heure_depart:
                        train.heure_depart = txt
                    else:
                        train.heure_arrivee = txt

            trains.append(train)

        return trains