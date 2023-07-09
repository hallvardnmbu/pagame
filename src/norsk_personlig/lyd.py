from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from gtts import gTTS
import pygame
import os
import time


class Uro:
    def __init__(self, playlist, directory, music, volume):
        self.playlist = playlist
        self.directory = directory

        client_id, client_secret, redirect_uri = music
        self.music = Spotify(auth_manager=SpotifyOAuth(scope="user-read-playback-state user-modify-playback-state",
                                                       client_id=client_id,
                                                       client_secret=client_secret,
                                                       redirect_uri=redirect_uri))
        self.music.volume(volume)
        self._play_music()

    def _play_music(self):
        """Starts the music."""

        self.music.start_playback(context_uri=self.playlist)
        self.music.shuffle(state=True)

    def pause_music(self):
        """Pause the music."""

        self.music.pause_playback()

    def unpause_music(self):
        """Unpause the music."""

        self.music.start_playback(uris=None)

    def skip_music(self):
        """Skips the current song."""

        self.music.next_track()

    def read(self, text):
        """Reads the text out loud."""

        time.sleep(0.5)

        audio = gTTS(text=text, lang="no", slow=False)

        audio.save(f'{self.directory}speak.mp3')

        pygame.mixer.init()
        pygame.mixer.music.load(f"{self.directory}speak.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

        os.remove(f'{self.directory}speak.mp3')

    def read_english(self, text):
        """Reads the text out loud."""

        time.sleep(0.5)

        audio = gTTS(text=text, lang="en", slow=False)

        audio.save(f'{self.directory}speak.mp3')

        pygame.mixer.init()
        pygame.mixer.music.load(f"{self.directory}speak.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

        os.remove(f'{self.directory}speak.mp3')
