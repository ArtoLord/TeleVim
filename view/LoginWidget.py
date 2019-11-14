from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt


class LoginWidget(QWidget):

    layout = QVBoxLayout()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setLayout(self.layout)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(QLabel(":Televim"))
        self.layout.setAlignment(Qt.AlignHCenter)
