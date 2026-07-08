import pygame
from pygame.sprite import Sprite
import math


class Bullet(Sprite):

    def __init__(self, ai_game, angle_offset=0):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        self.image = pygame.Surface((self.settings.bullet_width, self.settings.bullet_height), pygame.SRCALPHA)
        pygame.draw.rect(self.image, self.color, (0, 0, self.settings.bullet_width, self.settings.bullet_height))
        pygame.draw.rect(self.image, (self.color[0]+50, self.color[1]+50, self.color[2]+50, 100),
                        (1, 1, self.settings.bullet_width-2, self.settings.bullet_height-2))

        self.rect = self.image.get_rect()
        self.rect.midtop = ai_game.ship.rect.midtop

        self.angle_offset = angle_offset
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.speed_x = 0
        self.speed_y = -self.settings.bullet_speed

        if angle_offset != 0:
            angle_rad = math.radians(angle_offset)
            self.speed_x = self.settings.bullet_speed * math.sin(angle_rad)
            self.speed_y = -self.settings.bullet_speed * math.cos(angle_rad)

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def draw_bullet(self):
        self.screen.blit(self.image, self.rect)