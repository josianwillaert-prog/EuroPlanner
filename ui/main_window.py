import os

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QListWidget,
    QTextEdit,
    QMessageBox,
)

from services.calendar_generator import creer_calendrier


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.catalogues = []

        self.setWindowTitle("🚄 EuroPlanner")
        self.resize(1000, 700)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()
        central.setLayout(layout)

        titre = QLabel("🚄 EuroPlanner")
        titre.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
        """)

        sous_titre = QLabel("Assistant de planning Eurostar")

        layout.addWidget(titre)
        layout.addWidget(sous_titre)

        contenu = QHBoxLayout()

        # -------- Catalogues --------

        gauche = QVBoxLayout()

        gauche.addWidget(QLabel("📂 Catalogues"))

        self.liste_catalogues = QListWidget()

        bouton_catalogues = QPushButton("Importer les catalogues")
        bouton_catalogues.clicked.connect(self.importer_catalogues)

        gauche.addWidget(self.liste_catalogues)
        gauche.addWidget(bouton_catalogues)

        # -------- Planning --------

        droite = QVBoxLayout()

        droite.addWidget(QLabel("📅 Planning"))

        self.zone_planning = QTextEdit()

        self.zone_planning.setPlaceholderText(
            "27/07/2026 J481a\n"
            "28/07/2026 J491a\n"
            "02/08/2026 J307a"
        )

        bouton_calendrier = QPushButton("Créer le calendrier")
        bouton_calendrier.clicked.connect(self.creer_calendrier)

        droite.addWidget(self.zone_planning)
        droite.addWidget(bouton_calendrier)

        contenu.addLayout(gauche, 1)
        contenu.addLayout(droite, 2)

        layout.addLayout(contenu)

        self.label_statut = QLabel("Prêt.")
        layout.addWidget(self.label_statut)

    def importer_catalogues(self):

        fichiers, _ = QFileDialog.getOpenFileNames(
            self,
            "Choisir les catalogues",
            "",
            "Fichiers PDF (*.pdf)"
        )

        if not fichiers:
            return

        self.catalogues = fichiers

        self.liste_catalogues.clear()

        for fichier in fichiers:
            self.liste_catalogues.addItem(os.path.basename(fichier))

        self.label_statut.setText(
            f"{len(fichiers)} catalogue(s) chargé(s)."
        )

    def creer_calendrier(self):

        texte = self.zone_planning.toPlainText().strip()

        if not texte:
            QMessageBox.warning(
                self,
                "Planning vide",
                "Veuillez saisir un planning."
            )
            return

        try:

            nb = creer_calendrier(
                texte,
                "Planning.ics"
            )

            self.label_statut.setText(
                f"Planning.ics créé ({nb} journée(s))."
            )

            QMessageBox.information(
                self,
                "Succès",
                "Le fichier Planning.ics a été créé."
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Erreur",
                str(e)
            )