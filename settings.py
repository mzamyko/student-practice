class Settings:
    """Класс для хранения всех настроек игры."""

    def __init__(self):
        """Инициализирует настройки игры."""
        # Настройки экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (10, 10, 30)

        # Настройки звёзд
        self.star_count = 150

        # Настройки корабля
        self.ship_speed = 1.5
        self.ship_limit = 3

        # Настройки пули
        self.bullet_speed = 3.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5

        # Настройки пришельцев (МЕНЬШЕ ЗВЁЗД)
        self.alien_speed = 0.5
        self.fleet_drop_speed = 5
        self.fleet_direction = 1
        self.alien_points = 15   # было 50
        self.pink_alien_points = 30   # было 100

        # Темп ускорения игры
        self.speedup_scale = 1.05

        # Темп роста стоимости пришельцев
        self.score_scale = 1.5

        # Настройки звука
        self.volume = 0.7

        # Максимальное количество уровней
        self.max_level = 4

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Инициализирует настройки, изменяющиеся в ходе игры."""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 0.5
        self.alien_points = 15
        self.pink_alien_points = 30
        self.fleet_direction = 1

    def increase_speed(self):
        """Увеличивает настройки скорости и стоимости пришельцев."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        self.pink_alien_points = int(self.pink_alien_points * self.score_scale)