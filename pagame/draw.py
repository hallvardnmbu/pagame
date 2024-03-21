from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtWidgets import QDialog, QGraphicsView, QGraphicsScene, QVBoxLayout


class Draw(QDialog):
    def __init__(self):
        super().__init__()

        self.canvas = Canvas()

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)


class Canvas(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.size = 100

        self.scene = QGraphicsScene(self)
        self.scene.setBackgroundBrush(QBrush(QColor("white")))
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setFixedSize(800, 800)

        self.setCursor(Qt.CrossCursor)

        self.update()

    def update(self):
        self.scene.clear()
        pen = QPen(Qt.NoPen)
        brush = QBrush(QColor("white"))
        for i in range(40):
            rect = QRectF(i * self.size, i * self.size, self.size, self.size)
            self.scene.addRect(rect, pen, brush)

        self.scene.setSceneRect(self.scene.itemsBoundingRect())
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

    def resizeEvent(self, event):
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

    def mousePressEvent(self, event):
        self.mouseMoveEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() != Qt.LeftButton:
            return

        position = self.mapToScene(event.pos())
        i = int(position.x() // self.size)
        j = int(position.y() // self.size)

        self.scene.addRect(
            i * self.size, j * self.size,
            self.size, self.size,
            QPen(Qt.NoPen), QBrush(QColor("black"))
        )
