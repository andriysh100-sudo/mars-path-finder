from PySide6.QtCore import Qt
from PySide6.QtWidgets import QBoxLayout, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QFrame, QSizePolicy

from gui.widgets import exitButton, mapToggleButton

#import gui.widgets.exitButton as exitButton
#import gui.widgets.mapToggleButton as mapToggleButton

class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("MARS NAVIGATORZ")

        layout_main = QVBoxLayout()
        layout_top_bar = QHBoxLayout()
        layout_content = QHBoxLayout()
        layout_map = QVBoxLayout()
        layout_side_bar = QVBoxLayout()
        
        layout_main.addLayout(layout_top_bar, stretch=2)
        layout_main.addLayout(layout_content, stretch=8)
        layout_content.addLayout(layout_map)
        layout_content.addLayout(layout_side_bar)

        layout_top_bar.setContentsMargins(0, 0, 0, 0)
        layout_top_bar.setDirection(QBoxLayout.Direction.RightToLeft)

        layout_content.setContentsMargins(0, 0, 0, 0)
        frame = QFrame()
        frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        frame.setStyleSheet("background-color: black;")
        layout_content.addWidget(frame)

        self.layout = layout_main

        exit_button = layout_top_bar.addWidget(exitButton.ExitButton(self), alignment=Qt.AlignmentFlag.AlignRight)
        temperature_button = layout_top_bar.addWidget(mapToggleButton.MapToggleButton(self, type="Temp"), alignment=Qt.AlignmentFlag.AlignRight)
        elevation_button = layout_top_bar.addWidget(mapToggleButton.MapToggleButton(self, type="Elevation"), alignment=Qt.AlignmentFlag.AlignRight)

        widget = QWidget()
        widget.setLayout(layout_main)
        self.setCentralWidget(widget)
    