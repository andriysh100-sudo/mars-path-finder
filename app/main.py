import sys

from PySide6.QtWidgets import QApplication, QMessageBox


def main():
	app = QApplication(sys.argv)
	QMessageBox.information(None, "Hello", "Hello from PySide6!")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
