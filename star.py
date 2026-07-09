import pygame
from pygame.sprite import Sprite
import random


class Star(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        size = random.randint(1, 3)
        self.image = pygame.Surface((size, size))

        brightness = random.randint(100, 255)
        self.image.fill((brightness, brightness, brightness))
        self.rect = self.image.get_rect()

        self.rect.x = random.randint(0, self.settings.screen_width)
        self.rect.y = random.randint(0, self.settings.screen_height)

        self.twinkle_speed = random.uniform(0.01, 0.03)
        self.brightness = brightness
        self.direction = 1

    def update(self):
        self.brightness += self.twinkle_speed * self.direction
        if self.brightness > 255:
            self.brightness = 255
            self.direction = -1
        elif self.brightness < 50:
            self.brightness = 50
            self.direction = 1

        color = int(self.brightness)
        self.image.fill((color, color, color))