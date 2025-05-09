import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

from PL_model import PLWindow
from PLNE_model import PLNEWindow

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Projet de Recherche Opérationnelle")
        self.setGeometry(100, 100, 600, 500)
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #fdfefe;
                font-family: Arial, sans-serif;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 12px 20px;
                font-size: 16px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QLabel#title {
                font-size: 22px;
                font-weight: bold;
                color: #2c3e50;
            }
        """)

        layout = QVBoxLayout()


        image_label = QLabel()
        pixmap = QPixmap("img.png")
        pixmap = pixmap.scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)


        title = QLabel("Application de Résolution - Recherche Opérationnelle")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        layout.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding))

        subtitle = QLabel("Fait par : Rami Kaabi, Maryem Dammak, Ithar Hadj Amor")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 14px; color: #555; font-style: italic; margin-bottom: 15px;")
        layout.addWidget(subtitle)

        btn_pl = QPushButton("Problème de Transport (PL)")
        btn_pl.clicked.connect(self.open_pl)
        layout.addWidget(btn_pl, alignment=Qt.AlignCenter)

        btn_plne = QPushButton("Ouverture de Centres (PLNE)")
        btn_plne.clicked.connect(self.open_plne)
        layout.addWidget(btn_plne, alignment=Qt.AlignCenter)

        layout.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)

    def open_pl(self):
        self.pl_win = PLWindow()
        self.pl_win.show()

    def open_plne(self):
        self.plne_win = PLNEWindow()
        self.plne_win.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
