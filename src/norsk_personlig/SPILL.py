from drikkelek import Drikkelek

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth


"""
_WAIT_TIME : millisekunder mellom hver lek. 
    Enten ett tall eller en tuple (min, max).
_VOLUME : volumet på musikken.
    Prosent, 0-100.
    
_SOUND_DIR : mappen som inneholder lydfilene.
_PLAYLIST : Spotify-URI til spillelisten som skal spilles av.

_SPOTIFY_CLIENT_ID : Spotify Client ID.
_SPOTIFY_CLIENT_SECRET : Spotify Client Secret.
_REDIRECT_URI : Spotify-URI til redirect siden.
"""


_WAIT_TIME = 1000
_VOLUME = 80

_SOUND_DIR = "./lydfiler/"
_PLAYLIST = "spotify:playlist:6TutgaHFfkThmrrobwA2y9"

_SPOTIFY_CLIENT_ID = "0aa4de0a1d4d4f0082ee0e5d8d81b359"
_SPOTIFY_CLIENT_SECRET = "9295510062b74b17832a4f2fd833308c"
_REDIRECT_URI = "http://localhost:3000/callback"


musikk = Spotify(auth_manager=SpotifyOAuth(scope="user-read-playback-state "
                                                 "user-modify-playback-state",
                                           client_id=_SPOTIFY_CLIENT_ID,
                                           client_secret=_SPOTIFY_CLIENT_SECRET,
                                           redirect_uri=_REDIRECT_URI))
musikk.volume(_VOLUME)

Drikkelek(wait_time=_WAIT_TIME, playlist=_PLAYLIST, directory=_SOUND_DIR, musikk=musikk)
