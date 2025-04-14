import threading
from flask import Flask
import config
import spotify
from twitchio.ext import commands

# Flask Webserver
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot läuft!"

@app.route("/healthz")
def healthz():
    return "ok"

# Twitch Bot
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
        response = spotify.add_song_to_queue(song_name)
        song_info = spotify.get_current_song()
        await ctx.send(f"Song wurde zur Warteschlange hinzugefügt! Jetzt spielt: {song_info}")

# Start beides
if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=10000)).start()
    bot = Bot()
    bot.run()
