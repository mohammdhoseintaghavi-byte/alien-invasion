import json
from paths import HIGH_SCORE_FILE
class GameStats:
    def __init__(self,ai_game):
        self.settings=ai_game.settings
        self.reset_stats()
        try:
            with open(HIGH_SCORE_FILE) as f:
                self.high_score = json.load(f)
        except FileNotFoundError:
            self.high_score = 0

    def reset_stats(self):
        self.ship_left=self.settings.ship_limit
        self.score=0
        self.level=1