from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit


def status_item_widget(text: str) -> QWidget:
    v = QLabel(text)
    v.setObjectName("StatusItem")
    return v


class StatusBarWidget(QWidget):

    statusList = []
    layout = QHBoxLayout()

    def __init__(self):
        super().__init__()
        self.setObjectName("Statusbar")
        self.setLayout(self.layout)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        command_line = QLineEdit()
        self.layout.addWidget(QLineEdit(command_line))
        for s in self.statusList:
            self.layout.addWidget(status_item_widget(s))
