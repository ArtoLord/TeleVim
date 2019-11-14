from PyQt5.QtWidgets import QWidget, QVBoxLayout

from view.LoginWidget import LoginWidget
from view.StatusBarWidget import StatusBarWidget


class MainWidget(QWidget):

    layout = QVBoxLayout()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setLayout(self.layout)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(LoginWidget())
        self.layout.addStretch(1)
        self.layout.addWidget(StatusBarWidget())
