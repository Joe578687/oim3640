"""
mbta_helper.py
Helper functions for MBTA Finder app.
Pipeline: place name → Mapbox → lat/lng → MBTA → 3 nearest stops
"""

import os
import requests

# ── API keys ───────────────────────────────────────────
MAPBOX_TOKEN = os.environ.get("MAPBOX_TOKEN", "YOUR_MAPBOX_TOKEN_HERE")
MBTA_API_KEY = os.environ.get("MBTA_API_KEY", "YOUR_MBTA_API_KEY_HERE")


# ── Mapbox: get coordinates ────────────────────────────
def get_lat_lng(place_name: str) -> tuple[float, float]:
    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{requests.utils.quote(place_name)}.json"

    params = {
        "access_token": MAPBOX_TOKEN,
        "limit": 1,
        "proximity": "-71.0589,42.3601",   # Boston center
        "bbox": "-71.9,42.0,-70.5,42.9",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Mapbox API error: {e}")

    data = response.json()
    features = data.get("features", [])

    if not features:
        raise ValueError(f"Could not find '{place_name}'.")

    lng, lat = features[0]["geometry"]["coordinates"]
    return lat, lng


# ── MBTA: get 3 nearest stations ───────────────────────
def get_nearest_stations(lat: float, lng: float, limit: int = 3) -> list[dict]:
    url = "https://api-v3.mbta.com/stops"

    params = {
        "api_key": MBTA_API_KEY,
        "filter[latitude]": lat,
        "filter[longitude]": lng,
        "filter[radius]": 0.5,
        "filter[route_type]": "0,1,2",
        "sort": "distance",
        "page[limit]": limit,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"MBTA API error: {e}")

    data = response.json()
    stops = data.get("data", [])

    if not stops:
        raise ValueError("No MBTA stops found nearby.")

    result = []

    for stop in stops:
        attrs = stop["attributes"]

        result.append({
            "name": attrs.get("name") or "Unknown Stop",
            "accessible": attrs.get("wheelchair_boarding", 0) == 1,
            "lat": attrs.get("latitude"),
            "lng": attrs.get("longitude"),
        })

    return result


# ── Combined function ──────────────────────────────────
def find_stops_near(place_name: str) -> tuple[float, float, list[dict]]:
    lat, lng = get_lat_lng(place_name)
    stations = get_nearest_stations(lat, lng, limit=3)
    return lat, lng, stations


# ── Test from terminal ─────────────────────────────────
if __name__ == "__main__":
    test = "Boston Common"
    try:
        lat, lng, stations = find_stops_near(test)
        print(f"\n{test} ({lat:.4f}, {lng:.4f})")

        for i, s in enumerate(stations, 1):
            access = "Yes" if s["accessible"] else "No"
            print(f"{i}. {s['name']} | Wheelchair: {access}")

    except Exception as e:
        print("Error:", e)