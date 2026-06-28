import os

from PySide6.QtWidgets import QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,QLabel,QPushButton,QFileDialog,QListWidget,QTextEdit,QMessageBox

from models.catalogue import Catalogue
from services.planning_parser import lire_planning
from services.ics_generator import generer_ics

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.catalogue=None
        self.setWindowTitle("🚄 EuroPlanner")
        self.resize(1000,700)
        c=QWidget();self.setCentralWidget(c)
        l=QVBoxLayout(c)
        l.addWidget(QLabel("🚄 EuroPlanner"))
        h=QHBoxLayout();l.addLayout(h)
        g=QVBoxLayout();d=QVBoxLayout();h.addLayout(g);h.addLayout(d)
        self.liste_catalogues=QListWidget();g.addWidget(self.liste_catalogues)
        b=QPushButton("Importer les catalogues");b.clicked.connect(self.importer_catalogues);g.addWidget(b)
        self.zone_planning=QTextEdit();d.addWidget(self.zone_planning)
        b2=QPushButton("Créer le calendrier");b2.clicked.connect(self.creer_calendrier);d.addWidget(b2)
        self.label_statut=QLabel("Prêt.");l.addWidget(self.label_statut)
    def importer_catalogues(self):
        fichiers,_=QFileDialog.getOpenFileNames(self,"Choisir les catalogues","","Fichiers PDF (*.pdf)")
        if not fichiers:return
        self.liste_catalogues.clear()
        for f in fichiers:self.liste_catalogues.addItem(os.path.basename(f))
        self.catalogue=Catalogue(fichiers[0])
        self.label_statut.setText(f"{len(self.catalogue)} journée(s) chargée(s).")
    def creer_calendrier(self):
        if self.catalogue is None:
            QMessageBox.warning(self,"Catalogue","Importer un catalogue.");return
        planning=lire_planning(self.zone_planning.toPlainText())
        generer_ics(planning,self.catalogue,"Planning.ics")
        QMessageBox.information(self,"Succès","Planning.ics créé.")
