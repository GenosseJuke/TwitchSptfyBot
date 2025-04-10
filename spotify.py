# spotify.py

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import config

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=config.SPOTIFY_CLIENT_ID,
    client_secret=config.SPOTIFY_CLIENT_SECRET,
    redirect_uri=config.SPOTIFY_REDIRECT_URI,
    scope="user-read-currently-playing user-modify-playback-state",
    cache_path=".spotify_token_cache"
))

# Funktion, die den aktuellen Songtitel abruft
def get_current_song():
    track = sp.current_user_playing_track()
    if track and track["is_playing"]:
        title = track["item"]["name"]
        artist = track["item"]["artists"][0]["name"]
        return f"Aktuell läuft: {title} von {artist}"
    return "Gerade läuft kein Song auf Spotify."

# Funktion, um einen Song zur Warteschlange hinzuzufügen
def add_song_to_queue(song_name):
    results = sp.search(q=song_name, limit=1)
    if results["tracks"]["items"]:
        song_uri = results["tracks"]["items"][0]["uri"]
        sp.add_to_queue(song_uri)
        return f"Song '{song_name}' wurde zur Warteschlange hinzugefügt!"
    return "Kein passender Song gefunden."
