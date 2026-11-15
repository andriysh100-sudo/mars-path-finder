from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QFrame,
                               QSizePolicy, QLabel, QButtonGroup)

from app.gui.widgets import exitButton, mapToggleButton, getPathButton

import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
MAP_DIR = os.path.join(ROOT_DIR, "../data/map")

STYLE = """
QWidget {
    background-color: #0f1115;
    color: #e8e6e3;
    font-size: 14px;
}
#topBar {
    background-color: #171a21;
    border-bottom: 1px solid #2a2f3a;
}
#sideBar {
    background-color: #171a21;
    border-left: 1px solid #2a2f3a;
}
#topBar QLabel, #sideBar QLabel { background: transparent; }
#appTitle {
    font-size: 16px;
    font-weight: bold;
    letter-spacing: 2px;
}
#mapLabel { background-color: #000000; }

QPushButton {
    background-color: #232833;
    border: 1px solid #2a2f3a;
    border-radius: 6px;
    padding: 6px 16px;
}
QPushButton:hover   { background-color: #2e3442; }
QPushButton:pressed { background-color: #1b1f27; }
QPushButton:checked {
    background-color: #e0623a;
    border-color: #e0623a;
    color: #0f1115;
    font-weight: bold;
}
#primaryButton {
    background-color: #00b8d4;
    border-color: #00b8d4;
    color: #0f1115;
    font-weight: bold;
}
#primaryButton:hover   { background-color: #26c6da; }
#primaryButton:pressed { background-color: #0097a7; }
#exitButton:hover { background-color: #c0392b; border-color: #c0392b; }

#sideStatus { color: #e8e6e3; font-size: 14px; }
#sideTitle  { color: #8a8f98; font-size: 11px; letter-spacing: 1px; }
#sideValue  { font-size: 20px; font-weight: bold; }
#sideRule   { background-color: #2a2f3a; max-height: 1px; border: none; }
"""

# Sidebar rows: (key, title shown above the value)
SIDEBAR_ROWS = (
    ("map", "MAP"),
    ("start", "START"),
    ("end", "DESTINATION"),
    ("distance", "DISTANCE"),
    ("eta", "ETA"),
)


class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("MARS NAVIGATORZ")
        self.setStyleSheet(STYLE)

        self.map_dict = {
            "optical":   QPixmap(os.path.join(MAP_DIR, "optical_map.png")),
            "slope":     QPixmap(os.path.join(MAP_DIR, "slope_map.png")),
            "elevation": QPixmap(os.path.join(MAP_DIR, "elevation_map.png")),
            "thermal":   QPixmap(os.path.join(MAP_DIR, "optical_map.png")),
        }
        self.map_img = self.map_dict["optical"]

        ## TOP BAR: title left, map buttons, then actions on the right ##
        top_bar = QFrame()
        top_bar.setObjectName("topBar")
        top_bar.setFixedHeight(56)
        layout_top_bar = QHBoxLayout(top_bar)
        layout_top_bar.setContentsMargins(16, 0, 16, 0)
        layout_top_bar.setSpacing(8)

        title = QLabel("MARS NAVIGATOR")
        title.setObjectName("appTitle")
        layout_top_bar.addWidget(title)
        layout_top_bar.addStretch()

        self.map_buttons = QButtonGroup(self)
        self.map_buttons.setExclusive(True)
        for map_type in ("optical", "slope", "elevation", "thermal"):
            button = mapToggleButton.MapToggleButton(self, map_type=map_type)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            self.map_buttons.addButton(button)
            layout_top_bar.addWidget(button)
            if map_type == "optical":
                button.setChecked(True)

        layout_top_bar.addSpacing(16)
        layout_top_bar.addWidget(getPathButton.GetPathButton(self))
        layout_top_bar.addWidget(exitButton.ExitButton(self))

        ## MAP ##
        self.map_label = QLabel()
        self.map_label.setObjectName("mapLabel")
        self.map_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.map_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)

        ## SIDE BAR: status line, then title/value rows ##
        side_bar = QFrame()
        side_bar.setObjectName("sideBar")
        side_bar.setFixedWidth(260)
        layout_side_bar = QVBoxLayout(side_bar)
        layout_side_bar.setContentsMargins(20, 20, 20, 20)
        layout_side_bar.setSpacing(4)

        self.side_status = QLabel("")
        self.side_status.setObjectName("sideStatus")
        self.side_status.setWordWrap(True)
        self.side_status.setMinimumHeight(44)
        self.side_status.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout_side_bar.addWidget(self.side_status)

        rule = QFrame()
        rule.setObjectName("sideRule")
        rule.setFixedHeight(1)
        layout_side_bar.addWidget(rule)
        layout_side_bar.addSpacing(16)

        self.side_values = {}
        for key, text in SIDEBAR_ROWS:
            title_label = QLabel(text)
            title_label.setObjectName("sideTitle")
            value_label = QLabel("—")
            value_label.setObjectName("sideValue")
            layout_side_bar.addWidget(title_label)
            layout_side_bar.addWidget(value_label)
            layout_side_bar.addSpacing(16)
            self.side_values[key] = value_label
        layout_side_bar.addStretch()
        self.update_sidebar(map="Optical")

        ## PUT IT TOGETHER ##
        layout_content = QHBoxLayout()
        layout_content.setContentsMargins(0, 0, 0, 0)
        layout_content.setSpacing(0)
        layout_content.addWidget(self.map_label, stretch=1)
        layout_content.addWidget(side_bar)

        layout_main = QVBoxLayout()
        layout_main.setContentsMargins(0, 0, 0, 0)
        layout_main.setSpacing(0)
        layout_main.addWidget(top_bar)
        layout_main.addLayout(layout_content, stretch=1)

        widget = QWidget()
        widget.setLayout(layout_main)
        self.setCentralWidget(widget)

    def update_sidebar(self, status=None, **values):
        """update_sidebar(status="...", eta="42 min"). Pass None as a value to reset it to a dash."""
        if status is not None:
            self.side_status.setText(status)
        for key, value in values.items():
            if key in self.side_values:
                self.side_values[key].setText("—" if value is None else str(value))

    def set_map(self, map_type):
        self.map_img = self.map_dict[map_type]
        self.update_sidebar(map=map_type.capitalize())
        self.show_map()

    def show_map(self):
        if self.map_img.isNull():
            return
        self.map_label.setPixmap(self.map_img.scaled(
            self.map_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.show_map()