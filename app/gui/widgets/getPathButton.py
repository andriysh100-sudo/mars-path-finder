from PySide6.QtWidgets import QPushButton


class GetPathButton(QPushButton):

    def __init__(self, parent=None):
        super().__init__("Get path", parent)
        self.setObjectName("primaryButton")
        # The path logic lives in InteractiveMap.get_path
        self.clicked.connect(lambda: parent.get_path())