
from PySide6.QtCore import QObject, QEvent, Qt, QPoint
from PySide6.QtGui import QPainter, QColor, QPen

from app.gui.mapWindow import MapWindow


class InteractiveMap(MapWindow):

    def __init__(self):
        super().__init__()

        self.start_point = None
        self.end_point = None
        self.path = None 

        # Listen for clicks on the existing map
        self.map_label.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self.map_label:
            if event.type() == QEvent.Type.MouseButtonPress:
                if event.button() == Qt.MouseButton.LeftButton:
                    self.handle_click(event.position().toPoint())
                    return True

        return super().eventFilter(obj, event)

    def handle_click(self, pos):
        pixmap = self.map_img

        # Calculate image offset inside QLabel
        offset_x = (self.map_label.width() - pixmap.width()) // 2
        offset_y = (self.map_label.height() - pixmap.height()) // 2

        x = pos.x() - offset_x
        y = pos.y() - offset_y

        if not (0 <= x < pixmap.width()
                and 0 <= y < pixmap.height()):
            return

        if self.start_point is None or self.end_point is not None:
            self.start_point = (x, y)
            self.end_point = None
            print("START:", self.start_point)
        else:
            self.end_point = (x, y)
            print("END:", self.end_point)

        self.draw_points()

    def draw_points(self):
        pixmap = self.map_img.copy()
        painter = QPainter(pixmap)

        painter.setPen(QPen(Qt.GlobalColor.white, 2))

        if self.start_point is not None:
            painter.setBrush(QColor("green"))
            painter.drawEllipse(QPoint(*self.start_point), 8, 8)

        if self.end_point is not None:
            painter.setBrush(QColor("red"))
            painter.drawEllipse(QPoint(*self.end_point), 8, 8)

        painter.end()
        self.map_label.setPixmap(pixmap)

    def set_map(self, map_type):
        super().set_map(map_type)
        self.draw_points()
