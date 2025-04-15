import spotipy
from spotipy.oauth2 import SpotifyOAuth
import config

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
        track = sp.current_user_playing_track()
        if track and track["is_playing"]:
            title = track["item"]["name"]
            artist = track["item"]["artists"][0]["name"]
            return f"Aktuell läuft: {title} von {artist}"
        return "Gerade läuft kein Song auf Spotify."
    except Exception as e:
        return f"Fehler beim Abrufen des Songs: {e}"

def add_song_to_queue(song_name):
    try:
        results = sp.search(q=song_name, limit=1)
        if results["tracks"]["items"]:
            song_uri = results["tracks"]["items"][0]["uri"]
            sp.add_to_queue(song_uri)
            return f"Song '{song_name}' wurde zur Warteschlange hinzugefügt!"
        return "Kein passender Song gefunden."
    except Exception as e:
        return f"Fehler beim Hinzufügen zur Warteschlange: {e}"
