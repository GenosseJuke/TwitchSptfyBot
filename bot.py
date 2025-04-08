# bot.py

import config
import spotify
from twitchio.ext import commands
from threading import Thread
import asyncio

# Deine Bot-Klasse
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
        await ctx.send(current_song)

    @commands.command(name="wunsch")
    async def wunsch(self, ctx, *, song_name):
        response = spotify.add_song_to_queue(song_name)
        await ctx.send(response)

# Instanz des Bots erstellen
bot_instance = Bot()

# Stelle sicher, dass die globale Variable für deinen Webhook gesetzt wird
import eventsub_listener
eventsub_listener.bot_instance = bot_instance

# Funktion, um den Flask-Server zu starten
def run_flask():
    from eventsub_listener import app
    app.run(port=5000)

# Starte den Flask-Server in einem separaten Thread
flask_thread = Thread(target=run_flask)
flask_thread.start()

# Starte den Twitch-Bot
bot_instance.run()
