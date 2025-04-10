import config
import spotify
from twitchio.ext import commands

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=config.TWITCH_OAUTH, 
            prefix="!", 
            initial_channels=[config.TWITCH_CHANNEL]
        )

    async def event_ready(self):
        print(f"Bot ist online als {self.nick}")

    @commands.command(name="song")
    async def song(self, ctx):
        current_song = spotify.get_current_song()
        await ctx.send(f"Aktuell läuft: {current_song}")

    @commands.command(name="sr", aliases=["wunsch", "songrequest"])
    async def sr(self, ctx, *, song_name):
        # Füge den Song zur Warteschlange hinzu
        response = spotify.add_song_to_queue(song_name)
        
        # Hole die Songdaten von Spotify nach der Warteschlange
        song_info = spotify.get_current_song()
        
        # Sende eine Antwort, die den hinzugefügten Song zeigt
        await ctx.send(f"Song '{song_name}' wurde zur Warteschlange hinzugefügt! Jetzt spielt: {song_info}")

if __name__ == "__main__":
    bot = Bot()
    bot.run()
