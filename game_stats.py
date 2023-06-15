class GameStats:
    """Track statistics for Alien Invasion"""

    def __init__(self, ai_game) -> None:
        """Initialize statistics"""
        self.settings = ai_game.settings
        self.reset_stats()

        # High score should never be reset
        try:
            with open("data/hscore.txt", "r") as f:
                self.high_score = int(f.read())
        except ValueError:
            self.high_score = 0
        except Exception as e:
            print(f"Error {e}")

    def reset_stats(self):
        """Initialize statistics that can change durning the game"""
        self.ships_left = self.settings.ship_life_limit
        self.score = 0
        self.level = 1
