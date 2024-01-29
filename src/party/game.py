from .contestants import Contestants, BUTTON_SIZE
from .sound import Noise, VOLUME

from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QWidget, QListWidget)
from PyQt5.QtCore import QTimer
from functools import partial
import random
import time


class Game(QMainWindow):
    def __init__(self, delay, music):
        self.app = QApplication([])
        self.app.setStyleSheet("""
            QPushButton {
                border: 1px solid gray;
                outline: none;
                background-color: #FBFAF5;
            }
        """)
        super().__init__()

        self.volume = VOLUME
        self.Sound = Noise(**music)
        self.Contestants = Contestants()

        self.modes = {
            getattr(self, mode).__name__.replace("_", " ").capitalize(): getattr(self, mode)
            for mode in set(dir(self)) - set(dir(QMainWindow))
            if not mode.startswith("_") and callable(getattr(self, mode))
        }
        self.modes = {k: v for k, v in sorted(self.modes.items(), key=lambda x: x[0])}

        self.delay = tuple(int(i * 60000)
                           for i in (delay if isinstance(delay, tuple) else (delay, delay)))

        self._textfiles()
        self._graphics()

        self.show()
        self.app.exec_()

    def _textfiles(self):
        self.categories = []
        with open("../src/party/textfiles/categories.txt", "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                self.categories.append(line)

        self.most_likely_to = []
        with open("../src/party/textfiles/likely_to.txt", "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                self.most_likely_to.append(line)

        self.lyrics = []
        with open("../src/party/textfiles/lyrics.txt", "r", encoding="utf-8") as file:
            for line in file:
                info, text = line.split(" [] ")
                artist, song = info.split(", ")
                self.lyrics.append((artist, song, text))

    def _graphics(self):
        self.setGeometry(0, 0, 100, 200)

        central = QWidget()
        self.setCentralWidget(central)
        self.setWindowTitle("P4R7Y T13M!")

        self.layout = QVBoxLayout()
        central.setLayout(self.layout)

        self.__top()
        self.__bottom()

    def __top(self):

        top = QHBoxLayout()

        left = QWidget()
        controls = QVBoxLayout()
        playback = QHBoxLayout()
        feedback = QHBoxLayout()

        pause = QPushButton("PAUSE")
        pause.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        pause.clicked.connect(self.Sound.pause_music)
        playback.addWidget(pause)

        play = QPushButton("PLAY")
        play.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        play.clicked.connect(self.Sound.unpause_music)
        playback.addWidget(play)

        skip = QPushButton("SKIP")
        skip.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        skip.clicked.connect(self.Sound.skip_music)
        playback.addWidget(skip)

        up = QPushButton("UP")
        up.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        up.clicked.connect(self._increase_volume)
        feedback.addWidget(up)

        down = QPushButton("DOWN")
        down.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        down.clicked.connect(self._decrease_volume)
        feedback.addWidget(down)

        self.button_start = QPushButton("START")
        self.button_start.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        self.button_start.clicked.connect(self._start_game)
        feedback.addWidget(self.button_start)

        self.button_continue = QPushButton("CONTINUE")
        self.button_continue.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        self.button_continue.clicked.connect(self._pass)
        self.button_continue.hide()
        feedback.addWidget(self.button_continue)

        self.button_disable = QPushButton("DISABLE")
        self.button_disable.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        self.button_disable.clicked.connect(self._disable)
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

        right = QWidget()
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

        self.layout.addLayout(top)

    def _increase_volume(self):
        """Increases the volume."""
        self.volume = min(self.volume + 5, 100)
        self.Sound.music.volume(self.volume)

    def _decrease_volume(self):
        """Decreases the volume."""
        self.volume = max(self.volume - 5, 0)
        self.Sound.music.volume(self.volume)

    def __bottom(self):

        bottom = QHBoxLayout()

        adding = QVBoxLayout()
        adding.addWidget(QLabel("Add a game mode"))
        adding.addSpacing(5)

        for mode in self.modes:
            add = QPushButton(mode)
            add.clicked.connect(partial(self._add_mode, mode))
            add.setFixedSize(int(BUTTON_SIZE * 2.25), int(BUTTON_SIZE * 0.5))
            adding.addWidget(add)
        adding.setSpacing(3)

        bottom.addLayout(adding)

        activated = QVBoxLayout()
        activated.addWidget(QLabel("Currently active game modes"))

        self.activated = QListWidget()
        self.activated.itemClicked.connect(self._remove_mode)
        for mode in self.modes:
            self.activated.addItem(mode)
        self.activated.sortItems()
        activated.addWidget(self.activated)

        bottom.addLayout(activated)

        self.layout.addLayout(bottom)

    def _add_mode(self, mode):
        """Adds a game mode."""
        self.activated.addItem(mode)
        self.activated.sortItems()

    def _remove_mode(self, mode):
        """Renmoves a game mode."""
        self.activated.takeItem(self.activated.row(mode))

    def _start_game(self):
        """Starts the game."""
        self.button_start.hide()
        self.button_disable.show()

        self.Sound.pause_music()

        self.Sound.read("Welcome to the drinking")
        self.Sound.read(", ".join(self.Contestants.contestants))
        self.Sound.read("Let the games begin!")

        self.Sound.unpause_music()

        self.timer = QTimer()
        self.timer.timeout.connect(self._game_loop)
        self.timer.start(1000)

    def _game_loop(self):
        """The game loop."""
        index = random.randint(0, self.activated.count() - 1)
        self.modes[self.activated.item(index).text()]()

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
        self._timer.timeout.connect(continues)
        self._timer.start(12000)

    def drink_bitch(self):
        """Drink bitch game mode."""
        the_bitch = random.choice(self.Contestants.contestants)

        self.Sound.pause_music()

        self.Sound.read(f"Could I get your attention, please?")

        time.sleep(2)

        self.Sound.read(f"{the_bitch} drink. Bitch.")

        self.Sound.unpause_music()

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

            self.Sound.read(f"{song_name} by, {artist_name}")

        action = random.choice(["handing out 1 sip",
                                "handing out 2 sips",
                                "handing out 3 sips",
                                "drinking 1 sip",
                                "drinking 2 sips",
                                "drinking 3 sips",
                                "the fact that you are great in bed",
                                "the fact that you are a great person",
                                "the fact that you are a great friend"])
        self.Sound.read(f"If you got all correct, you can comfort yourself by {action}.")

        self.Sound.skip_music()

    def categories(self):
        """Category game mode."""
        self.Sound.pause_music()

        category = random.choice(self.categories)
        starting = random.choice(self.Contestants.contestants)

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

            action = random.choice(["drink 3 sips.",
                                    "drink 2 sips.",
                                    "drink 1 sip.",
                                    "give out 3 sips.",
                                    "give out 2 sips.",
                                    "give out 1 sip."])
            self.Sound.read(f"The loser has to {action}.")

            time.sleep(1)
            self.Sound.unpause_music()

        self._timer = QTimer()
        self._timer.timeout.connect(continues)
        self._timer.start(1000)

    def most_likely(self):
        """Most likely to game mode."""
        self.Sound.pause_music()
        self.Sound.read("Shut up! This is the most likely-game.")
        self.Sound.read("I will read a statement plus name, and you will decide if it is true.")
        self.Sound.read("If the majority says it is true, the person has to drink.")
        self.Sound.read("If the majority says it is false, the person can give out 3 sips.")

        for i in range(3):
            person = random.choice(self.Contestants.contestants)
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

        time.sleep(2)

        self.Sound.unpause_music()

    def lyrical_master(self):
        """Lyric master game mode."""
        self.Sound.pause_music()
        self.Sound.read("Welcome to the lyrical master.")
        self.Sound.read("I will read some lyrics and you must guess the song.")

        artist, song, text = random.choice(self.lyrics)

        self.Sound.read(text.strip())

        time.sleep(5)

        self.Sound.read(f"The song was {song} by {artist}")

        action = random.choice(["drink 3 sips.",
                                "drink 2 sips.",
                                "drink 1 sip.",
                                "give out 3 sips.",
                                "give out 2 sips.",
                                "give out 1 sip."])
        self.Sound.read(f"The winner has to {action}.")

        self.Sound.unpause_music()

    def last_to(self):
        """Last person to game."""
        self.Sound.pause_music()

        self.Sound.read("Last person to")
        activity = random.choice(["Dabs",
                                  "Drinks",
                                  "Takes a shot",
                                  "Stands up",
                                  "Lays down"])
        self.Sound.read(f"{activity}")

        time.sleep(2)

        action = random.choice(["drink 3 sips.",
                                "drink 2 sips.",
                                "drink 1 sip.",
                                "give out 3 sips.",
                                "give out 2 sips.",
                                "give out 1 sip."])
        self.Sound.read(f"May {action}.")

        self.Sound.unpause_music()

    def grimace(self):
        """Best grimace game."""
        self.Sound.pause_music()

        self.Sound.read("Everyone make a grimace!")

        time.sleep(2)

        self.Sound.read("Point at the person with the best grimace.")

        time.sleep(8)

        action = random.choice(["drink 3 sips.",
                                "drink 2 sips.",
                                "drink 1 sip.",
                                "give out 3 sips.",
                                "give out 2 sips.",
                                "give out 1 sip."])
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

        action = random.choice(["drink 3 sips.",
                                "drink 2 sips.",
                                "drink 1 sip.",
                                "give out 3 sips.",
                                "give out 2 sips.",
                                "give out 1 sip.",
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

            action = random.choice(["drink 3 sips.",
                                    "drink 2 sips.",
                                    "drink 1 sip.",
                                    "give out 3 sips.",
                                    "give out 2 sips.",
                                    "give out 1 sip.",
                                    "give out as many sips as tries it took.",
                                    "drink as many sips as tries it took."])
            self.Sound.read(f"The winner must {action}")

            time.sleep(5)

            self.Sound.unpause_music()

        self._timer = QTimer()
        self._timer.timeout.connect(continues)
        self._timer.start(1000)

    def mime(self):
        """Mime game."""
        self.Sound.pause_music()

        self.Sound.read("Miming game! Think of what you are going to mime!")

        time.sleep(5)

        delay = random.choice([5, 10, 12, 15, 17, 20])
        self.Sound.read(f"{random.choice(self.Contestants.contestants)} is miming and has {delay} seconds.")

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

        action = random.choice(["drink 3 sips.",
                                "drink 2 sips.",
                                "drink 1 sip.",
                                "give out 3 sips.",
                                "give out 2 sips.",
                                "give out 1 sip.",
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

        action = random.choice(["drink 3 sips.",
                                "drink 2 sips.",
                                "drink 1 sip.",
                                "give out 3 sips.",
                                "give out 2 sips.",
                                "give out 1 sip.",
                                "give out as many sips as slaps.",
                                "drink as many sips as slaps."])
        self.Sound.read(f"The slapped minis must {action}")

        self.Sound.unpause_music()
