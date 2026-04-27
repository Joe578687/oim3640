from flask import Flask, render_template, request
from api_client import search_players, get_player_matches, get_tournaments
from charts import make_win_rate_chart, make_opponent_chart

app = Flask(__name__)


@app.route("/")
def index():
    query = request.args.get("q", "")
    players = search_players(query) if query else []
    return render_template("index.html", query=query, players=players)


@app.route("/player/<path:player_id>")
def player_detail(player_id):
    matches = get_player_matches(player_id)

    wins = 0
    losses = 0
    opponents = {}

    for match in matches:
        competitors = match.get("sport_event", {}).get("competitors", [])
        winner_id = match.get("sport_event_status", {}).get("winner_id", "")

        opponent_name = "Unknown Opponent"

        for competitor in competitors:
            if competitor.get("id") != player_id:
                opponent_name = competitor.get("name", "Unknown Opponent")

        if winner_id == player_id:
            wins += 1
        elif winner_id:
            losses += 1

        opponents[opponent_name] = opponents.get(opponent_name, 0) + 1

    total = wins + losses
    win_rate = round((wins / total) * 100, 2) if total > 0 else 0

    return render_template(
        "player.html",
        player_id=player_id,
        matches=matches,
        wins=wins,
        losses=losses,
        win_rate=win_rate,
        win_chart=make_win_rate_chart(wins, losses),
        opponent_chart=make_opponent_chart(opponents)
    )


@app.route("/compare")
def compare():
    player1_name = request.args.get("player1", "")
    player2_name = request.args.get("player2", "")

    data = None
    error = None

    if player1_name and player2_name:
        player1_results = search_players(player1_name)
        player2_results = search_players(player2_name)

        if not player1_results or not player2_results:
            error = "One or both players could not be found. Try using last names like Djokovic, Alcaraz, Sinner, or Zverev."
        else:
            player1 = player1_results[0]
            player2 = player2_results[0]

            def calculate_record(player):
                player_id = player["id"]
                matches = get_player_matches(player_id)

                wins = 0
                losses = 0

                for match in matches:
                    winner_id = match.get("sport_event_status", {}).get("winner_id", "")

                    if winner_id == player_id:
                        wins += 1
                    elif winner_id:
                        losses += 1

                total = wins + losses
                win_rate = round((wins / total) * 100, 2) if total > 0 else 0

                return {
                    "name": player.get("name", "Unknown"),
                    "id": player_id,
                    "wins": wins,
                    "losses": losses,
                    "win_rate": win_rate
                }

            data = {
                "player1": calculate_record(player1),
                "player2": calculate_record(player2)
            }

    return render_template(
        "compare.html",
        data=data,
        error=error,
        player1_name=player1_name,
        player2_name=player2_name
    )


@app.route("/tournaments")
def tournaments():
    year = request.args.get("year", "")
    tournaments = get_tournaments(year=year)

    grouped_tournaments = {}

    for t in tournaments:
        group_name = (
            t.get("country")
            or t.get("category", {}).get("name")
            or t.get("gender")
            or "Other / Unknown"
        )

        if group_name not in grouped_tournaments:
            grouped_tournaments[group_name] = []

        grouped_tournaments[group_name].append(t)

    return render_template(
        "tournaments.html",
        year=year,
        grouped_tournaments=grouped_tournaments
    )


if __name__ == "__main__":
    app.run(debug=True)