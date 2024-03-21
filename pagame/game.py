from .draw import Draw
from .settings import Settings
from .sound import Noise, VOLUME
from .contestants import Contestants, BUTTON_SIZE

import os
import sys
import time
import random
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget,
                             QWidget, QListWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QComboBox, QGroupBox, QSlider, QLabel)


_dir = os.path.dirname(os.path.abspath(__file__))
ICONS = str(sys._MEIPASS) if getattr(sys, 'frozen', False) else os.path.join(_dir, "lookup", "icons")
TEXTFILES = str(sys._MEIPASS) if getattr(sys, 'frozen', False) else os.path.join(_dir, "lookup", "textfiles")


class Play:
    def __init__(self, delay=(2, 5), language="en", music=None):
        app = QApplication([])
        app.setStyleSheet("""
            QMainWindow {
                background-color: #E5E5E5;
            }
            QWidget {
                font-family: 'Courier New', Courier, monospace;
                background-color: #E5E5E5;
            }
            QTabWidget::pane {
                background-color: #E5E5E5;
            }
            QTabWidget::tab-bar {
                left: 22px;
                top: 10px;
            }
            QTabBar::tab {
                background: #E5E5E5;
                border: 1px solid gray;
                border-radius: 4px;
                min-width: 8ex;
                padding: 2px;
                color: black;
            }
            QTabBar::tab:selected {
                background: #FBFAF5;
            }
            QPushButton {
                border: 1px solid gray;
                border-radius: 4px;
                background-color: #FBFAF5;
                color: black;
                font-family: 'Courier New', Courier, monospace;
            }
            QPushButton:hover {
                background-color: #E5E5E5;
            }
            QPushButton:pressed {
                background-color: #D6D5D1;
            }
            QGroupBox {
                border: 1px solid gray;
                border-radius: 4px;
                margin-top: 0.5em;
                color: black;
                font-family: 'Courier New', Courier, monospace;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
                color: black;
            }
            QListWidget {
                border: 1px solid gray;
                border-radius: 4px;
                background-color: #FBFAF5;
                color: black;
                font-family: 'Courier New', Courier, monospace;
            }
            QListWidget::item:selected {
                background-color: #FBFAF5;
                color: black;
            }
            QListWidget::item:hover {
                background-color: #E5E5E5;
            }
            QListWidget QScrollBar:vertical {
                background: transparent;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QListWidget QScrollBar::handle:vertical {   
                border: 1px solid gray;
                background: transparent;
                min-height: 0px;
            }
            QLineEdit {
                border: 1px solid gray;
                border-radius: 4px;
                background-color: #FBFAF5;
                color: black;
                font-family: 'Courier New', Courier, monospace;
            }
            QComboBox {
                border: 1px solid gray;
                border-radius: 4px;
                background-color: #FBFAF5;
                color: black;
                font-family: 'Courier New', Courier, monospace;
            }
            QComboBox::drop-down {
                border: 1px solid gray;
                border-radius: 2px;
                background-color: #E5E5E5;
                width: 10px;
            }
            QComboBox::drop-down:hover {
                background-color: #FBFAF5;
            }
            QComboBox::item:selected {
                background-color: #ECEBE5;
                color: black;
            }
            QComboBox::item {
                background-color: #FBFAF5;
                color: gray;
            }
            QLabel {
                color: black;
                font-family: 'Courier New', Courier, monospace;
            }
            QSlider::groove:horizontal {
                border: 1px solid gray;
                background: #FBFAF5;
                border-radius: 5px;
                height: 20px;
                margin: 0px;
            }
            QSlider::handle:horizontal {
                background-color: #E5E5E5;
                border: 1px solid gray;
                width: 10px;
                margin: -15px 0px;
            }
        """)

        app.setWindowIcon(QIcon(ICONS + "/icon.ico"))

        if not music:
            music = {
                "playlist": "spotify:playlist:6TutgaHFfkThmrrobwA2y9",
                "spotify": {
                    "client_id": None,
                    "client_secret": None,
                    "redirect_uri": "http://localhost:3000/callback"
                }
            }

        window = Interface(delay, language, music)
        window.show()
        app.exec_()


