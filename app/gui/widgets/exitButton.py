from PySide6.QtWidgets import QPushButton


class ExitButton(QPushButton):

    def __init__(self, parent=None):
        super().__init__("Exit", parent)
        self.setObjectName("exitButton")
        self.clicked.connect(parent.close)