from PySide6.QtWidgets import QMainWindow, QVBoxLayout
import gui.widgets.exitButton as exitButton

class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("MARS NAVIGATORZ")
        self.layout = QVBoxLayout()
        aButton = self.layout.addWidget(exitButton.ExitButton(self))
    

        
       # self.setGeometry(100, 100, 800, 600)