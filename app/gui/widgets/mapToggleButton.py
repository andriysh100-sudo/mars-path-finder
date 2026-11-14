from PySide6.QtWidgets import QMainWindow, QPushButton, QWidget

class MapToggleButton(QPushButton):

    map_type = "default"

    def __init__(self, parent=QMainWindow, map_type="default"):
        super().__init__(parent)
        self.setText(map_type)
        self.map_type = map_type

        font = self.font()
        font.setPointSize(30)
        self.setFont(font)

        self.textSize = 40
        self.setFixedSize(200, 100)
        self.clicked.connect(lambda: parent.set_map(self.map_type))

    