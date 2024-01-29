import os
import time
import pygame
from gtts import gTTS
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth


VOLUME = 75


class Noise:
    def __init__(self, playlist, directory, spotify):
        """
        A class that handles the music and text-to-speech.

        Parameters
        ----------
        playlist : str
            The playlist to play, must be a Spotify URI.
        directory : str
            The directory to save (and play from) the mp3 files.
        spotify : dictionary
            The Spotify client id, client secret and redirect uri.
        """
        self.playlist = playlist
        self.directory = directory if directory[-1] == "/" else f"{directory}/"

        try:
            self.music = Spotify(
                auth_manager=SpotifyOAuth(
                    scope="user-read-playback-state user-modify-playback-state",
                    **spotify
                )
            )
            self.music.volume(VOLUME)
            self._play_music()
        except:  # noqa
            self.music = None

    def _play_music(self):
        """Starts the music."""
        if self.music and not self.music.current_playback()["is_playing"]:
            self.music.start_playback(context_uri=self.playlist)
            self.music.shuffle(state=True)

    def pause_music(self):
        """Pause the music."""
        if self.music and self.music.current_playback()["is_playing"]:
            self.music.pause_playback()

    def unpause_music(self):
        """Unpause the music."""
        if self.music and not self.music.current_playback()["is_playing"]:
            self.music.start_playback(uris=None)

    def skip_music(self):
        """Skips the current song."""
        if self.music:
            self.music.next_track()

    def read(self, text, language="en"):
        """
        Reads the text out loud.

        Parameters
        ----------
        text : str
            The text to read.
        language : str, optional
        """
        time.sleep(0.5)

        audio = gTTS(text=text, lang=language, slow=False)
        audio.save(f'{self.directory}speak.mp3')

        pygame.mixer.init()
        pygame.mixer.music.load(f"{self.directory}speak.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

        os.remove(f'{self.directory}speak.mp3')
