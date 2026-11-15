from PySide6.QtWidgets import QPushButton


class MapToggleButton(QPushButton):

    def __init__(self, parent=None, map_type="default"):
        super().__init__(map_type.capitalize(), parent)
        self.map_type = map_type
        self.setCheckable(True)
        self.clicked.connect(lambda: parent.set_map(self.map_type))