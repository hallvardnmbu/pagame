from src.party.game import Game


"""
DELAY : minutes between each game.
    Either an integer or a tuple.
    If a tuple, the game will start at a random time between the two values.
    
VOLUME : volume of the music.
    Percentage, 0-100.
    
SOUND_DIR : folder to place and play the sound files.
PLAYLIST : Spotify-URI for the playlist.

SPOTIFY_ID : Spotify Client ID.
SPOTIFY_SECRET : Spotify Client Secret.
REDIRECT_URI : Spotify-URI for the redirect-page.
"""


DELAY = 0.2 #(2, 5)
VOLUME = 70

SOUND_DIR = "../src/party/sounds/"
PLAYLIST = "spotify:playlist:6TutgaHFfkThmrrobwA2y9"

SPOTIFY_ID = open("../secrets/spotify_id").read()
SPOTIFY_SECRET = open("../secrets/spotify_secret").read()
REDIRECT_URI = "http://localhost:3000/callback"

Game(
    delay=DELAY,
    music={
     "playlist": PLAYLIST,
     "directory": SOUND_DIR,
     "spotify": {
         "client_id": SPOTIFY_ID,
         "client_secret": SPOTIFY_SECRET,
         "redirect_uri": REDIRECT_URI
     },
     "volume": VOLUME
    }
)
