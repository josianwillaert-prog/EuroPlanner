from dataclasses import dataclass, field


@dataclass
class JourneeService:
    """
    Représente une journée de service issue d'un catalogue Eurostar.
    """

    # Identifiant de la journée (J481A, G354B...)
    code: str

    # Horaires
    prise: str = ""
    fin: str = ""

    # Informations de service
    type_journee: str = "SERVICE"

    duree: str = ""
    travail: str = ""

    # Découcher
    decoucher: bool = False
    code_decoucher: str = ""

    # Trains
    trains: list[str] = field(default_factory=list)

    # Informations complémentaires
    observations: list[str] = field(default_factory=list)