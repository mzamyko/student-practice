import pygame
import random
from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, ai_game, alien_type='green'):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.ai_game = ai_game
        self.alien_type = alien_type

        self.size_timer = random.randint(0, 100)
        self.current_size = 1.0

        self.image = pygame.Surface((48, 56), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))

        self._draw_alien()
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

        self.shoot_timer = random.randint(0, 100)
        self.shoot_delay = random.randint(2400, 3000)  # 40-50 секунд

    def _draw_alien(self):
        self.image.fill((0, 0, 0, 0))

        if self.alien_type == 'green':
            self._draw_green_alien()
        elif self.alien_type == 'pink':
            self._draw_pink_alien()
        elif self.alien_type == 'yellow':
            self._draw_yellow_alien()
        elif self.alien_type == 'blue':
            self._draw_blue_alien()

    def _draw_green_alien(self):
        def s(v): return int(v * 0.85)

        pygame.draw.circle(self.image, (50, 200, 80), (24, 22), s(22))
        pygame.draw.circle(self.image, (80, 220, 100), (24, 22), s(22), 2)
        pygame.draw.ellipse(self.image, (50, 200, 80), (s(14), s(3), s(28), s(26)))
        pygame.draw.circle(self.image, (255, 255, 255), (s(20), s(18)), s(9))
        pygame.draw.circle(self.image, (255, 255, 255), (s(34), s(18)), s(9))
        pygame.draw.circle(self.image, (0, 0, 0), (s(22), s(19)), s(5))
        pygame.draw.circle(self.image, (0, 0, 0), (s(36), s(19)), s(5))
        pygame.draw.circle(self.image, (255, 255, 255), (s(20), s(17)), s(2))
        pygame.draw.circle(self.image, (255, 255, 255), (s(34), s(17)), s(2))
        pygame.draw.arc(self.image, (200, 50, 50), (s(20), s(24), s(16), s(11)), 0.1, 3.0, 2)
        pygame.draw.circle(self.image, (255, 150, 150, 150), (s(14), s(24)), s(5))
        pygame.draw.circle(self.image, (255, 150, 150, 150), (s(40), s(24)), s(5))
        pygame.draw.line(self.image, (50, 200, 80), (s(17), s(6)), (s(10), s(-2)), 2)
        pygame.draw.line(self.image, (50, 200, 80), (s(37), s(6)), (s(44), s(-2)), 2)
        pygame.draw.circle(self.image, (255, 200, 50), (s(10), s(-2)), s(5))
        pygame.draw.circle(self.image, (255, 200, 50), (s(44), s(-2)), s(5))
        pygame.draw.circle(self.image, (255, 255, 200), (s(10), s(-3)), s(2))
        pygame.draw.circle(self.image, (255, 255, 200), (s(44), s(-3)), s(2))
        pygame.draw.ellipse(self.image, (50, 200, 80), (s(18), s(34), s(22), s(17)))
        pygame.draw.line(self.image, (50, 200, 80), (s(10), s(30)), (s(4), s(40)), 3)
        pygame.draw.line(self.image, (50, 200, 80), (s(44), s(30)), (s(50), s(40)), 3)
        pygame.draw.circle(self.image, (50, 200, 80), (s(4), s(40)), s(5))
        pygame.draw.circle(self.image, (50, 200, 80), (s(50), s(40)), s(5))
        pygame.draw.line(self.image, (50, 200, 80), (s(20), s(46)), (s(17), s(52)), 2)
        pygame.draw.line(self.image, (50, 200, 80), (s(34), s(46)), (s(37), s(52)), 2)
        pygame.draw.ellipse(self.image, (80, 220, 100), (s(14), s(50), s(9), s(5)))
        pygame.draw.ellipse(self.image, (80, 220, 100), (s(32), s(50), s(9), s(5)))
        pygame.draw.circle(self.image, (80, 180, 100, 100), (s(22), s(32)), s(4))
        pygame.draw.circle(self.image, (80, 180, 100, 100), (s(32), s(32)), s(4))
        pygame.draw.circle(self.image, (80, 180, 100, 100), (s(27), s(38)), s(4))

    def _draw_pink_alien(self):
        def s(v): return int(v * 0.85)

        pygame.draw.circle(self.image, (255, 100, 150), (24, 22), s(22))
        pygame.draw.circle(self.image, (255, 80, 130), (24, 22), s(22), 2)
        pygame.draw.circle(self.image, (255, 255, 255), (s(20), s(18)), s(9))
        pygame.draw.circle(self.image, (255, 255, 255), (s(34), s(18)), s(9))
        pygame.draw.circle(self.image, (255, 0, 0), (s(22), s(19)), s(6))
        pygame.draw.circle(self.image, (255, 0, 0), (s(36), s(19)), s(6))
        pygame.draw.circle(self.image, (0, 0, 0), (s(22), s(19)), s(4))
        pygame.draw.circle(self.image, (0, 0, 0), (s(36), s(19)), s(4))
        pygame.draw.arc(self.image, (200, 50, 50), (s(18), s(24), s(20), s(11)), 3.5, 6.0, 2)
        pygame.draw.line(self.image, (255, 100, 150), (s(17), s(6)), (s(10), s(-2)), 2)
        pygame.draw.line(self.image, (255, 100, 150), (s(37), s(6)), (s(44), s(-2)), 2)
        pygame.draw.circle(self.image, (255, 50, 50), (s(10), s(-2)), s(6))
        pygame.draw.circle(self.image, (255, 50, 50), (s(44), s(-2)), s(6))
        pygame.draw.circle(self.image, (50, 50, 50), (24, s(37)), s(9))
        pygame.draw.circle(self.image, (200, 50, 50), (24, s(37)), s(6))
        pygame.draw.rect(self.image, (50, 50, 50), (s(25), s(30), s(5), s(6)))
        pygame.draw.circle(self.image, (255, 100, 50, 100), (24, s(37)), s(14), 2)
        pygame.draw.line(self.image, (255, 100, 150), (s(20), s(46)), (s(17), s(52)), 3)
        pygame.draw.line(self.image, (255, 100, 150), (s(34), s(46)), (s(37), s(52)), 3)

    def _draw_yellow_alien(self):
        def s(v): return int(v * 0.85)

        pygame.draw.ellipse(self.image, (255, 215, 0), (s(6), s(6), s(44), s(34)))
        pygame.draw.ellipse(self.image, (255, 200, 0), (s(6), s(6), s(44), s(34)), 2)
        pygame.draw.circle(self.image, (255, 215, 0), (s(27), s(10)), s(12))
        pygame.draw.line(self.image, (255, 200, 0), (s(22), s(6)), (s(18), s(-2)), 2)
        pygame.draw.line(self.image, (255, 200, 0), (s(32), s(6)), (s(36), s(-2)), 2)
        pygame.draw.circle(self.image, (255, 255, 255), (s(18), s(-2)), s(5))
        pygame.draw.circle(self.image, (255, 255, 255), (s(36), s(-2)), s(5))
        pygame.draw.circle(self.image, (0, 0, 0), (s(18), s(-2)), s(3))
        pygame.draw.circle(self.image, (0, 0, 0), (s(36), s(-2)), s(3))
        pygame.draw.rect(self.image, (200, 150, 0), (s(24), s(14), s(7), s(5)))
        for i in range(5):
            x = s(47 + i * 5)
            y = s(17 + i * 3)
            pygame.draw.circle(self.image, (255, 215, 0), (x, y), s(6 - i * 0.9))
        pygame.draw.line(self.image, (255, 215, 0), (s(6), s(17)), (s(0), s(12)), 3)
        pygame.draw.line(self.image, (255, 215, 0), (s(48), s(17)), (s(53), s(12)), 3)
        pygame.draw.circle(self.image, (255, 200, 0), (s(0), s(12)), s(5))
        pygame.draw.circle(self.image, (255, 200, 0), (s(53), s(12)), s(5))

    def _draw_blue_alien(self):
        def s(v): return int(v * 0.85)

        size = self.current_size
        cx, cy = 24, 24
        r = int(s(20) * size)

        pygame.draw.circle(self.image, (100, 200, 255), (cx, cy), r)
        pygame.draw.circle(self.image, (50, 150, 255), (cx, cy), r, 2)

        es = int(s(8) * size)
        pygame.draw.circle(self.image, (255, 255, 255), (cx - s(9), cy - s(5)), es)
        pygame.draw.circle(self.image, (255, 255, 255), (cx + s(9), cy - s(5)), es)
        pygame.draw.circle(self.image, (0, 0, 200), (cx - s(9), cy - s(5)), int(s(5) * size))
        pygame.draw.circle(self.image, (0, 0, 200), (cx + s(9), cy - s(5)), int(s(5) * size))
        pygame.draw.circle(self.image, (255, 255, 255), (cx - s(11), cy - s(7)), int(s(2) * size))
        pygame.draw.circle(self.image, (255, 255, 255), (cx + s(7), cy - s(7)), int(s(2) * size))
        pygame.draw.circle(self.image, (50, 50, 150), (cx, cy + s(7)), int(s(6) * size))
        pygame.draw.circle(self.image, (0, 0, 50), (cx, cy + s(7)), int(s(4) * size))
        for i in range(6):
            ang = i * 60
            l = int(s(14) * size)
            x = cx + l * pygame.math.Vector2(1, 0).rotate(ang)[0]
            y = cy + l * pygame.math.Vector2(1, 0).rotate(ang)[1]
            pygame.draw.line(self.image, (100, 200, 255), (cx, cy), (x, y), 2)
            pygame.draw.circle(self.image, (50, 150, 255), (int(x), int(y)), int(s(4) * size))

    def update(self):
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

        if self.alien_type == 'blue':
            self.size_timer += 0.02
            self.current_size = 1.0 + 0.3 * (pygame.math.Vector2(1, 0).rotate(self.size_timer * 180)[1])
            self._draw_alien()
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            self.x = float(self.rect.x)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def should_shoot(self):
        """Проверяет, должен ли жёлтый пришелец стрелять."""
        if self.alien_type != 'yellow':
            return False
        self.shoot_timer += 1
        # ОЧЕНЬ-ОЧЕНЬ МЕДЛЕННО: 1 выстрел в 40-50 секунд
        if self.shoot_timer >= self.shoot_delay:
            self.shoot_timer = 0
            self.shoot_delay = random.randint(2400, 3000)
            return True
        return False