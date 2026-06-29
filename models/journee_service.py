from dataclasses import dataclass, field

from models.train import Train


@dataclass(slots=True)
class JourneeService:

    code: str

    prise: str = ""
    fin: str = ""

    type_journee: str = "SERVICE"

    duree: str = ""
    travail: str = ""

    decoucher: bool = False
    code_decoucher: str = ""

    trains: list[Train] = field(default_factory=list)

    observations: list[str] = field(default_factory=list)