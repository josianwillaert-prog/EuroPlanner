from datetime import datetime, timedelta

from ics import Calendar, Event


def _convertir_datetime(date: str, heure: str) -> datetime:

    for fmt in (
        "%d/%m/%Y %H:%M",
        "%d/%m/%y %H:%M",
    ):

        try:
            return datetime.strptime(
                f"{date} {heure}",
                fmt,
            )

        except ValueError:
            pass

    raise ValueError(
        f"Date invalide : {date} {heure}"
    )


def generer_ics(
    planning,
    catalogue,
    fichier_sortie="Planning.ics",
):

    calendrier = Calendar()

    print("=" * 60)
    print("Création du calendrier")
    print("=" * 60)
    print("Nombre de lignes du planning :", len(planning))
    print("Nombre de journées catalogue :", len(catalogue))
    print()

    for item in planning:

        print("-" * 40)
        print("Planning :", item.date, item.code)

        journee = catalogue.get(item.code)

        print("Catalogue :", journee)

        if journee is None:

            print(">>> Journée introuvable")
            continue

        if not journee.prise or not journee.fin:

            print(">>> Horaires manquants")
            continue

        debut = _convertir_datetime(
            item.date,
            journee.prise,
        )

        fin = _convertir_datetime(
            item.date,
            journee.fin,
        )

        if fin <= debut:
            fin += timedelta(days=1)

        evenement = Event()

        evenement.name = journee.code
        evenement.begin = debut
        evenement.end = fin

        description = [
            f"Code : {journee.code}",
            f"Prise : {journee.prise}",
            f"Fin : {journee.fin}",
        ]

        evenement.description = "\n".join(description)

        calendrier.events.add(evenement)

        print(">>> Evènement ajouté")

    print()
    print("Nombre d'évènements :", len(calendrier.events))

    with open(
        fichier_sortie,
        "w",
        encoding="utf-8",
    ) as fichier:

        fichier.writelines(calendrier)

    print("ICS créé :", fichier_sortie)

    return fichier_sortie