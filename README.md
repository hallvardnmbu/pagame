Have fun.
=========

---

Download and run the correct `application` for your system directly, or follow one of the steps 
below.

---

Terminal usage
--------------

```bash
pip install pagame

pagame
```

Python usage
------------

```bash
pip install pagame
```

```python
from pagame import Play

Play()
```

See and run `examples/example_game.py` for manually starting the game with parameters.

---

Notes
-----

Spotify should be open for the proper experience, but does not have to.

In order for the game to access Spotify, you need to have a Spotify client id and secret. These
can be obtained by creating a Spotify app (through `developer.spotify.com`); and the client id
and secret can be pasted directly in through the GUI, or into the example script.

---

Parameters
----------

Note that all these can be controlled through the GUI.

| Parameter | Description | Type |
| --------- | ----------- | ---- |
| `delay` | Minutes between each game.<br>If tuple, randomly sampled between values. | `int` or `tuple[int, int]` |
| `language` | Which language the game is played with. | `str` |
| `playlist` | Spotify-URI for the playlist. | `str` |
| `spotify_id` | Spotify client id. | `str` |
| `spotify_secret` | Spotify client secret. | `str` |
