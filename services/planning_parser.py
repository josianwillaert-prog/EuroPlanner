from models.planning_item import PlanningItem


def lire_planning(texte: str) -> list[PlanningItem]:
    """
    Lit le planning saisi par l'utilisateur.

    Format attendu :
        27/07/2026 J481A

    Les espaces multiples et tabulations sont acceptés.
    Les lignes invalides sont ignorées.
    Les codes sont normalisés en majuscules.
    """

    resultat = []

    if not texte:
        return resultat

    for numero_ligne, ligne in enumerate(texte.splitlines(), start=1):

        ligne = ligne.strip()

        if not ligne:
            continue

        morceaux = ligne.split()

        if len(morceaux) < 2:
            continue

        date = morceaux[0].strip()
        code = morceaux[1].strip().upper()

        resultat.append(
            PlanningItem(
                date=date,
                code=code
            )
        )

    return resultat