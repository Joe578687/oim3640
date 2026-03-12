"""
Space Invaders Game
Main entry point
"""

from game import Game


if __name__ == "__main__":
    game = Game()
    game.run()

    # Store game results
    results = {
        "score": game.score,
        "level": game.level,
        "enemies_defeated": game.enemies_defeated
    }
    
    # Store in a results list for tracking multiple games
    game_history = [results]