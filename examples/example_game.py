from src.party.game import Game


"""
Notes
-----
    Spotify 'must' be open.
    
    In order for the game to access Spotify, you need to have a Spotify client id and secret. These 
    can be obtained by creating a Spotify app, and the client id and secret can be pasted below.
    
    When this is in order, run this file from the 'examples' directory.

Parameters 
----------
    DELAY : minutes between each game.
            Either an integer or a tuple.
            If a tuple, the game will start at a random time between the two values.
        
    PLAYLIST : Spotify-URI for the playlist.
    
    SPOTIFY_ID : Spotify client id.
    SPOTIFY_SECRET : Spotify client secret.
"""


DELAY = (2, 5)
PLAYLIST = "spotify:playlist:6TutgaHFfkThmrrobwA2y9"

SPOTIFY_ID = open("../secrets/spotify_id").read()               # INSERT YOUR SPOTIFY ID HERE
SPOTIFY_SECRET = open("../secrets/spotify_secret").read()       # INSERT YOUR SPOTIFY SECRET HERE

SPOTIFY = {
    "client_id": SPOTIFY_ID,
    "client_secret": SPOTIFY_SECRET,
    "redirect_uri": "http://localhost:3000/callback"
}

Game(
    delay=DELAY,
    music={
     "playlist": PLAYLIST,
     "directory": "../src/party/sounds/",
     "spotify": SPOTIFY
    }
)
