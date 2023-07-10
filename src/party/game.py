from .contestants import Contestants
from .sound import Noise

import tkinter as Window
import random
import time


class Game:
    def __init__(self,
                 wait_time,
                 playlist,
                 directory,
                 music,
                 volume):
        """
        Main class.
        
        Parameters
        ----------
        wait_time : int or tuple
            Minutes between each game.
        playlist : str
            Spotify-URI for the playlist.
        directory : str
            Folder to place and play the sound files.
        music : tuple
            Spotify Client ID, Spotify Client Secret and Spotify-URI for the redirect-page.
        volume : int
            Volume of the music (percentage, 0-100).
        """

        self.Sound = Noise(playlist, directory, music, volume)
        self.modes = [self.music_quiz,
                      self.drink_bitch,
                      self.categories,
                      self.most_likely,
                      self.waterfall,
                      self.lyrical_master,
                      self.last_to,
                      self.grimace,
                      self.mime,
                      self.thumb_war,
                      self.slap_the_mini]
        self.active_modes = [self.music_quiz,
                             self.music_quiz,
                             self.drink_bitch,
                             self.categories,
                             self.most_likely,
                             self.waterfall,
                             self.lyrical_master,
                             self.last_to,
                             self.grimace,
                             self.mime,
                             self.thumb_war,
                             self.slap_the_mini]

        if type(wait_time) != tuple:
            wait_time = (wait_time, wait_time)
        self.wait_time = (wait_time[0] * 60000, wait_time[1] * 60000)
        self.directory = directory

        self._continue = None
        self._button = None

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

        # Add players
        start = Contestants()
        self.contestants = start.contestants

        # Main window
        self.window = Window.Tk()
        self.window.geometry("1920x720+0+0")
        Window.Label(self.window, text="Drinking game", font=("Helvetica bold", 40)).place(x=0, y=0)

        # Pause Button
        Window.Button(self.window, text="PAUSE MUSIC",
                      command=lambda: self.Sound.pause_music()).place(x=0, y=80)

        # Play Button
        Window.Button(self.window, text="UNPAUSE MUSIC",
                      command=lambda: self.Sound.unpause_music()).place(x=150, y=80)

        # Play Button
        Window.Button(self.window, text="SKIP SONG",
                      command=lambda: self.Sound.skip_music()).place(x=300, y=80)

        # Players
        Window.Label(self.window, text="Contestants:", font=("Helvetica", 30)).place(x=0, y=160)

        player_position = 200
        for player in self.contestants:
            Window.Label(self.window, text=f" >  {player}",
                         font=("Helvetica", 16)).place(x=0, y=player_position)
            player_position += 30

        # Starting the game
        Window.Button(self.window, text="START",
                      command=lambda: self._start_game(), fg="Green").place(x=500, y=80)

        # Adding a new mode
        Window.Label(self.window, text="ADD MODE").place(x=700, y=80)

        pos = 80
        for mode in self.modes:
            pos += 50
            Window.Button(self.window, text=mode.__name__,
                          command=lambda: self.active_modes.append(mode)).place(x=700, y=pos)

        # Removing a mode
        Window.Label(self.window, text="REMOVE MODE").place(x=760, y=80)

        pos = 80
        for mode in self.modes:
            pos += 50
            Window.Button(self.window, text=mode.__name__,
                          command=lambda: self._remove_mode(mode)).place(x=760, y=pos)

        self.window.mainloop()

    def _remove_mode(self, mode):
        """Adds a new game mode."""

        while mode in self.active_modes:
            self.active_modes.remove(mode)

    def _start_game(self):
        """Starts the game."""

        self.Sound.pause_music()

        self.Sound.read("Welcome to the drinking")
        self.Sound.read(", ".join(self.contestants))
        self.Sound.read("Let the games begin!")

        self.Sound.unpause_music()

        self._game_loop()

    def _game_loop(self):
        """The game loop."""

        random.choice(self.active_modes)()

        wait = random.randint(self.wait_time[0], self.wait_time[1])
        self.window.after(wait, self._game_loop)

    def drink_bitch(self):
        """Drink bitch game mode."""

        the_bitch = random.choice(self.contestants)

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
        self.Sound.read("and may hand out one to two drinks.")

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

        action = random.choice(["handing out 1 drink",
                                "handing out 2 drinks",
                                "handing out 3 drinks",
                                "drinking 1 drink",
                                "drinking 2 drinks",
                                "drinking 3 drinks",
                                "the fact that you are great in bed",
                                "the fact that you are a great person",
                                "the fact that you are a great friend"])
        self.Sound.read(f"If you got all correct, you can comfort yourself by {action}.")

        self.Sound.skip_music()

    def _pass(self):
        """Continues the game."""

        self._continue = True
        self._button.destroy() if self._button else None
        self.window.update()

    def categories(self):
        """Category game mode."""

        self.Sound.pause_music()

        category = random.choice(self.categories)
        starting = random.choice(self.contestants)

        self.Sound.read("This is the category game.")
        self.Sound.read("Say something within the category until someone fails.")
        self.Sound.read("Click to continue.")

        self.Sound.read("The category is:")
        self.Sound.read(f"{category}, and {starting} is starting.")

        self._continue = False
        self._button = Window.Button(self.window, text="CONTINUE", command=self._pass)
        self._button.place(x=800, y=80)
        while not self._continue:
            self.window.update()

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

    def most_likely(self):
        """Most likely to game mode."""

        self.Sound.pause_music()
        self.Sound.read("Shut up! This is the most likely-game.")
        self.Sound.read("I will read a statement plus name, and you will decide if it is true.")
        self.Sound.read("If the majority says it is true, the person has to drink.")
        self.Sound.read("If the majority says it is false, the person can give out 3 drinks.")

        for i in range(3):
            person = random.choice(self.contestants)
            action = random.choice(self.most_likely_to)

            self.Sound.read(f"{person} is the most likely to {action}")

            time.sleep(10)

        self.Sound.unpause_music()

    def waterfall(self):
        """Waterfall game mode."""

        self.Sound.pause_music()

        self.Sound.read("Shut your mouth and pay attention. The next game is waterfall.")

        person = random.choice(self.contestants)
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
                                "drink the amount of cans in your tower."])
        self.Sound.read(f"The winner must {action}")

        time.sleep(2)

        self.Sound.unpause_music()

    def snacks(self):
        """Throw snacks!"""

        self.Sound.pause_music()

        self.Sound.read("One person at a time must try and throw snacks into their mouth.")
        self.Sound.read("The first person to manage it wins.")
        self.Sound.read(f"{random.choice(self.contestants)} starts.")
        self.Sound.read("Click to continue")

        self._continue = False
        self._button = Window.Button(self.window, text="CONTINUE", command=self._pass)
        self._button.place(x=800, y=80)
        while not self._continue:
            self.window.update()

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

    def mime(self):
        """Mime game."""

        self.Sound.pause_music()

        self.Sound.read("Miming game! Think of what you are going to mime!")

        time.sleep(5)

        delay = random.choice([5, 10, 12, 15, 17, 20])
        self.Sound.read(f"{random.choice(self.contestants)} is miming and has {delay} seconds.")

        time.sleep(delay)

        self.Sound.read("Stop!")
        self.Sound.read("Those who could not guess has to drink.")
        self.Sound.read("If no one managed, the mime must drink.")

        time.sleep(2)

        self.Sound.unpause_music()

    def thumb_war(self):
        """Thumb war game."""

        self.Sound.pause_music()

        person_1, person_2 = random.sample(self.contestants, 2)

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
