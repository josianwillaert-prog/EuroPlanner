from dataclasses import dataclass


@dataclass
class Train:
    numero: str = ""

    depart: str = ""
    heure_depart: str = ""

    arrivee: str = ""
    heure_arrivee: str = ""

    materiel: str = ""

    def __str__(self):

        return (
            f"{self.numero} "
            f"{self.depart} {self.heure_depart} → "
            f"{self.arrivee} {self.heure_arrivee}"
        )