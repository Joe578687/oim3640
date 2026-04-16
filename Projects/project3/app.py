"""
app.py
Flask web application for the MBTA Nearest Stop Finder.
"""

import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

from mbta_helper import find_stops_near

load_dotenv()
app = Flask(__name__)

MAPBOX_TOKEN = os.environ.get("MAPBOX_TOKEN", "YOUR_MAPBOX_TOKEN_HERE")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", mapbox_token=MAPBOX_TOKEN)


@app.route("/nearest", methods=["POST"])
def nearest():
    place_name = request.form.get("place_name", "").strip()

    if not place_name:
        return render_template(
            "index.html",
            mapbox_token=MAPBOX_TOKEN,
            error="Please enter a place name.",
        )

    try:
        lat, lng, nearest_stations = find_stops_near(place_name)
    except ValueError as exc:
        return render_template(
            "index.html",
            mapbox_token=MAPBOX_TOKEN,
            error=str(exc),
        )
    except RuntimeError as exc:
        return render_template(
            "index.html",
            mapbox_token=MAPBOX_TOKEN,
            error=f"Service error: {exc}",
        )

    return render_template(
        "result.html",
        place_name=place_name,
        nearest_stations=nearest_stations,
        lat=lat,
        lng=lng,
        mapbox_token=MAPBOX_TOKEN,
    )


if __name__ == "__main__":
    app.run(debug=True)