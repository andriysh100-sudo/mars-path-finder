from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QBoxLayout, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QFrame, QSizePolicy, QLabel

from gui.widgets import exitButton, mapToggleButton, mapLabel

import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

#import gui.widgets.exitButton as exitButton
#import gui.widgets.mapToggleButton as mapToggleButton

class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("MARS NAVIGATORZ")

        self.map_dict = {
            "optical" : QPixmap(os.path.join(ROOT_DIR, "../data/map/optical_map.png")),
            "slope" : QPixmap(os.path.join(ROOT_DIR, "../data/map/slope_map.png")),
            "elevation" : QPixmap(os.path.join(ROOT_DIR, "../data/map/elevation_map.png")),
            "thermal" : QPixmap(os.path.join(ROOT_DIR, "../data/map/optical_map.png"))
        }

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
        layout_top_bar.setSpacing(0)
        layout_top_bar.setDirection(QBoxLayout.Direction.RightToLeft)
        layout_content.setContentsMargins(0, 0, 0, 0)
        layout_map.setContentsMargins(0, 0, 0, 0)
        layout_map.hasHeightForWidth()
        layout_side_bar.setContentsMargins(0, 0, 0, 0)

        ## SET MAIN LAYOUT ##
        self.layout = layout_main

        layout_side_bar.addWidget(QLabel("Side Bar"), alignment=Qt.AlignmentFlag.AlignCenter)

        ### SET UP FRAME ###
        self.map_img = QPixmap(os.path.join(ROOT_DIR, "../data/map/optical_map.png"))
        #self.map_label = QLabel()
        self.map_label = mapLabel.MapLabel(self)
        self.map_label.setPixmap(self.map_img)
        self.map_label.paint_path([3,4,5,6])
       
        self.map_label.setStyleSheet("background-color: black;")
        self.map_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.map_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        layout_map.addWidget(self.map_label)

        
        
        #frame = QFrame()
        #frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #
        

        ## ADD TOP BAR BUTTONS ##
        exit_button = layout_top_bar.addWidget(exitButton.ExitButton(self), alignment=Qt.AlignmentFlag.AlignRight)
        layout_top_bar.addStretch()
        temperature_button = layout_top_bar.addWidget(mapToggleButton.MapToggleButton(self, map_type="thermal"), alignment=Qt.AlignmentFlag.AlignLeft)
        elevation_button = layout_top_bar.addWidget(mapToggleButton.MapToggleButton(self, map_type="elevation"), alignment=Qt.AlignmentFlag.AlignLeft)
        slope_button = layout_top_bar.addWidget(mapToggleButton.MapToggleButton(self, map_type="slope"), alignment=Qt.AlignmentFlag.AlignLeft)
        base_button = layout_top_bar.addWidget(mapToggleButton.MapToggleButton(self, map_type="optical"), alignment=Qt.AlignmentFlag.AlignLeft)

        widget = QWidget()
        widget.setLayout(layout_main)
        self.setCentralWidget(widget)

    ## PRINTS THE MAP TYPE OF THE BUTTON PRESSED, USE THIS FOR WHATEVR YOU WANT ##
    def set_map(self, map_type):
        self.map_img = self.map_dict[map_type]
        self.map_label.setPixmap(self.map_img)

        

    