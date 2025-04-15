import spotipy
from spotipy.oauth2 import SpotifyOAuth
import config
import re

auth_manager = SpotifyOAuth(
    client_id=config.SPOTIFY_CLIENT_ID,
    client_secret=config.SPOTIFY_CLIENT_SECRET,
    redirect_uri=config.SPOTIFY_REDIRECT_URI,
    scope="user-read-currently-playing user-modify-playback-state",
    cache_path=".spotify_token_cache",
    open_browser=False  # wichtig für Headless-Umgebungen
)

# Token beim Start laden (damit keine Interaktion nötig ist)
auth_manager.get_access_token(as_dict=False)

sp = spotipy.Spotify(auth_manager=auth_manager)

def get_current_song():
    try:
        # Hole den aktuellen Song, aber keine Abfrage, ob er gerade läuft
        track = sp.current_user_playing_track()
        if track and track["is_playing"]:
            title = track["item"]["name"]
            artist = track["item"]["artists"][0]["name"]
            return f"Aktuell läuft: {title} von {artist}"
        return "Gerade läuft kein Song auf Spotify."
    except Exception as e:
        return f"Fehler beim Abrufen des Songs: {e}"

def get_song_uri(song_name_or_url):
    # Überprüfe, ob der Songname ein Spotify-URI ist (Link)
    spotify_url_pattern = r"(https://open.spotify.com/track/[\w]+)"
    match = re.match(spotify_url_pattern, song_name_or_url)

    if match:
        # Wenn es ein Link ist, extrahiere die URI
        return song_name_or_url
    else:
        # Wenn es kein Link ist, suche nach dem Song
        results = sp.search(q=song_name_or_url, limit=1)
        if results["tracks"]["items"]:
            return results["tracks"]["items"][0]["uri"]
    return None

def add_song_to_queue(song_name_or_url):
    try:
        song_uri = get_song_uri(song_name_or_url)
        if song_uri:
            sp.add_to_queue(song_uri)
            return f"Song '{song_name_or_url}' wurde zur Warteschlange hinzugefügt!"
        return "Kein passender Song gefunden."
    except Exception as e:
        return f"Fehler beim Hinzufügen zur Warteschlange: {e}"
