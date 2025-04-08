# eventsub_listener.py
from flask import Flask, request, jsonify
import spotify  # dein bestehendes Spotify-Modul
import asyncio

app = Flask(__name__)
bot_instance = None  # wird vom Hauptscript gesetzt

@app.route("/eventsub", methods=["POST"])
def eventsub():
    data = request.json

    # Twitch-Webhook-Handshake
    if 'challenge' in data:
        return data['challenge']

    event_type = data.get("subscription", {}).get("type")
    if event_type == "channel.channel_points_custom_reward_redemption.add":
        event = data.get("event", {})
        song_request = event.get("user_input", "").strip()

        print(f"Songwunsch über Kanalpunkte: {song_request}")
        if song_request:
            response = spotify.add_song_to_queue(song_request)
            print(response)
            if bot_instance:
                asyncio.run_coroutine_threadsafe(
                    bot_instance.get_channel("DEIN_CHANNELNAME").send(response),
                    bot_instance.loop
                )
    return jsonify({"status": "ok"})
