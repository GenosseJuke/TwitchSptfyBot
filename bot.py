# bot.py

import config
import spotify
from twitchio.ext import commands
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=3000)


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
        # Aufruf der Funktion aus dem spotify-Modul
        current_song = spotify.get_current_song()
        await ctx.send(current_song)

    @commands.command(name="wunsch")
    async def wunsch(self, ctx, *, song_name):
        response = spotify.add_song_to_queue(song_name)
        await ctx.send(response)


# Hauptprogramm starten
if __name__ == "__main__":
    # Flask im Hintergrund starten
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Bot starten
    bot = Bot()
    bot.run()
