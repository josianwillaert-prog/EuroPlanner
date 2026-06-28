from datetime import datetime, timedelta

from ics import Calendar, Event


def _convertir_datetime(date: str, heure: str) -> datetime:
    """
    Accepte les dates au format :
        23/07/26
        23/07/2026
    """

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
    """
    Génère le calendrier ICS à partir du planning
    et du catalogue.
    """

    calendrier = Calendar()

    for item in planning:

        journee = catalogue.get(item.code)

        if journee is None:
            print(f"Journée inconnue : {item.code}")
            continue

        if not journee.prise or not journee.fin:
            print(f"Horaires manquants : {item.code}")
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

        if journee.duree:
            description.append(
                f"Durée : {journee.duree}"
            )

        if journee.travail:
            description.append(
                f"Travail effectif : {journee.travail}"
            )

        if journee.decoucher:
            description.append(
                "Découcher : Oui"
            )

        if journee.code_decoucher:
            description.append(
                f"Suite : {journee.code_decoucher}"
            )

        if journee.trains:
            description.append("")
            description.append("Trains :")

            for train in journee.trains:
                description.append(train)

        evenement.description = "\n".join(description)

        calendrier.events.add(evenement)

    with open(
        fichier_sortie,
        "w",
        encoding="utf-8",
    ) as fichier:
        fichier.writelines(calendrier)

    return fichier_sortie