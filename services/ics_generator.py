from datetime import datetime

from ics import Calendar, Event


def generer_ics(
    planning,
    catalogue,
    fichier_sortie="Planning.ics",
):
    """
    Génère le calendrier ICS à partir du planning
    et du catalogue des journées.
    """

    calendrier = Calendar()

    for item in planning:

        journee = catalogue.get(item.code.upper())

        if journee is None:
            print(f"Journée inconnue : {item.code}")
            continue

        if not journee.prise or not journee.fin:
            print(f"Horaires manquants : {item.code}")
            continue

        debut = datetime.strptime(
            f"{item.date} {journee.prise}",
            "%d/%m/%Y %H:%M",
        )

        fin = datetime.strptime(
            f"{item.date} {journee.fin}",
            "%d/%m/%Y %H:%M",
        )

        if fin <= debut:
            from datetime import timedelta
            fin += timedelta(days=1)

        evenement = Event()

        evenement.name = item.code

        evenement.begin = debut
        evenement.end = fin

        description = [
            f"Code : {journee.code}",
            f"Prise : {journee.prise}",
            f"Fin : {journee.fin}",
        ]

        if journee.duree:
            description.append(f"Durée : {journee.duree}")

        if journee.travail:
            description.append(f"Travail effectif : {journee.travail}")

        if journee.decoucher:
            description.append("Découcher : Oui")

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