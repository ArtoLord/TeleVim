import sys
from PyQt5.QtWidgets import QApplication
from view.MainWidget import MainWidget


def load_styles() -> str:
    with open("./view/styles/style.css", "r") as f:
        return "".join(f.readlines())


if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet(load_styles())
    v = MainWidget()
    v.show()
    sys.exit(app.exec_())
