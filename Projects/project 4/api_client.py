import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("SPORTS_API_BASE_URL")
API_KEY = os.getenv("SPORTS_API_KEY")


PLAYER_DATABASE = [
    {"id": "sr:competitor:14882", "name": "Djokovic, Novak", "status": "Active/Recent", "country": "Serbia"},
    {"id": "sr:competitor:14486", "name": "Nadal, Rafael", "status": "Retired/Recent", "country": "Spain"},
    {"id": "sr:competitor:122366", "name": "Federer, Roger", "status": "Retired", "country": "Switzerland"},
    {"id": "sr:competitor:407573", "name": "Alcaraz, Carlos", "status": "Active", "country": "Spain"},
    {"id": "sr:competitor:225050", "name": "Sinner, Jannik", "status": "Active", "country": "Italy"},
    {"id": "sr:competitor:359610", "name": "Medvedev, Daniil", "status": "Active", "country": "Russia"},
    {"id": "sr:competitor:57163", "name": "Zverev, Alexander", "status": "Active", "country": "Germany"},
    {"id": "sr:competitor:163504", "name": "Tsitsipas, Stefanos", "status": "Active", "country": "Greece"},
    {"id": "sr:competitor:14484", "name": "Murray, Andy", "status": "Retired/Recent", "country": "Great Britain"},
    {"id": "sr:competitor:19300", "name": "Wawrinka, Stan", "status": "Active/Recent", "country": "Switzerland"},
    {"id": "sr:competitor:44310", "name": "Thiem, Dominic", "status": "Retired/Recent", "country": "Austria"},
    {"id": "sr:competitor:1726", "name": "Roddick, Andy", "status": "Retired", "country": "USA"},
    {"id": "sr:competitor:14889", "name": "Hewitt, Lleyton", "status": "Retired", "country": "Australia"},
    {"id": "sr:competitor:143620", "name": "Kyrgios, Nick", "status": "Active/Recent", "country": "Australia"},
    {"id": "sr:competitor:27213", "name": "Del Potro, Juan Martin", "status": "Retired", "country": "Argentina"},
    {"id": "sr:competitor:30969", "name": "Cilic, Marin", "status": "Active/Recent", "country": "Croatia"},
    {"id": "sr:competitor:70968", "name": "Raonic, Milos", "status": "Active/Recent", "country": "Canada"},
    {"id": "sr:competitor:210326", "name": "Rublev, Andrey", "status": "Active", "country": "Russia"},
    {"id": "sr:competitor:106755", "name": "Fritz, Taylor", "status": "Active", "country": "USA"},
    {"id": "sr:competitor:407573", "name": "Alcaraz, Carlos", "status": "Active", "country": "Spain"},
]


def make_request(endpoint):
    url = f"{BASE_URL.rstrip('/')}/{endpoint.lstrip('/')}"
    params = {"api_key": API_KEY}

    try:
        response = requests.get(url, params=params, timeout=15)
        print("REQUEST:", response.url)
        print("STATUS:", response.status_code)
        response.raise_for_status()
        return response.json()

    except Exception as error:
        print("API request failed:", error)
        return {}


def search_players(query):
    players = []

    for player in PLAYER_DATABASE:
        if query.lower() in player["name"].lower():
            players.append(player)

    # Also search current rankings from API
    data = make_request("/en/rankings.json")
    rankings = data.get("rankings", [])

    for ranking_group in rankings:
        competitor_rankings = ranking_group.get("competitor_rankings", [])

        for item in competitor_rankings:
            competitor = item.get("competitor", {})
            name = competitor.get("name", "")

            if query.lower() in name.lower():
                player = {
                    "id": competitor.get("id"),
                    "name": name,
                    "rank": item.get("rank"),
                    "points": item.get("points"),
                    "status": "Active/Ranked",
                    "country": competitor.get("country", "")
                }

                if player not in players:
                    players.append(player)

    return players


def get_player_matches(player_id):
    data = make_request(f"/en/competitors/{player_id}/summaries.json")
    return data.get("summaries", [])


def get_tournaments(year=""):
    data = make_request("/en/competitions.json")
    return data.get("competitions", [])