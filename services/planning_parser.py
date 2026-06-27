from models.journee_service import JourneeService


def lire_planning(texte: str):

    resultat = []

    for ligne in texte.splitlines():

        ligne = ligne.strip()

        if not ligne:
            continue

        morceaux = ligne.split()

        if len(morceaux) < 2:
            continue

        resultat.append(
            JourneeService(
                date=morceaux[0],
                code=morceaux[1]
            )
        )

    return resultat