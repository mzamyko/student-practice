import pygame.font
from pygame.sprite import Group
import pygame

from ship import Ship


class Scoreboard:
    """Класс для вывода игровой информации."""

    def __init__(self, ai_game):
        """Инициализирует атрибуты подсчета очков."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Настройки шрифта для вывода счета.
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont('Arial', 48)
        self.small_font = pygame.font.SysFont('Arial', 28)

        # Подготовка исходного изображения.
        self.prep_score()
        self.prep_level_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Преобразует общий счёт в графическое изображение."""
        rounded_score = round(self.stats.total_score, -1)
        score_str = f"{rounded_score:,}"
        self.score_image = self.font.render(score_str, True,
                                            self.text_color, self.settings.bg_color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_level_score(self):
        """Преобразует счёт за уровень в графическое изображение."""
        level_score_str = f"* {self.stats.level_score}"
        self.level_score_image = self.small_font.render(level_score_str, True,
                                                        (255, 215, 0), self.settings.bg_color)
        self.level_score_rect = self.level_score_image.get_rect()
        self.level_score_rect.right = self.screen_rect.right - 20
        self.level_score_rect.top = self.score_rect.bottom + 5

    def prep_high_score(self):
        """Преобразует рекордный счет в графическое изображение."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"* {high_score:,}"
        self.high_score_image = self.font.render(high_score_str, True,
                                                 (255, 215, 0), self.settings.bg_color)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Преобразует уровень в графическое изображение."""
        level_str = "LVL " + str(self.stats.level)
        self.level_image = self.small_font.render(level_str, True,
                                                  self.text_color, self.settings.bg_color)

        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right - 20
        self.level_rect.top = self.level_score_rect.bottom + 5

    def draw_heart(self, surface, x, y, size, color):
        """Рисует сердечко на поверхности."""
        pygame.draw.circle(surface, color, (int(x - size * 0.3), int(y - size * 0.2)), int(size * 0.35))
        pygame.draw.circle(surface, color, (int(x + size * 0.3), int(y - size * 0.2)), int(size * 0.35))
        heart_points = [
            (int(x - size * 0.45), int(y - size * 0.1)),
            (int(x + size * 0.45), int(y - size * 0.1)),
            (int(x), int(y + size * 0.5))
        ]
        pygame.draw.polygon(surface, color, heart_points)

        pygame.draw.circle(surface, (255, 50, 50), (int(x - size * 0.3), int(y - size * 0.2)), int(size * 0.35), 1)
        pygame.draw.circle(surface, (255, 50, 50), (int(x + size * 0.3), int(y - size * 0.2)), int(size * 0.35), 1)
        pygame.draw.polygon(surface, (255, 50, 50), heart_points, 1)
        pygame.draw.circle(surface, (255, 200, 200), (int(x - size * 0.15), int(y - size * 0.3)), int(size * 0.08))

    def prep_ships(self):
        """Показывает количество оставшихся жизней в виде сердечек."""
        self.ships = Group()
        heart_size = 25

        self.ships.empty()

        for ship_number in range(self.stats.ships_left):
            heart_surface = pygame.Surface((heart_size + 10, heart_size + 10), pygame.SRCALPHA)
            heart_surface.fill((0, 0, 0, 0))

            self.draw_heart(heart_surface, heart_size // 2 + 5, heart_size // 2 + 5, heart_size, (255, 50, 50))

            heart_sprite = pygame.sprite.Sprite()
            heart_sprite.image = heart_surface
            heart_sprite.rect = heart_surface.get_rect()
            heart_sprite.rect.x = 10 + ship_number * (heart_size + 15)
            heart_sprite.rect.y = 10

            self.ships.add(heart_sprite)

    def check_high_score(self):
        """Проверяет, появился ли новый рекорд."""
        if self.stats.total_score > self.stats.high_score:
            self.stats.high_score = self.stats.total_score
            self.prep_high_score()

    def show_score(self):
        """Выводит счет, звёзды за уровень, рекорд, уровень и сердца на экран."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_score_image, self.level_score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)