from .deltakere import Deltakere
from .lyd import Uro

import tkinter as Vindu
import random
import time


class Drikkelek:
    def __init__(self,
                 wait_time,
                 playlist,
                 directory,
                 music,
                 volume):
        """
        Hovedklasse.

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

        self.Lyd = Uro(playlist, directory, music, volume)
        self.modes = [self.musikk_quiz,
                      self.drink_bitch,
                      self.kategorileken,
                      self.mest_sannsynlig,
                      self.waterfall,
                      self.lyric_masteren,
                      self.siste_som,
                      self.beste_grimase,
                      self.mime,
                      self.tommelkrig,
                      self.capture_the_mini]
        self.active_modes = [self.musikk_quiz,
                             self.musikk_quiz,
                             self.drink_bitch,
                             self.kategorileken,
                             self.mest_sannsynlig,
                             self.waterfall,
                             self.lyric_masteren,
                             self.siste_som,
                             self.beste_grimase,
                             self.mime,
                             self.tommelkrig,
                             self.capture_the_mini]

        if type(wait_time) != tuple:
            wait_time = (wait_time, wait_time)
        self.wait_time = (wait_time[0] * 60000, wait_time[1] * 60000)
        self.directory = directory

        self._fortsetter = None
        self._knapp = None

        self.kategorier = []
        with open('../src/norsk_personlig/tekstfiler/kategorier.txt', 'r',
                  encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                self.kategorier.append(line)

        self.mest_sannsynlig_til = []
        with open('../src/norsk_personlig/tekstfiler/sannsynlig_til.txt', 'r',
                  encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                self.mest_sannsynlig_til.append(line)

        self.sangtekster = []
        with open('../src/norsk_personlig/tekstfiler/sangtekster.txt', 'r',
                  encoding='utf-8') as file:
            for line in file:
                info, tekst = line.split(" [] ")
                artist, sang = info.split(", ")
                self.sangtekster.append((artist, sang, tekst))

        # Add players
        start = Deltakere()
        self.deltakere = start.deltakere

        # Main window
        self.vindu = Vindu.Tk()
        self.vindu.geometry("1920x720+0+0")
        Vindu.Label(self.vindu, text='Hobozz Drikkelek', font=('Helvetica bold', 40)).place(x=0,
                                                                                            y=0)

        # Pause Button
        Vindu.Button(self.vindu, text='PAUSE MUSIKK',
                     command=lambda: self.Lyd.pause_music()).place(x=0, y=80)

        # Play Button
        Vindu.Button(self.vindu, text='SPILL MUSIKK',
                     command=lambda: self.Lyd.unpause_music()).place(x=150, y=80)

        # Play Button
        Vindu.Button(self.vindu, text='SKIP SANG',
                     command=lambda: self.Lyd.skip_music()).place(x=300, y=80)

        # Players
        Vindu.Label(self.vindu, text='Deltakere:', font=('Helvetica', 30)).place(x=0, y=160)

        player_lable_distance = 200
        for player in self.deltakere:
            Vindu.Label(self.vindu, text=f" >  {player}",
                        font=('Helvetica', 16)).place(x=0, y=player_lable_distance)
            player_lable_distance += 30

        # Starting the game
        Vindu.Button(self.vindu, text='START',
                     command=lambda: self._start_game(), fg='Green').place(x=500, y=80)

        # Adding a new mode
        Vindu.Label(self.vindu, text="LEGG TIL").place(x=700, y=80)

        pos = 80
        for mode in self.modes:
            pos += 50
            Vindu.Button(self.vindu, text=mode.__name__,
                          command=lambda mode=mode: self._add_mode(mode)).place(x=700, y=pos)

        # Removing a mode
        Vindu.Label(self.vindu, text="FJERN").place(x=850, y=80)

        pos = 80
        for mode in self.modes:
            pos += 50
            Vindu.Button(self.vindu, text=mode.__name__,
                          command=lambda mode=mode: self._remove_mode(mode)).place(x=850, y=pos)

        # Active modes
        Vindu.Label(self.vindu, text="AKTIVE:").place(x=1000, y=80)

        pos = 110
        self.active_labels = []
        for mode in self.active_modes:
            pos += 20
            label = Vindu.Label(self.vindu, text=mode.__name__,
                                 font=("Helvetica", 10))
            label.place(x=1000, y=pos)
            self.active_labels.append(label)

        self.vindu.mainloop()

    def _add_mode(self, mode):
        """Adds a game mode."""

        self.active_modes.append(mode)

        for label in self.active_labels:
            label.destroy()

        pos = 110
        self.active_labels = []
        for game in self.active_modes:
            pos += 20
            label = Vindu.Label(self.vindu, text=game.__name__,
                                 font=("Helvetica", 10))
            label.place(x=1000, y=pos)
            self.active_labels.append(label)

    def _remove_mode(self, mode):
        """Removes a game mode."""

        while mode in self.active_modes:
            self.active_modes.remove(mode)

        for label in self.active_labels:
            label.destroy()

        pos = 110
        self.active_labels = []
        for game in self.active_modes:
            pos += 20
            label = Vindu.Label(self.vindu, text=game.__name__,
                                 font=("Helvetica", 10))
            label.place(x=1000, y=pos)
            self.active_labels.append(label)

        self.vindu.mainloop()

    def _start_game(self):
        """Starts the game."""

        self.Lyd.pause_music()

        self.Lyd.read('Velkommen til hobozzz drikkeleken, dette blir gay!')

        self.Lyd.read('Deltakerne i dag er')
        self.Lyd.read(", ".join(self.deltakere))

        self.Lyd.read('Let the games begin!')

        self.Lyd.unpause_music()

        self._game_loop()

    def _game_loop(self):
        """The game loop."""

        random.choice(self.active_modes)()

        vent = random.randint(self.wait_time[0], self.wait_time[1])
        self.vindu.after(vent, self._game_loop)

    def drink_bitch(self):
        """Drink bitch game mode."""

        the_bitch = random.choice(self.deltakere)

        self.Lyd.pause_music()

        self.Lyd.read(f'Kan jeg få oppmerksomheten')

        time.sleep(2)

        self.Lyd.read(f'{the_bitch} DRINK, BITCH')
        self.Lyd.read('Takk for meg')

        self.Lyd.unpause_music()

    def musikk_quiz(self):
        """Music quiz game mode."""

        self.Lyd.pause_music()

        self.Lyd.read('Velkommen til musikkquiz')
        t = 'Her kommer 3 sanger. Førstemann til å rope ut sangens navn eller artist kan dele ut 1 til 2 slurker'
        self.Lyd.read(t)

        songs = self.Lyd.music.playlist_tracks("2sbw07iogIXbWpmOz0U66W")["items"]
        random.shuffle(songs)

        for i in range(1, 4):
            if i != 3:
                self.Lyd.read(f'Sang nummer {i}')
            else:
                self.Lyd.read(f'Siste sang')

            song = songs[i]["track"]
            song_id = song["id"]
            song_name = song["name"]
            artist_name = song["artists"][0]["name"]

            self.Lyd.music.add_to_queue(song_id)
            self.Lyd.skip_music()

            time.sleep(25)

            self.Lyd.pause_music()

            time.sleep(1)

            self.Lyd.read_english(f'{song_name} by, {artist_name}')

        burn = random.choice(["at du ser lesbisk ut",
                              "at du er dritflink til å drikke",
                              "at du er en god venn",
                              "at du ikke har et liv",
                              "at du er god i senga",
                              "at du kan mye",
                              "at du får dele ut 3 slurker",
                              "at du får drikke 3 slurker",
                              "at du får dele ut 1 slurk",
                              "at du får drikke 1 slurk",
                              "at du får dele ut 2 slurker",
                              "at du får drikke 2 slurker"])
        t = f'Det var sang quizen, takk for deltakelsen, Bull hvis du klarte alle sangene kan du trøste deg med {burn}.'
        self.Lyd.read(t)

        self.Lyd.skip_music()
        self.Lyd.unpause_music()

    def _fortsett(self):
        """Continues the game."""

        self._fortsetter = True
        self._knapp.destroy() if self._knapp else None
        self.vindu.update()

    def kategorileken(self):
        """Category game mode."""

        self.Lyd.pause_music()

        kategori = random.choice(self.kategorier)
        startperson = random.choice(self.deltakere)

        self.Lyd.read('Dette er kategori leken')
        self.Lyd.read("Trykk for å fortsette")

        self.Lyd.read('Kategorien er:')
        self.Lyd.read(f'{kategori}, {startperson} starter')

        self._fortsetter = False
        self._knapp = Vindu.Button(self.vindu, text='FORTSETT', command=self._fortsett)
        self._knapp.place(x=800, y=80)
        while not self._fortsetter:
            self.vindu.update()

        time.sleep(1)
        self.Lyd.read('Den som tapte må drikke.')

        time.sleep(1)
        self.Lyd.unpause_music()

    def mest_sannsynlig(self):
        """Most likely to game mode."""

        self.Lyd.pause_music()
        self.Lyd.read('Hold kjeftene deres, dette er mest sannsynlig leken')
        t = 'dere stemmer på om den stemmer. Hvis den stemmer må personen drikke, hvis ikke må alle andre drikke.'
        self.Lyd.read(f"Jeg kommer med tre påstander, {t}")

        for i in range(3):
            person = random.choice(self.deltakere)
            handling = random.choice(self.mest_sannsynlig_til)

            self.Lyd.read(f'{person} er den av dere som er mest sannsynlig til {handling}')

            time.sleep(10)

        self.Lyd.unpause_music()

    def waterfall(self):
        """Waterfall game mode."""

        self.Lyd.pause_music()

        self.Lyd.read('Hold de stygge munnene deres og lytt, neste lek er waterfall')

        person = random.choice(self.deltakere)
        self.Lyd.read(f'{person} starter og bestemmer hvilken retning det skal gå')

        time.sleep(2)

        self.Lyd.unpause_music()

    def lyric_masteren(self):
        """Lyric master game mode."""

        self.Lyd.pause_music()
        self.Lyd.read('Velkommen til lyrikkmesteren')
        self.Lyd.read('Jeg skal lese opp en sang for dere. Hvis ingen klarer å gjette sangen må dere drikke')

        artist, sang, tekst = random.choice(self.sangtekster)

        self.Lyd.read_english(tekst.strip())

        time.sleep(5)

        self.Lyd.read(f'Sangen var {sang} av {artist}')

        self.Lyd.unpause_music()

    def siste_som(self):
        """Last person to game."""

        self.Lyd.pause_music()

        self.Lyd.read('Siste som')
        aktivitet = random.choice(["Reiser seg",
                                   "Tar en slurk",
                                   "Tar en high five",
                                   "Tar en shot",
                                   "Snurrer rundt",
                                   "Tar en pushup",
                                   "Tar en situp",
                                   "Rekker opp hånden",
                                   "Dabber"])
        self.Lyd.read(f'{aktivitet}')

        self.Lyd.unpause_music()

    def beste_grimase(self):
        """Best grimace game."""

        self.Lyd.pause_music()

        self.Lyd.read('Pek på den som lager best grimase')

        time.sleep(20)

        aktivitet = random.choice(["Dele ut to slurker",
                                   "Drikke to slurker",
                                   "Ta en shot",
                                   "Dele ut en slurk",
                                   "Drikke en slurk",
                                   "Dele ut en shot",
                                   "Dele ut tre slurker",
                                   "Drikke tre slurker"])

        self.Lyd.read(f"Vinneren får {aktivitet}")

        time.sleep(2)

        self.Lyd.unpause_music()

    def bygge_bokser(self):
        """Den som bygger høyest frittstående vinner."""

        self.Lyd.pause_music()

        self.Lyd.read('Den som bygger høyest frittstående tårn av SINE EGNE tomme ølbokser vinner')

        tid = random.choice([5, 10, 15, 20, 25, 30])

        self.Lyd.read(f'Dere har {tid} sekunder')

        time.sleep(tid)

        self.Lyd.read('Stopp!')

        time.sleep(2)

        aktivitet = random.choice(["Dele ut en slurk",
                                   "Dele ut to slurker",
                                   "Dele ut tre slurker",
                                   "Dele ut like mange slurker som antall bokser"])
        self.Lyd.read(f"Vinneren får {aktivitet}")

        time.sleep(2)

        self.Lyd.unpause_music()

    def karin_henter(self):
        """Karin er tjener!"""

        self.Lyd.pause_music()

        self.Lyd.read('Øl runde!')
        self.Lyd.read('Karin henter drikke til alle som vil ha!')

        time.sleep(15)

        self.Lyd.unpause_music()

    def kaste_snacks(self):
        """Første til å treffe munnen!"""

        self.Lyd.pause_music()

        self.Lyd.read('En og en skal kaste snacks i munnen')
        self.Lyd.read('Første til å kaste og treffe munnen med snacks vinner')
        self.Lyd.read(f"{random.choice(self.deltakere)} starter")
        self.Lyd.read("Trykk for å fortsette")

        self._fortsetter = False
        self._knapp = Vindu.Button(self.vindu, text='FORTSETT', command=self._fortsett)
        self._knapp.place(x=800, y=80)
        while not self._fortsetter:
            self.vindu.update()

        handling = random.choice(["Vinneren får dele ut en slurk",
                                  "Vinneren får dele ut to slurker",
                                  "Vinneren får dele ut tre slurker",
                                  "De som ikke traff munnen må drikke!",
                                  "Alle må drikke antall slurker det tok før vinneren traff",
                                  "Alle unntatt vinneren må drikke antall slurker det tok",
                                  "Alle må drikke like mange slurker som de selv bommet"])

        self.Lyd.read(handling)

        time.sleep(5)

        self.Lyd.unpause_music()

    def mime(self):
        """Mime game."""

        self.Lyd.pause_music()

        self.Lyd.read('Mimelek, tenk på hva du skal mime!')

        time.sleep(5)

        self.Lyd.read(f'{random.choice(self.deltakere)} skal mime, og har 30 sekunder på seg.')

        time.sleep(30)

        self.Lyd.read('Stopp!')
        self.Lyd.read('De som ikke klarte å gjette må drikke. Hvis ingen klarte det må mimeren drikke.')

        time.sleep(2)

        self.Lyd.unpause_music()

    def tommelkrig(self):
        """Thumb war game."""

        self.Lyd.pause_music()

        person_1, person_2 = random.sample(self.deltakere, 2)

        self.Lyd.read(f'Tommelkrig mellom {person_1} og {person_2}!')

        aktivitet = random.choice(["Dele ut to slurker",
                                   "Drikke to slurker",
                                   "Ta en shot",
                                   "Dele ut en slurk",
                                   "Drikke en slurk",
                                   "Dele ut en shot",
                                   "Dele ut tre slurker",
                                   "Drikke tre slurker"])
        self.Lyd.read(f'Den som taper må {aktivitet}')

        time.sleep(20)

        self.Lyd.unpause_music()

    def andreas_round(self):
        """Andreas game."""

        self.Lyd.pause_music()

        self.Lyd.read('Andreas sin runde!')

        time.sleep(2)

        self.Lyd.read("Hvilken sang er dette?")

        time.sleep(1)

        self.Lyd.unpause_music()

    def capture_the_mini(self):
        """Dwarf game."""

        self.Lyd.pause_music()

        self.Lyd.read('Klask den nærmeste minien!')

        time.sleep(2)

        handling = random.choice(["Drikk en slurk",
                                  "Dele ut en slurk",
                                  "Drikke antall klask hen fikk",
                                  "Ingenting, fordi Karin skal drikke to slurker uansett"])

        self.Lyd.read(f'Den som flest klaska får {handling}')

        self.Lyd.unpause_music()
