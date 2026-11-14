from PySide6.QtCore import Qt
from PySide6.QtWidgets import QBoxLayout, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QFrame, QSizePolicy, QLabel

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

        ## SET SIZES ON LAYOUTS ##
        layout_main.addLayout(layout_top_bar, stretch=2)
        layout_main.addLayout(layout_content, stretch=8)
        layout_content.addLayout(layout_map, stretch=8)
        layout_content.addLayout(layout_side_bar, stretch=2)

        ## SET MARGINS & DIRECTIONS ON LAYOUTS ##
        layout_top_bar.setContentsMargins(0, 0, 0, 0)
        layout_top_bar.setDirection(QBoxLayout.Direction.RightToLeft)
        layout_content.setContentsMargins(0, 0, 0, 0)
        layout_map.setContentsMargins(0, 0, 0, 0)
        layout_side_bar.setContentsMargins(0, 0, 0, 0)

        ## SET MAIN LAYOUT ##
        self.layout = layout_main

        layout_side_bar.addWidget(QLabel("Side Bar"), alignment=Qt.AlignmentFlag.AlignCenter)

        ### SET UP FRAME ###
        frame = QFrame()
        frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        frame.setStyleSheet("background-color: black;")
        layout_map.addWidget(frame)

        ## ADD TOP BAR BUTTONS ##
        exit_button = layout_top_bar.addWidget(exitButton.ExitButton(self), alignment=Qt.AlignmentFlag.AlignRight)
        temperature_button = layout_top_bar.addWidget(mapToggleButton.MapToggleButton(self, type="Temp"), alignment=Qt.AlignmentFlag.AlignRight)
        elevation_button = layout_top_bar.addWidget(mapToggleButton.MapToggleButton(self, type="Elevation"), alignment=Qt.AlignmentFlag.AlignRight)

        widget = QWidget()
        widget.setLayout(layout_main)
        self.setCentralWidget(widget)
    