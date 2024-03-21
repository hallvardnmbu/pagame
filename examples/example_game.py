from pagame.game import Play


DELAY = (2, 5)
LANGUAGE = "en"

PLAYLIST = "6TutgaHFfkThmrrobwA2y9"

SPOTIFY_ID = None                                                 # INSERT YOUR SPOTIFY ID HERE
SPOTIFY_SECRET = None                                             # INSERT YOUR SPOTIFY SECRET HERE

SPOTIFY = {
    "client_id": SPOTIFY_ID,
    "client_secret": SPOTIFY_SECRET,
    "redirect_uri": "http://localhost:3000/callback"
}

Play(
    delay=DELAY,
    language=LANGUAGE,
    music={
     "playlist": "spotify:playlist:" + PLAYLIST,
     "spotify": SPOTIFY
    }
)
