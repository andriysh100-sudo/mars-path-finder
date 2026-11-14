from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("MARS NAVIGATORZ")
        self.exitButton = QPushButton("Exit", self)
        self.exitButton.clicked.connect(self.close)
       # self.setGeometry(100, 100, 800, 600)