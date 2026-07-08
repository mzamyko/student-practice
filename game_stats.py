class GameStats:
    """Отслеживание статистики для игры Alien Invasion."""

    def __init__(self, ai_game):
        """Инициализирует статистику."""
        self.settings = ai_game.settings
        self.reset_stats()

        # Игра запускается в неактивном состоянии.
        self.game_active = False

        # Рекорд не должен сбрасываться.
        self.high_score = 0

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры."""
        self.ships_left = self.settings.ship_limit
        self.total_score = 0      # ОБЩИЙ счёт (сохраняется после прохождения уровня)
        self.level_score = 0      # Счёт за текущий уровень (сбрасывается при потере жизни)
        self.level = 1
        self.bullets_fired = 0

    def reset_level_stats(self):
        """Сбрасывает очки уровня (только при потере жизни)."""
        self.level_score = 0

    def add_score(self, points):
        """Добавляет очки к счёту уровня."""
        self.level_score += points

    def complete_level(self):
        """Завершает уровень - добавляет очки уровня к общему счёту."""
        self.total_score += self.level_score
        self.level_score = 0

    def add_bullet(self):
        """Увеличивает счётчик пуль."""
        self.bullets_fired += 1

    def get_final_score(self):
        """Возвращает общий счёт для рекордов."""
        return self.total_score