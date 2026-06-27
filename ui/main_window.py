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
)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("🚄 EuroPlanner")
        self.resize(1000, 700)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()
        central.setLayout(layout)

        # ---------- TITRE ----------

        titre = QLabel("🚄 EuroPlanner")
        titre.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
        """)

        sous_titre = QLabel("Assistant de planning Eurostar")

        layout.addWidget(titre)
        layout.addWidget(sous_titre)

        # ---------- CONTENU ----------

        contenu = QHBoxLayout()

        # ===== COLONNE GAUCHE =====

        gauche = QVBoxLayout()

        gauche.addWidget(QLabel("📂 Catalogues"))

        self.liste_catalogues = QListWidget()

        bouton_catalogues = QPushButton("Importer les catalogues")
        bouton_catalogues.clicked.connect(self.importer_catalogues)

        gauche.addWidget(self.liste_catalogues)
        gauche.addWidget(bouton_catalogues)

        # ===== COLONNE DROITE =====

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

        # ---------- STATUT ----------

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

        self.liste_catalogues.clear()

        for fichier in fichiers:
            self.liste_catalogues.addItem(os.path.basename(fichier))

        self.label_statut.setText(f"{len(fichiers)} catalogue(s) chargé(s).")

    def creer_calendrier(self):

        texte = self.zone_planning.toPlainText()

        nb_lignes = len([l for l in texte.splitlines() if l.strip()])

        self.label_statut.setText(
            f"{nb_lignes} journée(s) saisie(s)."
        )