from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QListWidget


BUTTON_SIZE = 40


class Contestants(QWidget):
    def __init__(self):
        super().__init__()

        self.contestants = []

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("Name:"))

        self.entry = QLineEdit()
        layout.addWidget(self.entry)

        self.add = QPushButton("Add")
        self.add.setFixedHeight(BUTTON_SIZE)
        self.add.setStyleSheet("background-color: #FBFAF5;")
        self.add.clicked.connect(self._add)
        layout.addWidget(self.add)

        self.names = QListWidget()
        self.names.itemClicked.connect(self._remove)
        layout.addWidget(self.names)

    def _add(self):
        name = self.entry.text()
        if name:
            self.names.addItem(name)
            self.contestants.append(name) if name not in self.contestants else None
            self.entry.clear()

    def _remove(self, item):
        self.names.takeItem(self.names.row(item))
        self.contestants.remove(item.text())
