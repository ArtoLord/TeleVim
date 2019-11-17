from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit
from PyQt5.QtCore import pyqtSignal, Qt, pyqtSlot
from PyQt5.QtGui import QKeyEvent

from Controller import Controller


def status_item_widget(text: str) -> QWidget:
    v = QLabel(text)
    v.setObjectName("StatusItem")
    return v


class StatusBarWidget(QWidget):

    commandSignal = pyqtSignal(str, name="commandSignal")
    statusList = []
    layout = QHBoxLayout()

    def __init__(self):
        super().__init__()
        self.commandLine = QLineEdit()
        self.setObjectName("Statusbar")
        self.initUI()
        self.connectSignals()

    def initUI(self):
        self.setLayout(self.layout)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.commandLine)
        for s in self.statusList:
            self.layout.addWidget(status_item_widget(s))

    def connectSignals(self):
        def keyEvent():
            old = self.commandLine.keyPressEvent

            def inner(a0: QKeyEvent):
                old(a0)
                self.keyPressEvent(a0)
            return inner

        self.commandLine.keyPressEvent = keyEvent()
        self.commandLine.textChanged.connect(Controller().onCommand)
        Controller().callbackSignal.connect(self.onCallback)

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        if a0.key() == Qt.Key_Return:
            print("Enter")
        self.commandSignal.emit(a0.text())

    @pyqtSlot(int, name="callbackSignal")
    def onCallback(self, i: int):
        print(i)
