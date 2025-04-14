from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot läuft!"

@app.route("/healthz")
def healthz():
    return "ok"
