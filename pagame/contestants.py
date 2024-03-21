from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QListWidget
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import Qt


BUTTON_SIZE = 55


class Contestants(QWidget):
    """Widget to add and remove contestants."""
    def __init__(self):
        super().__init__()

        self.contestants = []

        layout = QVBoxLayout()
        top = QHBoxLayout()

        self.entry = QLineEdit()
        self.entry.setPlaceholderText("Name")
        self.entry.setFixedHeight(int(BUTTON_SIZE * 0.5))
        self.entry.setAlignment(Qt.AlignCenter)
        self.entry.returnPressed.connect(self._add)  # noqa
        top.addWidget(self.entry)
        top.addSpacing(10)

        add = QPushButton("Include")
        add.setFixedSize(int(BUTTON_SIZE * 1.5), int(BUTTON_SIZE * 0.5))
        add.clicked.connect(self._add)  # noqa
        top.addWidget(add)

        layout.addLayout(top)

        self.names = QListWidget()
        self.names.setFixedHeight(int(BUTTON_SIZE * 1.5))
        self.names.itemClicked.connect(self._remove)  # noqa
        layout.addWidget(self.names)

        self.setLayout(layout)

    def _add(self):
        """Add contestant."""
        name = self.entry.text()
        if name:
            self.names.addItem(name)
            self.contestants.append(name) if name not in self.contestants else None
            self.entry.clear()

    def _remove(self, item):
        """Remove contestant."""
        self.names.takeItem(self.names.row(item))
        self.contestants.remove(item.text())

    def rigged(self, person):
        """Color the rigged person."""
        for i in range(self.names.count()):
            if self.names.item(i).text().lower() == person.lower():
                print(person)
                self.names.item(i).setForeground(QBrush(QColor("red")))
                break

    def unrigged(self):
        """Unrig all contestants."""
        for i in range(self.names.count()):
            self.names.item(i).setForeground(QBrush(QColor("black")))
