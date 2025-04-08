# spotify.py

import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Authentifizierung
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='dein_client_id',
                                               client_secret='dein_client_secret',
                                               redirect_uri='deine_redirect_uri',
                                               scope='user-library-read user-read-playback-state user-modify-playback-state'))

# Hole den aktuellen Song
def get_current_song():
    current_track = sp.current_playback()
    if current_track is not None:
        song_name = current_track['item']['name']
        artist_name = current_track['item']['artists'][0]['name']
        return f"Der aktuelle Song ist: {song_name} von {artist_name}"
    return "Kein Song wird derzeit abgespielt."

# Füge einen Song zur Warteschlange hinzu
def add_song_to_queue(song_name):
    results = sp.search(q=song_name, limit=1, type='track')
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        sp.add_to_queue(track['uri'])
        return f"{song_name} wurde zur Warteschlange hinzugefügt!"
    return f"Der Song '{song_name}' konnte nicht gefunden werden."

  @commands.command(name="skip")
    async def skip(self, ctx):
        # Funktion zum Überspringen des aktuellen Songs
        response = spotify.skip_current_song()
        await ctx.send(response)

if __name__ == "__main__":
    bot = Bot()
    bot.run()
