from dataclasses import dataclass


@dataclass(slots=True)
class Train:

    numero: str = ""

    materiel: str = ""

    depart: str = ""
    heure_depart: str = ""

    arrivee: str = ""
    heure_arrivee: str = ""

    voie_depart: str = ""
    voie_arrivee: str = ""

    commentaire: str = ""

    @property
    def est_valide(self):

        return (
            self.numero != ""
            and self.depart != ""
            and self.arrivee != ""
        )

    def __str__(self):

        texte = (
            f"{self.numero} "
            f"{self.depart} {self.heure_depart}"
            f" → "
            f"{self.arrivee} {self.heure_arrivee}"
        )

        if self.materiel:
            texte += f" ({self.materiel})"

        return texte