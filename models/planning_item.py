from dataclasses import dataclass, field


@dataclass
class PlanningItem:
    # Informations provenant du planning saisi
    date: str
    code: str

    # Informations qui seront complétées à partir des catalogues
    heure_debut: str = ""
    heure_fin: str = ""

    type_journee: str = ""

    trains: list[str] = field(default_factory=list)

    decoucher: str = ""

    observations: list[str] = field(default_factory=list)