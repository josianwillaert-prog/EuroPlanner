from PySide6.QtWidgets import QFileDialog


def choisir_catalogues(parent):
    fichiers, _ = QFileDialog.getOpenFileNames(
        parent,
        "Choisir les catalogues",
        "",
        "Fichiers PDF (*.pdf)"
    )

    return fichiers