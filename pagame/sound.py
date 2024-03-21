import os
import time
import pygame
import tempfile
from gtts import gTTS
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from deep_translator import GoogleTranslator
from deep_translator.exceptions import LanguageNotSupportedException


VOLUME = 75


class Noise:
    def __init__(self, language, spotify):
        """
        A class that handles the music and text-to-speech.

        Parameters
        ----------
        language : str
            The language to read text in.
        spotify : dictionary
            The Spotify client id, client secret and redirect uri.
        """
        try:
            self.language = language
            self.translator = GoogleTranslator(source='en', target=language)
        except LanguageNotSupportedException:
            print(f"Language [{language}] not supported. Using default language.")
            self.language = "en"

        try:
            _cache_dir = os.path.join(os.getcwd(), "pagame", "lookup", "_cache")
            os.makedirs(_cache_dir, exist_ok=True)
            _cache_path = os.path.join(_cache_dir, ".cache")

            self.music = Spotify(
                auth_manager=SpotifyOAuth(
                    scope="user-read-playback-state user-modify-playback-state",
                    cache_path=_cache_path,
                    **spotify
                )
            )
            self.music.volume(VOLUME)
        except Exception as e:
            print(spotify)
            print(f"No music device connected.\n > Message: {e}")
            self.music = None

    def play_music(self, playlist):
        """
        Starts the music.

        Parameters
        ----------
        playlist : str, optional
            The playlist to play, uses the default playlist if not provided.
        """
        if not self.music:
            return

        if playlist.startswith("https://open.spotify.com/playlist/"):
            playlist = playlist.split("/")[-1].split("?")[0].split(":")[-1]

        self.music.start_playback(context_uri="spotify:playlist:" + playlist)
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

    def read(self, text, override=False):
        """
        Reads the text out loud.

        Parameters
        ----------
        text : str
            The text to read.
        override : bool, optional
            Whether to override the language setting, by default False.
        """
        time.sleep(0.5)

        if not override and self.language != "en":
            text = self.translator.translate(text=text)

        audio = gTTS(text=text, lang=self.language, slow=False)

        with tempfile.NamedTemporaryFile(delete=True) as sound:
            audio.save(sound.name)

            pygame.mixer.init()
            pygame.mixer.music.load(sound.name)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                continue

    def update(self, id, secret):
        try:
            _cache_dir = os.path.join(os.getcwd(), "pagame", "lookup", "_cache")
            os.makedirs(_cache_dir, exist_ok=True)
            _cache_path = os.path.join(_cache_dir, ".cache")

            self.music = Spotify(
                auth_manager=SpotifyOAuth(
                    scope="user-read-playback-state user-modify-playback-state",
                    cache_path=_cache_path,
                    client_id=id,
                    client_secret=secret,
                    redirect_uri="http://localhost:3000/callback"
                )
            )
            self.music.volume(VOLUME)
        except Exception as e:
            print(f"Failed to connect to Spotify.\n > Message: {e}")
            self.music = None
