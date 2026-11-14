from PySide6.QtWidgets import QMainWindow, QPushButton, QWidget

class ExitButton(QPushButton):
    def __init__(self, parent=QMainWindow):
        super().__init__(parent)
        self.setText("Exit")

        font = self.font()
        font.setPointSize(30)
        self.setFont(font)



        self.textSize = 40
        self.setFixedSize(200, 100)
        self.clicked.connect(parent.close)

    