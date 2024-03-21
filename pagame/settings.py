from PyQt5.QtCore import Qt
from gtts import lang as speech
from deep_translator import GoogleTranslator
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout,
                             QGroupBox, QPushButton, QLineEdit, QComboBox)

from .contestants import BUTTON_SIZE


class Settings(QWidget):
    """Class entering Spotify credentials."""
    def __init__(self, interface, music):
        super().__init__()
        self.interface = interface

        self.id = None
        self.secret = None
        self.language = None
        self.playlist = None
        self.custom_playlist = None
        self.save = None
        self.difficulty = None

        self.playlists = {
            "Disco Hits": "5B3gb8HbvFm02ccQVH33IO",
            "Soft Rock": "37i9dQZF1DX6xOPeSOGone",
            "Heavy Metal": "37i9dQZF1DX9qNs32fujYe",
            "Andreas «vors» style": "6TutgaHFfkThmrrobwA2y9",
            "Sol og sour": "3b3kSFIjetuBb4OHx8APc4",
            "Gucci": "3Fj02sUHhIVRWvoJpdWddT",
            "Girl disco": "0UZZ621jxVtzR09zxufSKX",
            "Psychedelic rock": "0XH1JLrIyQn2p9XWqNFAcC",
        }

        self.input(music)

    def input(self, music):
        """Sets up the layout."""
        layout = QVBoxLayout()

        credentials = QGroupBox("Credentials")
        _credentials = QVBoxLayout()

        id = QHBoxLayout()
        self.id = QLineEdit()
        self.id.setPlaceholderText("Spotify id")
        self.id.setText(
            music["spotify"]["client_id"] if music["spotify"]["client_id"] else None
        )
        self.id.setFixedHeight(int(BUTTON_SIZE * 0.5))
        self.id.setAlignment(Qt.AlignCenter)
        id.addWidget(self.id)

        secret = QHBoxLayout()
        self.secret = QLineEdit()
        self.secret.setText(
            music["spotify"]["client_secret"] if music["spotify"]["client_secret"] else None
        )
        self.secret.setPlaceholderText("Spotify secret")
        self.secret.setFixedHeight(int(BUTTON_SIZE * 0.5))
        self.secret.setAlignment(Qt.AlignCenter)
        secret.addWidget(self.secret)

        save = QPushButton("Update")
        save.setFixedHeight(int(BUTTON_SIZE * 0.5))
        save.clicked.connect(lambda: self._credentials())

        _credentials.addLayout(id)
        _credentials.addLayout(secret)
        _credentials.addWidget(save)

        credentials.setLayout(_credentials)
        credentials.setObjectName("credentials")
        credentials.setStyleSheet("""
            QWidget#credentials {
                border: 1px solid gray;
                border-radius: 4px;
            }
        """)

        difficulty = QGroupBox("Difficulty")
        _difficulty = QHBoxLayout()

        for mode in ["Weak", "Normal", "Hardcore", "Rigged"]:
            button = QPushButton(mode)
            button.setFixedSize(BUTTON_SIZE * 2, BUTTON_SIZE // 2)
            button.clicked.connect(
                lambda checked, button=button: self.interface.game._difficulty(button.text())
            )

            _difficulty.addWidget(button)

        difficulty.setLayout(_difficulty)

        language = QHBoxLayout()
        self.language = QComboBox()
        self.language.setPlaceholderText("Language")
        self.language.addItems(speech.tts_langs().values())
        self.language.setFixedHeight(BUTTON_SIZE // 2)
        self.language.currentTextChanged.connect(lambda lang: self._language(lang))
        language.addWidget(self.language)

        playlist = QVBoxLayout()
        self.playlist = QComboBox()
        self.playlist.setPlaceholderText("Playlist")
        self.playlist.addItems(self.playlists.keys())
        self.playlist.setFixedHeight(BUTTON_SIZE // 2)
        self.playlist.currentTextChanged.connect(lambda play: self._playlist(play))
        playlist.addWidget(self.playlist)

        settings = QGroupBox("Sound")
        _settings = QVBoxLayout()
        __settings = QHBoxLayout()
        __settings.addLayout(language)
        __settings.addLayout(playlist)

        custom_playlist = QHBoxLayout()
        self.custom_playlist = QLineEdit()
        self.custom_playlist.setPlaceholderText("Playlist link")
        self.custom_playlist.setFixedHeight(BUTTON_SIZE // 2)
        self.custom_playlist.setAlignment(Qt.AlignCenter)
        self.custom_playlist.editingFinished.connect(lambda: self._playlist())

        self.save = QPushButton("Play")
        self.save.setFixedSize(BUTTON_SIZE, BUTTON_SIZE // 2)
        self.save.clicked.connect(lambda: self._playlist())

        custom_playlist.addWidget(self.custom_playlist)
        custom_playlist.addWidget(self.save)

        _settings.addLayout(__settings)
        _settings.addLayout(custom_playlist)
        settings.setLayout(_settings)

        layout.addSpacing(20)
        layout.addWidget(difficulty)
        layout.addSpacing(40)
        layout.addWidget(settings)
        layout.addStretch()
        layout.addWidget(credentials)

        self.setLayout(layout)

    def _credentials(self):
        if not (self.id.text() and self.secret.text()):
            return
        self.interface.game.Sound.update(self.id.text(), self.secret.text())

        self.interface.game._sound_change()

    def _playlist(self, play=None):
        play = self.playlists[play] if play else self.custom_playlist.text()
        self.interface.game.Sound.play_music(play) if play else None

        self.playlist.setCurrentIndex(-1)
        if self.custom_playlist.text():
            self.custom_playlist.clear()

        self.interface.game._sound_change()

    def _language(self, language):
        language = [key for key, value in speech.tts_langs().items() if value == language][0]

        self.interface.game.Sound.language = language
        self.interface.game.Sound.translator = GoogleTranslator(source='en', target=language)
