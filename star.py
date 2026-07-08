import pygame
from pygame.sprite import Sprite
import random


class Star(Sprite):
    """Класс для создания звёзд на фоне."""

    def __init__(self, ai_game):
        """Инициализирует звезду и задает её позицию."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Случайный размер звезды (1-3 пикселя)
        size = random.randint(1, 3)
        self.image = pygame.Surface((size, size))

        # Случайная яркость звезды
        brightness = random.randint(100, 255)
        self.image.fill((brightness, brightness, brightness))
        self.rect = self.image.get_rect()

        # Случайная позиция на экране
        self.rect.x = random.randint(0, self.settings.screen_width)
        self.rect.y = random.randint(0, self.settings.screen_height)

        # Для анимации мерцания
        self.twinkle_speed = random.uniform(0.01, 0.03)
        self.brightness = brightness
        self.direction = 1

    def update(self):
        """Обновляет звезду (мерцание)."""
        # Мерцание звезды
        self.brightness += self.twinkle_speed * self.direction
        if self.brightness > 255:
            self.brightness = 255
            self.direction = -1
        elif self.brightness < 50:
            self.brightness = 50
            self.direction = 1

        # Обновляем цвет звезды
        color = int(self.brightness)
        self.image.fill((color, color, color))