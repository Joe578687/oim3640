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
    player1 = request.args.get("player1", "")
    player2 = request.args.get("player2", "")

    data = None

    if player1 and player2:
        def calculate_record(player_id):
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
            return wins, losses, win_rate

        p1_wins, p1_losses, p1_rate = calculate_record(player1)
        p2_wins, p2_losses, p2_rate = calculate_record(player2)

        data = {
            "player1": {"id": player1, "wins": p1_wins, "losses": p1_losses, "win_rate": p1_rate},
            "player2": {"id": player2, "wins": p2_wins, "losses": p2_losses, "win_rate": p2_rate}
        }

    return render_template("compare.html", data=data)


@app.route("/tournaments")
def tournaments():
    year = request.args.get("year", "")
    tournaments = get_tournaments(year=year)
    return render_template("tournaments.html", year=year, tournaments=tournaments)


if __name__ == "__main__":
    app.run(debug=True)