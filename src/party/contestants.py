from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QListWidget


BUTTON_SIZE = 55


class Contestants(QWidget):
    def __init__(self):
        super().__init__()

        self.contestants = []

        layout = QVBoxLayout()
        top = QHBoxLayout()

        self.entry = QLineEdit()
        self.entry.setPlaceholderText("Name")
        self.entry.setFixedHeight(int(BUTTON_SIZE * 0.5))
        top.addWidget(self.entry)
        top.addSpacing(10)

        add = QPushButton("Include")
        add.setFixedSize(int(BUTTON_SIZE * 1.5), int(BUTTON_SIZE * 0.5))
        add.clicked.connect(self._add)
        top.addWidget(add)

        layout.addLayout(top)

        self.names = QListWidget()
        self.names.setFixedHeight(int(BUTTON_SIZE * 1.5))
        self.names.itemClicked.connect(self._remove)
        layout.addWidget(self.names)

        self.setLayout(layout)

    def _add(self):
        name = self.entry.text()
        if name:
            self.names.addItem(name)
            self.contestants.append(name) if name not in self.contestants else None
            self.entry.clear()

    def _remove(self, item):
        self.names.takeItem(self.names.row(item))
        self.contestants.remove(item.text())
