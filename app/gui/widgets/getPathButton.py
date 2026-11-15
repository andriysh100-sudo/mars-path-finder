from PySide6.QtWidgets import QPushButton

from scripts.a_star import run_a_star


class GetPathButton(QPushButton):

    def __init__(self, parent=None):
        super().__init__("Get path", parent)
        self.window = parent

        font = self.font()
        font.setPointSize(30)
        self.setFont(font)
        self.setFixedSize(200, 100)

        self.clicked.connect(self.on_click)
    def on_click(self):
        start = self.window.start_point
        end = self.window.end_point

        if start is None or end is None:
            print("Set both a start and an end point first")
            return

        print("Path from", start, "to", end)
        print(run_a_star(start, end))