import math

from PySide6.QtCore import QEvent, Qt, QPointF
from PySide6.QtGui import QPainter, QColor, QPen, QPolygonF
from PySide6.QtWidgets import QApplication

from app.gui.mapWindow import MapWindow
from scripts.a_star import run_a_star

# ASSUMPTIONS: set these to match your data and your walking model.
METRES_PER_PIXEL = 1.0      # ground distance covered by one pixel of the map images
WALK_SPEED_M_S = 1.0        # flat walking speed used for the simple ETA


class InteractiveMap(MapWindow):

    def __init__(self):
        super().__init__()

        self.start_point = None      # (x, y) in original image pixels
        self.end_point = None
        self.path = None             # list of (x, y) in original image pixels

        # Listen for clicks on the existing map
        self.map_label.installEventFilter(self)
        self.update_sidebar(status="Click the map to set a start point.")

    def eventFilter(self, obj, event):
        if obj == self.map_label:
            if event.type() == QEvent.Type.MouseButtonPress:
                if event.button() == Qt.MouseButton.LeftButton:
                    self.handle_click(event.position())
                    return True

        return super().eventFilter(obj, event)

    def handle_click(self, pos):
        if self.map_img.isNull():
            return
        scale = min(self.map_label.width() / self.map_img.width(),
                    self.map_label.height() / self.map_img.height())

        # The scaled image is centred in the label: remove the bars, then undo the scaling
        offset_x = (self.map_label.width() - self.map_img.width() * scale) / 2
        offset_y = (self.map_label.height() - self.map_img.height() * scale) / 2
        x = int((pos.x() - offset_x) / scale)
        y = int((pos.y() - offset_y) / scale)

        if not (0 <= x < self.map_img.width() and 0 <= y < self.map_img.height()):
            return

        self.path = None                         # any old route is now out of date
        if self.start_point is None or self.end_point is not None:
            self.start_point = (x, y)
            self.end_point = None
            print("START:", self.start_point)
            self.update_sidebar(status="Click the map to set a destination.",
                                start=f"{x}, {y}", end=None, distance=None, eta=None)
        else:
            self.end_point = (x, y)
            print("END:", self.end_point)
            self.update_sidebar(status="Press Get path to find a route.",
                                end=f"{x}, {y}", distance=None, eta=None)

        self.show_map()

    def get_path(self):
        """Called by the Get path button."""
        if self.start_point is None or self.end_point is None:
            self.update_sidebar(status="Set both a start and a destination first.")
            return

        self.update_sidebar(status="Calculating route…")
        QApplication.processEvents()             # let the status text appear before the search runs

        try:
            path = run_a_star(self.start_point, self.end_point)
        except Exception as error:
            print("A* failed:", error)
            path = None

        if not path:
            self.path = None
            self.update_sidebar(status="No route found between these points.",
                                distance=None, eta=None)
            self.show_map()
            return

        self.path = [(p[0], p[1]) for p in path]

        pixels = sum(math.hypot(x2 - x1, y2 - y1)
                     for (x1, y1), (x2, y2) in zip(self.path, self.path[1:]))
        metres = pixels * METRES_PER_PIXEL
        minutes = metres / WALK_SPEED_M_S / 60
        self.update_sidebar(status="Route found.",
                            distance=f"{metres / 1000:.2f} km" if metres >= 1000 else f"{metres:.0f} m",
                            eta=f"{minutes:.0f} min")
        self.show_map()

    def show_map(self):
        """Replaces MapWindow.show_map: scaled map, then the route, then the markers on top."""
        if self.map_img.isNull():
            return
        pixmap = self.map_img.scaled(self.map_label.size(),
                                     Qt.AspectRatioMode.KeepAspectRatio,
                                     Qt.TransformationMode.SmoothTransformation)
        scale = pixmap.width() / self.map_img.width()

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        path = getattr(self, "path", None)
        if path:
            line = QPolygonF([QPointF(x * scale, y * scale) for x, y in path])
            for color, width in (("#0f1115", 6), ("#00e5ff", 3)):      # dark outline, then the line
                pen = QPen(QColor(color), width)
                pen.setCapStyle(Qt.PenCapStyle.RoundCap)
                pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
                painter.setPen(pen)
                painter.drawPolyline(line)

        painter.setPen(QPen(Qt.GlobalColor.white, 2))
        for point, color in ((getattr(self, "start_point", None), "#00e676"),
                             (getattr(self, "end_point", None), "#ff5252")):
            if point is not None:
                painter.setBrush(QColor(color))
                painter.drawEllipse(QPointF(*point) * scale, 8, 8)
        painter.end()

        self.map_label.setPixmap(pixmap)