class Interface(QMainWindow):
    """The game class controlling everything."""
    def __init__(self, delay, language, music):
        super().__init__()

        self.parameters = {
            "delay": delay,
            "language": language,
            "music": music,

            "previous": 0,
        }

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.game = Game(delay, language, music)
        self.settings = Settings(self, music)

        self.tabs.addTab(self.info(), "Help")
        self.tabs.addTab(self.settings, "Settings")
        self.tabs.addTab(self.game, "Game")

        self.tabs.setCurrentIndex(1)

    def info(self):
        """Adds information to the layout."""
        window = QWidget()

        layout = QVBoxLayout()

        information = QGroupBox()

        content = QVBoxLayout()

        steps = QLabel("<strong>Spotify credentials</strong><br><br>"
                       "1. Go to <a href='https://developer.spotify.com/dashboard/create'>"
                       "https://developer.spotify.com/dashboard/create</a><br><br>"
                       "2. Enter the following information:<br><br>"
                       "&nbsp;&nbsp;&nbsp;&nbsp;Redirect URI: http://localhost:3000/callback<br>"
                       "&nbsp;&nbsp;&nbsp;&nbsp;API: Web API<br><br>"
                       "3. Click 'Save'.<br><br>"
                       "4. Click 'Settings'.<br><br>"
                       "5. Copy the 'Client ID' and 'Client Secret' into the fields in the "
                       "'Settings' tab.")
        steps.setAlignment(Qt.AlignLeft)
        steps.setOpenExternalLinks(True)
        steps.setWordWrap(True)
        steps.setStyleSheet("""
            color: black; 
            background-color: #FBFAF5;
            font-family: 'Courier New', Courier, monospace;
        """)

        content.addWidget(steps)

        information.setLayout(content)
        information.setObjectName("information")
        information.setStyleSheet("""
            QWidget#information {
                border: 1px solid gray;
                border-radius: 4px;
                background-color: #FBFAF5;
            }
        """)

        layout.addSpacing(20)
        layout.addWidget(information)
        layout.addStretch()
        window.setLayout(layout)

        return window


