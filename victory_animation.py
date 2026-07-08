import pygame
import random


class VictoryAnimation:
    """Класс для анимации победы."""

    def __init__(self, ai_game):
        """Инициализирует анимацию победы."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings

        # Состояние анимации
        self.active = False
        self.finished = False
        self.timer = 0
        self.duration = 1200  # 20 секунд

        # Облака
        self.clouds = []

        # Текст
        self.font = pygame.font.SysFont('Arial', 120, bold=True)
        self.small_font = pygame.font.SysFont('Arial', 50)

    def start(self):
        """Запускает анимацию победы."""
        self.active = True
        self.finished = False
        self.timer = 0

        # Создаём облака (фиксированные позиции)
        self.clouds = [
            (100, 80, 150),
            (350, 50, 200),
            (600, 90, 170),
            (850, 60, 180),
            (150, 200, 130),
            (500, 170, 160),
            (750, 180, 140),
            (1000, 150, 150),
        ]

    def update(self):
        """Обновляет анимацию победы."""
        if not self.active:
            return

        self.timer += 1

        # Проверка завершения
        if self.timer >= self.duration:
            self.active = False
            self.finished = True

    def draw(self):
        """Рисует анимацию победы."""
        if not self.active:
            return

        # Голубой фон (небо)
        self.screen.fill((135, 206, 235))

        # Рисуем солнце
        sun_x = self.screen_rect.width - 150
        sun_y = 150
        sun_radius = 80

        # Свечение солнца
        for i in range(3):
            glow_radius = sun_radius + i * 25
            alpha = 50 - i * 15
            glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (255, 255, 200, alpha), (glow_radius, glow_radius), glow_radius)
            self.screen.blit(glow_surf, (sun_x - glow_radius, sun_y - glow_radius))

        # Солнце
        pygame.draw.circle(self.screen, (255, 255, 100), (sun_x, sun_y), sun_radius)
        pygame.draw.circle(self.screen, (255, 255, 200), (sun_x, sun_y), sun_radius - 10)

        # Лучи солнца (неподвижные)
        for i in range(12):
            angle = i * 30
            length = sun_radius + 35
            x1 = sun_x + sun_radius * pygame.math.Vector2(1, 0).rotate(angle)[0]
            y1 = sun_y + sun_radius * pygame.math.Vector2(1, 0).rotate(angle)[1]
            x2 = sun_x + length * pygame.math.Vector2(1, 0).rotate(angle)[0]
            y2 = sun_y + length * pygame.math.Vector2(1, 0).rotate(angle)[1]
            pygame.draw.line(self.screen, (255, 255, 200, 100), (x1, y1), (x2, y2), 4)

        # Рисуем облака
        for x, y, size in self.clouds:
            self._draw_cloud(x, y, size)

        # Надпись "ПОБЕДА!"
        pulse = abs(pygame.math.Vector2(1, 0).rotate(self.timer * 2)[1])
        alpha = int(200 + 55 * pulse)

        text = "ПОБЕДА!"
        text_surf = self.font.render(text, True, (255, 215, 0))
        text_surf.set_alpha(alpha)

        shadow_surf = self.font.render(text, True, (100, 50, 0))
        shadow_surf.set_alpha(alpha)

        text_rect = text_surf.get_rect()
        text_rect.centerx = self.screen_rect.centerx
        text_rect.centery = self.screen_rect.centery - 50

        shadow_rect = shadow_surf.get_rect()
        shadow_rect.centerx = self.screen_rect.centerx + 4
        shadow_rect.centery = self.screen_rect.centery - 46

        self.screen.blit(shadow_surf, shadow_rect)
        self.screen.blit(text_surf, text_rect)

        # Подпись
        sub_text = "ЗЕМЛЯ СПАСЕНА!"
        sub_surf = self.small_font.render(sub_text, True, (255, 255, 255))
        sub_surf.set_alpha(alpha)
        sub_rect = sub_surf.get_rect()
        sub_rect.centerx = self.screen_rect.centerx
        sub_rect.top = text_rect.bottom + 20
        self.screen.blit(sub_surf, sub_rect)

        # Счётчик уровня
        level_text = f"Уровень {self.settings.max_level} пройден!"
        level_surf = self.small_font.render(level_text, True, (255, 255, 200))
        level_surf.set_alpha(alpha)
        level_rect = level_surf.get_rect()
        level_rect.centerx = self.screen_rect.centerx
        level_rect.top = sub_rect.bottom + 10
        self.screen.blit(level_surf, level_rect)

    def _draw_cloud(self, x, y, size):
        """Рисует облако."""
        cloud_surf = pygame.Surface((size * 2, size), pygame.SRCALPHA)

        # Круги облака
        circles = [
            (size * 0.3, size * 0.5, size * 0.4),
            (size * 0.6, size * 0.3, size * 0.5),
            (size * 0.9, size * 0.4, size * 0.45),
            (size * 0.5, size * 0.6, size * 0.35),
            (size * 0.7, size * 0.55, size * 0.38),
        ]

        for cx, cy, r in circles:
            pygame.draw.circle(cloud_surf, (255, 255, 255, 220), (int(cx), int(cy)), int(r))
            pygame.draw.circle(cloud_surf, (240, 240, 250, 150), (int(cx - r * 0.1), int(cy - r * 0.1)), int(r * 0.6))

        self.screen.blit(cloud_surf, (int(x), int(y)))

    def is_finished(self):
        """Проверяет, завершена ли анимация."""
        return self.finished