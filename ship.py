import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.Surface((60, 70), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))

        self.color = (0, 255, 0)
        self.skin_index = 0
        self._draw_ship()

        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

        self.moving_right = False
        self.moving_left = False

    def _draw_ship(self):
        self.image.fill((0, 0, 0, 0))

        skin = self.skin_index % 5

        if skin == 0:
            self._draw_classic_ship()
        elif skin == 1:
            self._draw_wing_ship()
        elif skin == 2:
            self._draw_round_ship()
        elif skin == 3:
            self._draw_jet_ship()
        elif skin == 4:
            self._draw_arrow_ship()
        else:
            self._draw_classic_ship()

    def _draw_classic_ship(self):
        c = self.color
        points = [(30, 5), (8, 55), (52, 55)]
        pygame.draw.polygon(self.image, c, points)
        pygame.draw.polygon(self.image, (c[0] // 2, c[1] // 2, c[2] // 2), [(30, 15), (18, 45), (42, 45)])
        pygame.draw.circle(self.image, (100, 255, 255), (30, 28), 6)
        pygame.draw.polygon(self.image, c, [(5, 35), (0, 55), (15, 50)])
        pygame.draw.polygon(self.image, c, [(55, 35), (60, 55), (45, 50)])
        pygame.draw.rect(self.image, (255, 100, 50), (12, 55, 8, 8))
        pygame.draw.rect(self.image, (255, 100, 50), (40, 55, 8, 8))

    def _draw_wing_ship(self):
        c = self.color
        points = [(30, 0), (10, 40), (0, 60), (60, 60), (50, 40)]
        pygame.draw.polygon(self.image, c, points)
        pygame.draw.polygon(self.image, (c[0] // 2, c[1] // 2, c[2] // 2), [(30, 15), (18, 45), (42, 45)])
        pygame.draw.circle(self.image, (255, 255, 200), (30, 25), 8)
        pygame.draw.circle(self.image, (200, 200, 255), (30, 25), 5)
        pygame.draw.circle(self.image, (255, 200, 50), (12, 45), 4)
        pygame.draw.circle(self.image, (255, 200, 50), (48, 45), 4)

    def _draw_round_ship(self):
        c = self.color
        pygame.draw.ellipse(self.image, c, (5, 10, 50, 40))
        pygame.draw.ellipse(self.image, (c[0] // 2, c[1] // 2, c[2] // 2), (15, 15, 30, 25))
        pygame.draw.circle(self.image, (255, 255, 200), (30, 22), 10)
        pygame.draw.circle(self.image, (200, 200, 255), (30, 22), 6)
        for i in range(6):
            angle = i * 60
            x = 30 + 20 * pygame.math.Vector2(1, 0).rotate(angle)[0]
            y = 30 + 20 * pygame.math.Vector2(1, 0).rotate(angle)[1]
            pygame.draw.circle(self.image, (255, 200, 50), (int(x), int(y)), 3)

    def _draw_jet_ship(self):
        c = self.color
        points = [(30, 0), (10, 30), (0, 50), (60, 50), (50, 30)]
        pygame.draw.polygon(self.image, c, points)
        pygame.draw.polygon(self.image, (c[0] // 2, c[1] // 2, c[2] // 2), [(30, 12), (18, 35), (42, 35)])
        pygame.draw.circle(self.image, (100, 200, 255), (30, 22), 5)
        pygame.draw.rect(self.image, (255, 150, 50), (8, 50, 8, 10))
        pygame.draw.rect(self.image, (255, 150, 50), (44, 50, 8, 10))
        pygame.draw.ellipse(self.image, (255, 100, 0, 150), (6, 58, 12, 8))
        pygame.draw.ellipse(self.image, (255, 100, 0, 150), (42, 58, 12, 8))
        pygame.draw.ellipse(self.image, (150, 230, 255), (22, 8, 16, 14))

    def _draw_arrow_ship(self):
        c = self.color
        points = [(30, 0), (0, 45), (15, 40), (15, 60), (45, 60), (45, 40), (60, 45)]
        pygame.draw.polygon(self.image, c, points)
        pygame.draw.polygon(self.image, (c[0] // 2, c[1] // 2, c[2] // 2), [(30, 15), (22, 40), (38, 40)])
        pygame.draw.circle(self.image, (255, 255, 200), (30, 25), 6)
        pygame.draw.circle(self.image, (200, 200, 255), (30, 25), 3)
        pygame.draw.line(self.image, (200, 200, 200), (8, 45), (52, 45), 2)
        pygame.draw.line(self.image, (200, 200, 200), (12, 50), (48, 50), 2)

    def change_color(self, color, skin_index=None):
        self.color = color
        if skin_index is not None:
            self.skin_index = skin_index
        self._draw_ship()

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)