class Game(QWidget):
    """The game class controlling everything."""
    def __init__(self, delay, language, music):
        super().__init__()

        self.difficulty = "Normal"
        self.action = {
            "Weak": ["half a sip.", "1 sip.", "one and a half sips.", "2 sips."],
            "Normal": ["1 sip.", "2 sips.", "3 sips.", "4 sips."],
            "Hardcore": [f"{i} sips." for i in range(2, 9)],
        }
        self.rigged = False

        self.volume = VOLUME
        self.Sound = Noise(
            language=language,
            spotify=music["spotify"]
        )
        self.Contestants = Contestants()

        self.modes = {
            getattr(self, mode).__name__.replace("_", " ").capitalize(): getattr(self, mode)
            for mode in set(dir(self)) - set(dir(QMainWindow))
            if not mode.startswith("_") and callable(getattr(self, mode))
        }
        custom = {k: v for k, v in self.modes.items() if k.endswith("x")}
        self.modes = {k: v for k, v in sorted(self.modes.items(), key=lambda x: x[0])
                      if k not in custom}
        custom = {f"({(k.replace(' x', ''))})": v for k, v in custom.items()}
        self.modes.update(custom)

        if not self.Sound.music:
            self.modes = {k: v for k, v in self.modes.items() if not "music" in k.lower()}

        self.delay = tuple(int(i * 60000)
                           for i in (delay if isinstance(delay, tuple) else (delay, delay)))
        self.delay = (min(self.delay), max(self.delay))

        self._delay = QLabel(str(self.delay[0] // 60000))
        self._width = None

        self._continue = None
        self._timer = None

        self._textfiles()
        self._graphics()

    def _difficulty(self, mode):
        """Changes the gamemode."""
        self.difficulty = mode if mode != "Rigged" else "Hardcore"

        if mode == "Rigged" and self.Contestants.contestants:
            self.Contestants.unrigged()

            contestants = self.Contestants.contestants

            if any("an" in contestant.lower() for contestant in contestants):
                person = [contestant for contestant in contestants if "an" in contestant.lower()][0]
            else:
                person = random.choice(contestants)

            self.rigged = person

            self.Contestants.rigged(person)
        elif mode == "Rigged":
            self.rigged = None
        else:
            self.rigged = False

    def _textfiles(self):
        """Reads the textfiles."""
        self.categories = []
        # with importlib.resources.open_text('pagame.lookup.textfiles', 'categories.txt') as file:
        with open(TEXTFILES + "/categories.txt", "r") as file:
            for line in file:
                line = line.strip()
                self.categories.append(line)

        self.most_likely_to = []
        # with importlib.resources.open_text('pagame.lookup.textfiles', 'likely_to.txt') as file:
        with open(TEXTFILES + "/likely_to.txt", "r") as file:
            for line in file:
                line = line.strip()
                self.most_likely_to.append(line)

        self.lyrics = []
        # with importlib.resources.open_text('pagame.lookup.textfiles', 'lyrics.txt') as file:
        with open(TEXTFILES + "/lyrics.txt", "r") as file:
            for line in file:
                info, text = line.split(" [] ")
                artist, song = info.split(", ")
                self.lyrics.append((artist, song, text))

    def _graphics(self):
        """Creates the GUI."""
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self._graphics_top()
        self._graphics_bottom()

    def _graphics_top(self):
        """Creates the top part of the GUI."""
        top = QHBoxLayout()

        left = QGroupBox("Controls")
        controls = QVBoxLayout()
        playback = QHBoxLayout()
        feedback = QHBoxLayout()

        pause = QPushButton()
        pause.setIcon(QIcon(ICONS + "/pause.png"))
        pause.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        pause.clicked.connect(self.Sound.pause_music)  # noqa
        playback.addWidget(pause)

        play = QPushButton()
        play.setIcon(QIcon(ICONS + "/play.png"))
        play.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        play.clicked.connect(self.Sound.unpause_music)  # noqa
        playback.addWidget(play)

        skip = QPushButton()
        skip.setIcon(QIcon(ICONS + "/skip.png"))
        skip.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        skip.clicked.connect(self.Sound.skip_music)  # noqa
        playback.addWidget(skip)

        down = QPushButton()
        down.setIcon(QIcon(ICONS + "/volume-down.png"))
        down.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        down.clicked.connect(self._decrease_volume)  # noqa
        feedback.addWidget(down)

        up = QPushButton()
        up.setIcon(QIcon(ICONS + "/volume-up.png"))
        up.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        up.clicked.connect(self._increase_volume)  # noqa
        feedback.addWidget(up)

        self.button_start = QPushButton("START")
        self.button_start.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        self.button_start.clicked.connect(self._start_game)  # noqa
        feedback.addWidget(self.button_start)

        self.button_continue = QPushButton()
        self.button_continue.setIcon(QIcon(ICONS + "/continue.png"))
        self.button_continue.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        self.button_continue.clicked.connect(self._pass)  # noqa
        self.button_continue.hide()
        feedback.addWidget(self.button_continue)

        self.button_disable = QPushButton()
        self.button_disable.setIcon(QIcon(ICONS + "/power.png"))
        self.button_disable.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        self.button_disable.clicked.connect(self._disable)  # noqa
        self.button_disable.hide()
        feedback.addWidget(self.button_disable)

        playback.setSpacing(20)
        feedback.setSpacing(20)
        controls.addLayout(playback)
        controls.addLayout(feedback)

        left.setLayout(controls)
        left.setObjectName("left")
        left.setStyleSheet("""
            QWidget#left {
                border: 1px solid gray;
                border-radius: 4px;
            }
        """)
        top.addWidget(left)

        right = QGroupBox("Contestants")
        inside = QVBoxLayout()
        inside.addWidget(self.Contestants)
        right.setLayout(inside)
        right.setFixedWidth(BUTTON_SIZE * 5)
        right.setObjectName("right")
        right.setStyleSheet("""
            QWidget#right {
                border: 1px solid gray;
                border-radius: 4px;
            }
        """)
        top.addWidget(right)

        self.layout.addSpacing(20)
        self.layout.addLayout(top)

    def _graphics_bottom(self):
        """Creates the bottom part of the GUI."""
        bottom = QHBoxLayout()

        left = QVBoxLayout()

        left_top = QGroupBox("Add game")
        addition = QVBoxLayout()

        self.adding = QComboBox()
        self.adding.addItems(self.modes.keys())
        self.adding.setFixedHeight(BUTTON_SIZE // 2)

        add = QPushButton()
        add.setIcon(QIcon(ICONS + "/add.png"))
        add.clicked.connect(lambda: self._add_mode(self.adding.currentText()))  # noqa
        add.setFixedHeight(BUTTON_SIZE)

        addition.addWidget(self.adding)
        addition.addWidget(add)

        left_top.setLayout(addition)
        left_top.setObjectName("left_top")
        left_top.setStyleSheet("""
            QWidget#left_top {
                border: 1px solid gray;
                border-radius: 4px;
            }
        """)

        left_bottom = QGroupBox("Game delay (minutes)")
        delay = QHBoxLayout()

        _delay = QSlider(Qt.Horizontal)
        _delay.setMinimum(1)
        _delay.setMaximum(25)
        _delay.setValue(2)
        _delay.valueChanged.connect(self._delay_change)

        self._delay.setFixedWidth(BUTTON_SIZE // 2)
        self._delay.setAlignment(Qt.AlignCenter)

        delay.addWidget(self._delay)
        delay.addWidget(_delay)
        left_bottom.setLayout(delay)

        left.addWidget(left_top)
        left.addWidget(left_bottom)

        bottom.addLayout(left)

        right = QGroupBox("Active games")
        activated = QVBoxLayout()

        self.activated = QListWidget()
        self.activated.itemClicked.connect(self._remove_mode)  # noqa
        for mode in self.modes:
            self.activated.addItem(mode) if not mode.startswith("(") else None
        self.activated.sortItems()
        activated.addWidget(self.activated)

        right.setLayout(activated)
        bottom.addWidget(right)

        self.layout.addLayout(bottom)

    def _delay_change(self, value):
        """Changes the delay."""
        self.delay = (int(value * 60000), int(value * 60000))
        self._delay.setText(str(value))

    def _increase_volume(self):
        """Increases the volume."""
        self.volume = min(self.volume + 5, 100)
        try:
            self.Sound.music.volume(self.volume)
        except AttributeError:
            pass

    def _decrease_volume(self):
        """Decreases the volume."""
        self.volume = max(self.volume - 5, 0)
        try:
            self.Sound.music.volume(self.volume)
        except AttributeError:
            pass

    def _add_mode(self, mode):
        """Adds a game mode."""
        self.activated.addItem(mode)
        self.activated.sortItems()

    def _remove_mode(self, mode):
        """Renmoves a game mode."""
        self.activated.takeItem(self.activated.row(mode))

    def _start_game(self):
        """Starts the game."""
        if len(self.Contestants.contestants) < 2:
            self.Sound.read("Dude... You can't seriously be trying to play this alone.")

            if self.Sound.music:
                self.Sound.music.volume(100)
                self.Sound.music.start_playback(uris=["spotify:track:0nr2FxkTgIwCjDdUC50gPI"])
                self.Sound.music.repeat("track")

            return

        self._difficulty(self.difficulty)

        self.button_start.hide()
        self.button_disable.show()

        self.Sound.pause_music()

        self.Sound.read("Welcome to the drinking;")
        self.Sound.read(' and '.join(self.Contestants.contestants), override=True)
        self.Sound.read("Let the games begin!")

        self.Sound.unpause_music()

        self.timer = QTimer()  # noqa
        self.timer.timeout.connect(self._game_loop)  # noqa
        self.timer.start(1000)

    def _game_loop(self):
        """The game loop."""
        if self.rigged is None:
            self._difficulty("Rigged")

        try:
            index = random.randint(0, self.activated.count() - 1)
            self.modes[self.activated.item(index).text()]()
        except ValueError:
            pass

        wait = random.randint(self.delay[0], self.delay[1])
        self.timer.start(wait)

    def _pass(self):
        """Continues the game."""
        self._continue = True
        self.button_continue.hide()
        self.button_disable.show()

    def _disable(self):
        """Disables the game."""
        self.timer.stop()
        self._continue = False
        self.button_disable.hide()
        self.button_continue.show()

        def continues():
            if not self._continue:
                return

            self.timer.start(1000)
            self._timer.stop()

        self._timer = QTimer()
        self._timer.timeout.connect(continues)  # noqa
        self._timer.start(12000)

    def _sound_change(self):
        self.modes = {
            getattr(self, mode).__name__.replace("_", " ").capitalize(): getattr(self, mode)
            for mode in set(dir(self)) - set(dir(QMainWindow))
            if not mode.startswith("_") and callable(getattr(self, mode))
        }
        custom = {k: v for k, v in self.modes.items() if k.endswith("x")}
        self.modes = {k: v for k, v in sorted(self.modes.items(), key=lambda x: x[0])
                      if k not in custom}
        custom = {f"({(k.replace(' x', ''))})": v for k, v in custom.items()}
        self.modes.update(custom)

        if not self.Sound.music:
            self.modes = {k: v for k, v in self.modes.items() if not "music" in k.lower()}

        self.activated.clear()
        for mode in self.modes:
            self.activated.addItem(mode) if not mode.startswith("(") else None
        self.activated.sortItems()

        self.adding.clear()
        self.adding.addItems(self.modes.keys())

    def draw(self):
        if self.Sound.music:
            playback = self.Sound.music.current_playback()
            volume = playback["device"]["volume_percent"]

        self.Sound.pause_music()

        person = random.choice(self.Contestants.contestants)
        self.Sound.read("Hello... Everyone, look at me!")
        self.Sound.read(f"I am the host of the game, and I would like "
                        f"{person} to draw me a picture.")
        self.Sound.read("The others must guess what it is. "
                        "Close the drawing when you are ready to continue.")

        self.Sound.music.volume(40) if self.Sound.music else None
        self.Sound.unpause_music()

        draw = Draw()
        draw.exec_()

        self.Sound.pause_music()

        self.Sound.read(f"The drawing is done. {person}, what is it?")
        time.sleep(4)

        what = random.choice(self.action[self.difficulty])
        action = random.choice([f"the losers has to drink {what}",
                                f"the losers may hand out {what}",
                                f"the winners may hand out {what}",
                                f"the winners may drink {what}"])
        self.Sound.read(f"If everyone or no-one guessed correctly, the artist has to {what}. "
                        f"Otherwise, {action}")

        self.Sound.unpause_music()
        self.Sound.music.volume(volume) if self.Sound.music else None

    def drink_bitch(self):
        """Drink bitch game mode."""
        the_bitch = self.rigged if self.rigged else random.choice(self.Contestants.contestants)

        self.Sound.pause_music()

        self.Sound.read(f"Could I get your attention, please?")

        time.sleep(2)

        self.Sound.read(f"{the_bitch} drink. Bitch.")

        self.Sound.unpause_music()

    def music_length(self):
        playback = self.Sound.music.current_playback()

        length = playback["item"]["duration_ms"] / 60000
        minutes = int(length)
        seconds = int((length - minutes) * 60)

        volume = playback["device"]["volume_percent"]

        self.Sound.pause_music()
        time.sleep(1)
        self.Sound.read("How long is the song that you just listened to?")

        self.Sound.music.volume(40)
        self.Sound.unpause_music()
        time.sleep(10)
        self.Sound.pause_music()
        self.Sound.volume(volume)

        self.Sound.read(f"The answer is {minutes} minutes and {seconds} seconds.")

        what = random.choice(self.action[self.difficulty])
        action = random.choice([f"drink {what}",
                                f"hand out {what}"])
        self.Sound.read(f"The closest answer wins and that person may {action}.")

    def music_year(self):
        playback = self.Sound.music.current_playback()

        year = playback["item"]["release_date"][:4]
        volume = playback["device"]["volume_percent"]

        self.Sound.pause_music()
        time.sleep(1)
        self.Sound.read("When did the song that you just listened to come out?")

        self.Sound.music.volume(40)
        self.Sound.unpause_music()
        time.sleep(10)
        self.Sound.pause_music()
        self.Sound.volume(volume)

        self.Sound.read(f"The song was from {year}.")

        what = random.choice(self.action[self.difficulty])
        action = random.choice([f"drink {what}",
                                f"hand out {what}"])
        self.Sound.read(f"The closest answer wins and that person may {action}.")

    def music_quiz(self):
        """Music quiz game mode."""
        self.Sound.pause_music()

        self.Sound.read("Welcome to the music quiz.")
        self.Sound.read("I am going to play three songs for you.")
        self.Sound.read("The first person to shout out the name of the song or the artist wins")
        self.Sound.read("and may hand out one to two sips.")

        # Sometimes the ID doesn't match the artist and name:

        songs = self.Sound.music.playlist_tracks("2sbw07iogIXbWpmOz0U66W")["items"]
        random.shuffle(songs)

        for i in range(1, 4):
            if i != 3:
                self.Sound.read(f"Song number {i}")
            else:
                self.Sound.read("Last song")

            song = songs[i]["track"]
            song_id = song["id"]
            song_name = song["name"]
            artist_name = song["artists"][0]["name"]

            self.Sound.music.add_to_queue(song_id)
            self.Sound.skip_music()

            time.sleep(25)

            self.Sound.pause_music()

            time.sleep(1)

            self.Sound.read(f"{song_name} by, {artist_name}", override=True)

        action = random.choice([f"handing out {random.choice(self.action[self.difficulty])}",
                                f"drinking {random.choice(self.action[self.difficulty])}",
                                "the fact that you are great in bed",
                                "the fact that you are a great person",
                                "the fact that you are a great friend"])
        self.Sound.read(f"If you got all correct, you may comfort yourself by {action}.")

        self.Sound.skip_music()

    def categories(self):
        """Category game mode."""
        self.Sound.pause_music()

        category = random.choice(self.categories)
        starting = self.rigged if self.rigged else random.choice(self.Contestants.contestants)

        self.Sound.read("This is the category game.")
        self.Sound.read("Say something within the category until someone fails.")
        self.Sound.read("Click to continue.")

        self.Sound.read("The category is:")
        self.Sound.read(f"{category}, and {starting} is starting.")

        self._continue = False
        self.button_disable.hide()
        self.button_continue.show()

        def continues():
            if not self._continue:
                return

            self._timer.stop()

            time.sleep(1)

            what = random.choice(self.action[self.difficulty])
            action = random.choice([f"drink {what}",
                                    f"hand out {what}"])
            self.Sound.read(f"The loser has to {action}.")

            time.sleep(1)
            self.Sound.unpause_music()

        self._timer = QTimer()
        self._timer.timeout.connect(continues)  # noqa
        self._timer.start(1000)

    def most_likely(self):
        """Most likely to game mode."""
        self.Sound.pause_music()
        self.Sound.read("Shut up! This is the most likely game.")
        self.Sound.read("I will read a statement plus name, and you will decide if it is true.")
        self.Sound.read("If the majority says it is true, the person has to drink.")
        self.Sound.read("If the majority says it is false, the person can give out 3 sips.")

        for i in range(3):
            person = self.rigged if self.rigged else random.choice(self.Contestants.contestants)
            action = random.choice(self.most_likely_to)

            self.Sound.read(f"{person} is the most likely to {action}")

            time.sleep(10)

        self.Sound.unpause_music()

    def waterfall(self):
        """Waterfall game mode."""
        self.Sound.pause_music()

        self.Sound.read("Shut your mouth and pay attention. The next game is waterfall.")

        person = random.choice(self.Contestants.contestants)
        self.Sound.read(f"{person} starts and decides the direction.")

        if self.rigged:
            time.sleep(1)
            self.Sound.read("Hold that thought. I have a special announcement.")
            time.sleep(1)
            self.Sound.read(f"I want the person next to {self.rigged} to start, "
                            f"so that the waterfall ends on {self.rigged}.")

        time.sleep(2)

        self.Sound.unpause_music()

    def lyrical_master(self):
        """Lyricsmaster game mode."""
        self.Sound.pause_music()
        self.Sound.read("Welcome to the lyrical master.")
        self.Sound.read("I will read some lyrics, and you must guess the song.")

        artist, song, text = random.choice(self.lyrics)

        self.Sound.read(text.strip(), override=True)

        time.sleep(5)

        self.Sound.read(f"The song was {song} by {artist}")

        what = random.choice(self.action[self.difficulty])
        action = random.choice([f"drink {what}",
                                f"hand out {what}"])
        self.Sound.read(f"The winner has to {action}.")

        self.Sound.unpause_music()

    def last_to(self):
        """Last person to game."""
        self.Sound.pause_music()

        self.Sound.read("Last person who")
        activity = random.choice(["Dabs",
                                  "Drinks",
                                  "Takes a shot",
                                  "Stands up",
                                  "Lays down"])
        self.Sound.read(f"{activity}")

        time.sleep(2)

        what = random.choice(self.action[self.difficulty])
        action = random.choice([f"drink {what}",
                                f"hand out {what}"])
        self.Sound.read(f"May {action}.")

        self.Sound.unpause_music()

    def grimace(self):
        """Best grimace game."""
        self.Sound.pause_music()

        self.Sound.read("Everyone make a grimace!")

        time.sleep(2)

        self.Sound.read("Point at the person with the best grimace.")

        time.sleep(8)

        what = random.choice(self.action[self.difficulty])
        action = random.choice([f"drink {what}",
                                f"hand out {what}"])
        self.Sound.read(f"The winner must {action}")

        time.sleep(1)

        self.Sound.unpause_music()

    def build(self):
        """Building game."""
        self.Sound.pause_music()

        self.Sound.read("The person to build the highest tower of HIS OWN empty cans wins.")

        delay = random.choice([2, 5, 10, 12, 15, 17])

        self.Sound.read(f"You have {delay} seconds.")

        time.sleep(delay)

        self.Sound.read("Stop!")

        time.sleep(2)

        what = random.choice(self.action[self.difficulty])
        action = random.choice([f"drink {what}",
                                f"hand out {what}",
                                "give out the amount of cans in your tower.",
                                "sip the amount of cans in your tower."])
        self.Sound.read(f"The winner must {action}")

        time.sleep(2)

        self.Sound.unpause_music()

    def snacks(self):
        """Throw snacks!"""
        self.Sound.pause_music()

        self.Sound.read("One person at a time must try and throw snacks into their mouth.")
        self.Sound.read("The first person to manage it wins.")
        self.Sound.read(f"{random.choice(self.Contestants.contestants)} starts.")
        self.Sound.read("Click to continue")

        self._continue = False
        self.button_disable.hide()
        self.button_continue.show()

        def continues():
            if not self._continue:
                return

            self._timer.stop()

            what = random.choice(self.action[self.difficulty])
            action = random.choice([f"drink {what}",
                                    f"hand out {what}",
                                    "give out as many sips as tries it took.",
                                    "drink as many sips as tries it took."])
            self.Sound.read(f"The winner must {action}")

            time.sleep(5)

            self.Sound.unpause_music()

        self._timer = QTimer()
        self._timer.timeout.connect(continues)  # noqa
        self._timer.start(1000)

    def mime(self):
        """Mime game."""
        self.Sound.pause_music()

        self.Sound.read("Miming game! Think of what you are going to mime!")

        time.sleep(5)

        delay = random.choice([5, 10, 12, 15, 17, 20])
        self.Sound.read(
            f"{self.rigged if self.rigged else random.choice(self.Contestants.contestants)} "
            f"is miming and has {delay} seconds."
        )

        time.sleep(delay)

        self.Sound.read("Stop!")
        self.Sound.read("Those who could not guess has to drink.")
        self.Sound.read("If no one managed, the mime must drink.")

        time.sleep(2)

        self.Sound.unpause_music()

    def thumb_war(self):
        """Thumb war game."""
        try:
            person_1, person_2 = random.sample(self.Contestants.contestants, 2)
            self.Sound.pause_music()
        except ValueError:
            return

        self.Sound.read(f"Thumb war between {person_1} and {person_2}!")

        what = random.choice(self.action[self.difficulty])
        action = random.choice([f"drink {what}",
                                f"hand out {what}",
                                "give out as many sips as tries it took.",
                                "drink as many sips as tries it took."])
        person = random.choice(["winner", "loser"])
        self.Sound.read(f"The {person} must {action}")

        time.sleep(20)

        self.Sound.unpause_music()

    def slap_the_mini(self):
        """Mini game."""
        self.Sound.pause_music()

        self.Sound.read("Slap the closest mini!")

        time.sleep(2)

        what = random.choice(self.action[self.difficulty])
        action = random.choice([f"drink {what}",
                                f"hand out {what}",
                                "give out as many sips as slaps.",
                                "drink as many sips as slaps."])
        self.Sound.read(f"The slapped minis must {action}")

        self.Sound.unpause_music()

    def karin_henter_x(self):
        """Karin er tjener!"""
        self.Sound.pause_music()

        self.Sound.read("Beer-round!")
        self.Sound.read("Karin fetches drinks to everyone that wants!")
        time.sleep(10)

        self.Lyd.unpause_music()

    def andreas_round_x(self):
        """Andreas game."""
        self.Sound.pause_music()

        self.Sound.read("Andreas' round!")
        time.sleep(2)
        self.Sound.read("Which song is this?")
        time.sleep(1)

        self.Sound.unpause_music()
