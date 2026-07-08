import pygame
from pygame.sprite import Sprite


class AlienBullet(Sprite):

    def __init__(self, ai_game, x, y):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = pygame.Surface((6, 12), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (255, 200, 50), (0, 0, 6, 12))
        pygame.draw.ellipse(self.image, (255, 255, 100), (1, 1, 4, 6))
        pygame.draw.ellipse(self.image, (255, 200, 50, 80), (-2, 0, 10, 12), 2)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y

        self.speed = 2.0

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > self.screen.get_rect().bottom:
            self.kill()

    def draw_bullet(self):
        self.screen.blit(self.image, self.rect)