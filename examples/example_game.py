from src.party.game import Game


"""
_WAIT_TIME : minutes between each game.
    Either an integer or a tuple.
    If a tuple, the game will start at a random time between the two values.
_VOLUME : volume of the music.
    Percentage, 0-100.
    
_SOUND_DIR : folder to place and play the sound files.
_PLAYLIST : Spotify-URI for the playlist.

_SPOTIFY_CLIENT_ID : Spotify Client ID.
_SPOTIFY_CLIENT_SECRET : Spotify Client Secret.
_REDIRECT_URI : Spotify-URI for the redirect-page.
"""


_WAIT_TIME = (2, 5)
_VOLUME = 70

_SOUND_DIR = "../src/party/sounds/"
_PLAYLIST = "spotify:playlist:6TutgaHFfkThmrrobwA2y9"

_SPOTIFY_CLIENT_ID = "YOUR CLIENT ID"
_SPOTIFY_CLIENT_SECRET = "YOUR CLIENT SECRET"
_REDIRECT_URI = "http://localhost:3000/callback"

Game(wait_time=_WAIT_TIME,
     playlist=_PLAYLIST,
     directory=_SOUND_DIR,
     music=(_SPOTIFY_CLIENT_ID, _SPOTIFY_CLIENT_SECRET, _REDIRECT_URI),
     volume=_VOLUME)
