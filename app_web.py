from flask import Flask, render_template
import asyncio
from app.db import get_animes

app = Flask(__name__, template_folder="templates")

@app.route("/")
def anime_list():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    animes = loop.run_until_complete(get_animes())
    return render_template("animes.html", animes=animes)
