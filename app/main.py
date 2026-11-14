import sys

import gui.mapWindow as mapWindow

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QLabel, QMessageBox, QPushButton, QWidget


def main():
    app = QApplication(sys.argv)
    mainWindow = mapWindow.MapWindow()
    mainWindow.showFullScreen()
    app.exec()
    return 0


if __name__ == "__main__":
	raise SystemExit(main())
