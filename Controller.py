from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
from PyQt5Singleton import Singleton


class Controller(QObject, metaclass=Singleton):

    i = 0
    callbackSignal = pyqtSignal(int)

    @pyqtSlot(str, name="commandSignal")
    def onCommand(self, command: str):
        self.i += 1
        self.callbackSignal.emit(self.i)
