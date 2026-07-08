class GameStats:

    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()

        self.game_active = False

        self.high_score = 0

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.total_score = 0
        self.level_score = 0
        self.level = 1
        self.bullets_fired = 0

    def reset_level_stats(self):
        self.level_score = 0

    def add_score(self, points):
        self.level_score += points

    def complete_level(self):
        self.total_score += self.level_score
        self.level_score = 0

    def add_bullet(self):
        self.bullets_fired += 1

    def get_final_score(self):
        return self.total_score