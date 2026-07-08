import pygame
import random
from pygame.sprite import Sprite


class IntroAnimation:

    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings

        self.active = False
        self.finished = False
        self.timer = 0
        self.duration = 6000

        self.aliens = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.fire_particles = pygame.sprite.Group()
        self.ufo = None
        self.big_alien = None

        self.earth_image = self._create_earth()
        self.earth_rect = self.earth_image.get_rect()
        self.earth_rect.center = self.screen_rect.center

        self.fire_image = None

        self.font = pygame.font.SysFont('Arial', 60, bold=True)
        self.small_font = pygame.font.SysFont('Arial', 30)
        self.huge_font = pygame.font.SysFont('Arial', 100, bold=True)

        self.phase = 0
        self.fire_started = False
        self.big_alien_appeared = False

        self.show_final_text = False
        self.final_text_timer = 0

        self.clearing_screen = False
        self.clear_timer = 0

    def _create_earth(self):
        earth_surf = pygame.Surface((300, 300), pygame.SRCALPHA)

        pygame.draw.circle(earth_surf, (50, 150, 255), (150, 150), 140)

        continents = [
            (150, 130, 60, 40),
            (120, 150, 30, 50),
            (180, 140, 50, 30),
            (100, 110, 40, 30),
            (200, 110, 30, 20),
        ]
        for x, y, w, h in continents:
            pygame.draw.ellipse(earth_surf, (50, 200, 80), (x - w // 2, y - h // 2, w, h))

        for _ in range(10):
            x = random.randint(50, 250)
            y = random.randint(50, 250)
            r = random.randint(10, 25)
            pygame.draw.circle(earth_surf, (200, 220, 255, 100), (x, y), r)

        pygame.draw.circle(earth_surf, (100, 180, 255, 50), (150, 150), 145, 5)

        return earth_surf

    def _create_fire_on_earth(self):
        fire_surf = pygame.Surface((300, 300), pygame.SRCALPHA)

        fire_spots = [
            (80, 120, 30, 20), (150, 160, 40, 25), (200, 130, 25, 15),
            (100, 180, 35, 20), (170, 200, 30, 18), (130, 100, 20, 15),
            (220, 170, 25, 20), (60, 150, 20, 15), (180, 100, 25, 18),
            (110, 210, 30, 20), (140, 140, 45, 30), (190, 190, 35, 25),
            (75, 170, 25, 18), (210, 120, 30, 22), (120, 220, 28, 20),
            (160, 90, 22, 16), (200, 200, 32, 24), (90, 140, 26, 18),
            (50, 100, 20, 15), (250, 150, 25, 18), (170, 230, 30, 20),
        ]

        for x, y, w, h in fire_spots:
            pygame.draw.ellipse(fire_surf, (255, 100, 0, 200), (x - w // 2, y - h // 2, w, h))
            pygame.draw.ellipse(fire_surf, (255, 200, 50, 150), (x - w // 3, y - h // 3, w // 1.5, h // 1.5))
            pygame.draw.ellipse(fire_surf, (255, 50, 0, 100), (x - w // 4, y - h // 4, w // 2, h // 2))

        for i in range(15):
            x = random.randint(50, 250)
            y = random.randint(50, 250)
            r = random.randint(30, 60)
            pygame.draw.circle(fire_surf, (255, 100, 0, 30), (x, y), r)

        for i in range(20):
            x = random.randint(40, 260)
            y = random.randint(40, 260)
            r = random.randint(15, 30)
            pygame.draw.circle(fire_surf, (100, 100, 100, 60), (x, y), r)

        return fire_surf

    def _create_fire_particles(self):
        for _ in range(40):
            particle = FireParticle(
                self.screen_rect.centerx + random.randint(-150, 150),
                self.screen_rect.centery + random.randint(-80, 80)
            )
            self.fire_particles.add(particle)

    def _create_big_alien(self):
        self.big_alien = BigAlien(self.screen_rect)

    def start(self):
        self.active = True
        self.finished = False
        self.timer = 0
        self.phase = 0
        self.fire_started = False
        self.big_alien_appeared = False
        self.show_final_text = False
        self.final_text_timer = 0
        self.clearing_screen = False
        self.clear_timer = 0
        self.aliens.empty()
        self.explosions.empty()
        self.fire_particles.empty()
        self.big_alien = None
        self.fire_image = None
        self.earth_image = self._create_earth()

        self.ufo = UFO(self.screen_rect.centerx, -800, self.screen_rect)
        self.ufo.speed = 0.01

        self._create_first_wave()

    def _create_first_wave(self):
        for i in range(5):
            x = random.randint(50, self.screen_rect.width - 50)
            y = random.randint(-1500, -400)
            alien = IntroAlien(x, y, random.choice(['red', 'green', 'purple']))
            alien.speed = random.uniform(0.3, 0.8)
            alien.earth_rect = self.earth_rect
            alien.target_x = random.randint(100, self.screen_rect.width - 100)
            alien.target_y = self.earth_rect.centery - random.randint(20, 80)
            self.aliens.add(alien)

    def _create_second_wave(self):
        for i in range(8):
            x = random.randint(50, self.screen_rect.width - 50)
            y = random.randint(-1800, -400)
            alien = IntroAlien(x, y, random.choice(['red', 'green', 'purple']))
            alien.speed = random.uniform(0.4, 1.0)
            alien.earth_rect = self.earth_rect
            alien.target_x = random.randint(100, self.screen_rect.width - 100)
            alien.target_y = self.earth_rect.centery - random.randint(20, 80)
            self.aliens.add(alien)

        for i in range(5):
            x = random.randint(-600, -150)
            y = random.randint(100, self.screen_rect.height - 100)
            alien = IntroAlien(x, y, random.choice(['red', 'green', 'purple']))
            alien.speed = random.uniform(0.4, 1.0)
            alien.earth_rect = self.earth_rect
            alien.target_x = random.randint(100, self.screen_rect.width - 100)
            alien.target_y = self.earth_rect.centery - random.randint(20, 80)
            self.aliens.add(alien)

        for i in range(5):
            x = random.randint(self.screen_rect.width + 150, self.screen_rect.width + 600)
            y = random.randint(100, self.screen_rect.height - 100)
            alien = IntroAlien(x, y, random.choice(['red', 'green', 'purple']))
            alien.speed = random.uniform(0.4, 1.0)
            alien.earth_rect = self.earth_rect
            alien.target_x = random.randint(100, self.screen_rect.width - 100)
            alien.target_y = self.earth_rect.centery - random.randint(20, 80)
            self.aliens.add(alien)

    def _create_final_wave(self):
        for i in range(30):
            side = random.choice(['top', 'bottom', 'left', 'right'])
            if side == 'top':
                x = random.randint(0, self.screen_rect.width)
                y = random.randint(-1800, -300)
            elif side == 'bottom':
                x = random.randint(0, self.screen_rect.width)
                y = random.randint(self.screen_rect.height + 300, self.screen_rect.height + 1800)
            elif side == 'left':
                x = random.randint(-1800, -300)
                y = random.randint(0, self.screen_rect.height)
            else:
                x = random.randint(self.screen_rect.width + 300, self.screen_rect.width + 1800)
                y = random.randint(0, self.screen_rect.height)

            alien = IntroAlien(x, y, random.choice(['red', 'green', 'purple']))
            alien.speed = random.uniform(0.5, 1.2)
            alien.earth_rect = self.earth_rect
            alien.target_x = random.randint(100, self.screen_rect.width - 100)
            alien.target_y = self.earth_rect.centery - random.randint(20, 80)
            self.aliens.add(alien)

    def update(self):
        if not self.active:
            return

        self.timer += 1

        if self.clearing_screen:
            self.clear_timer += 1
            if self.clear_timer > 180:
                self.clearing_screen = False
                self.show_final_text = True
                self.final_text_timer = self.timer
            return

        if self.ufo:
            self.ufo.update()

        if self.timer % 200 == 0 and self.ufo and self.ufo.rect.y > 50:
            self._create_laser()

        for alien in self.aliens.copy():
            alien.update()
            if alien.rect.centery >= self.earth_rect.centery - 50:
                explosion = Explosion(alien.rect.centerx, self.earth_rect.centery - 50)
                self.explosions.add(explosion)
                self.aliens.remove(alien)

        for explosion in self.explosions.copy():
            explosion.update()
            if explosion.finished:
                self.explosions.remove(explosion)

        for particle in self.fire_particles.copy():
            particle.update()
            if particle.finished:
                self.fire_particles.remove(particle)

        if self.big_alien:
            self.big_alien.update()

        if self.phase >= 1 and not self.fire_started:
            self.fire_started = True
            self.fire_image = self._create_fire_on_earth()
            self._create_fire_particles()

        if self.phase >= 2 and not self.big_alien_appeared:
            if self.timer >= 3900:
                self.big_alien_appeared = True
                self._create_big_alien()

        if self.big_alien_appeared and not self.show_final_text:
            if self.timer >= 5000:
                self.aliens.empty()
                self.explosions.empty()
                self.fire_particles.empty()
                self.fire_image = None
                self.big_alien = None
                self.ufo = None
                self.earth_image = None

                self.clearing_screen = True
                self.clear_timer = 0

        if self.timer < 1500:
            self.phase = 0
        elif self.timer < 3000:
            self.phase = 1
            if self.timer == 1500:
                self._create_second_wave()
        elif self.timer < 4500:
            self.phase = 2
            if self.timer == 3000:
                self._create_final_wave()

        if self.show_final_text and self.timer - self.final_text_timer > 900:  # ← было 480
            self.active = False
            self.finished = True

        if self.timer >= self.duration:
            self.active = False
            self.finished = True

    def _create_laser(self):
        if self.ufo:
            laser = Laser(self.ufo.rect.centerx, self.ufo.rect.bottom)
            self.explosions.add(laser)

    def draw(self):
        if not self.active:
            return

        self.screen.fill((5, 5, 20))

        if self.clearing_screen:
            return

        if self.show_final_text:
            pulse = abs(pygame.math.Vector2(1, 0).rotate(self.timer * 2)[1])
            alpha = int(180 + 75 * pulse)

            text1 = "СПАСИ"
            text2 = "ЖИТЕЛЕЙ ЗЕМЛИ"

            text1_surf = self.huge_font.render(text1, True, (255, 255, 100))
            text1_surf.set_alpha(alpha)
            text2_surf = self.huge_font.render(text2, True, (255, 255, 100))
            text2_surf.set_alpha(alpha)

            shadow1_surf = self.huge_font.render(text1, True, (100, 50, 0))
            shadow1_surf.set_alpha(alpha)
            shadow2_surf = self.huge_font.render(text2, True, (100, 50, 0))
            shadow2_surf.set_alpha(alpha)

            text1_rect = text1_surf.get_rect()
            text1_rect.centerx = self.screen_rect.centerx
            text1_rect.centery = self.screen_rect.centery - 60

            text2_rect = text2_surf.get_rect()
            text2_rect.centerx = self.screen_rect.centerx
            text2_rect.centery = self.screen_rect.centery + 60

            shadow1_rect = shadow1_surf.get_rect()
            shadow1_rect.centerx = self.screen_rect.centerx + 4
            shadow1_rect.centery = self.screen_rect.centery - 56

            shadow2_rect = shadow2_surf.get_rect()
            shadow2_rect.centerx = self.screen_rect.centerx + 4
            shadow2_rect.centery = self.screen_rect.centery + 64

            self.screen.blit(shadow1_surf, shadow1_rect)
            self.screen.blit(shadow2_surf, shadow2_rect)

            self.screen.blit(text1_surf, text1_rect)
            self.screen.blit(text2_surf, text2_rect)

            sub_text = "ПРИШЕЛЬЦЫ ЗАХВАТИЛИ ЗЕМЛЮ"
            sub_surf = self.small_font.render(sub_text, True, (255, 200, 200))
            sub_surf.set_alpha(alpha)
            sub_rect = sub_surf.get_rect()
            sub_rect.centerx = self.screen_rect.centerx
            sub_rect.top = text2_rect.bottom + 30
            self.screen.blit(sub_surf, sub_rect)

            return

        if self.big_alien:
            self.big_alien.draw(self.screen)

        if self.earth_image:
            self.screen.blit(self.earth_image, self.earth_rect)

        if self.fire_image:
            self.screen.blit(self.fire_image, self.earth_rect)

        self.fire_particles.draw(self.screen)
        self.explosions.draw(self.screen)
        self.aliens.draw(self.screen)

        if self.ufo:
            self.ufo.draw(self.screen)

        if not self.show_final_text:
            if self.phase == 0:
                text = "ПРИБЫТИЕ ПРИШЕЛЬЦЕВ"
                color = (255, 150, 150)
            elif self.phase == 1:
                text = "ВТОРЖЕНИЕ НАЧАЛОСЬ"
                color = (255, 200, 50)
            else:
                text = "ЗЕМЛЯ ГОРИТ"
                color = (255, 50, 50)

            text_surf = self.font.render(text, True, color)
            text_rect = text_surf.get_rect()
            text_rect.centerx = self.screen_rect.centerx
            text_rect.top = 50
            self.screen.blit(text_surf, text_rect)

        if not self.show_final_text:
            progress = self.timer / self.duration
            bar_width = 400
            bar_height = 10
            bar_x = self.screen_rect.centerx - bar_width // 2
            bar_y = self.screen_rect.bottom - 50

            pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(self.screen, (255, 100, 0), (bar_x, bar_y, int(bar_width * progress), bar_height))

            progress_text = f"Захват Земли {int(progress * 100)}%"
            prog_surf = self.small_font.render(progress_text, True, (200, 200, 200))
            prog_rect = prog_surf.get_rect()
            prog_rect.centerx = self.screen_rect.centerx
            prog_rect.bottom = bar_y - 10
            self.screen.blit(prog_surf, prog_rect)

    def is_finished(self):
        return self.finished


class UFO(Sprite):
    def __init__(self, x, y, screen_rect):
        super().__init__()
        self.screen_rect = screen_rect

        self.image = pygame.Surface((120, 60), pygame.SRCALPHA)

        pygame.draw.ellipse(self.image, (150, 150, 200), (0, 15, 120, 40))
        pygame.draw.ellipse(self.image, (200, 200, 255), (0, 15, 120, 40), 2)
        pygame.draw.ellipse(self.image, (100, 200, 255), (38, 0, 44, 28))
        pygame.draw.ellipse(self.image, (150, 230, 255), (38, 0, 44, 28), 2)

        for i in range(9):
            pygame.draw.circle(self.image, (255, 255, 100), (6 + i * 14, 45), 4)

        self.rect = self.image.get_rect()
        self.rect.x = x - self.rect.width // 2
        self.rect.y = y
        self.speed = 0.01

    def update(self):
        if self.rect.y < self.screen_rect.centery - 100:
            self.rect.y += self.speed
        else:
            self.rect.x += pygame.math.Vector2(1, 0).rotate(pygame.time.get_ticks() / 4000)[0] * 0.015

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class IntroAlien(Sprite):
    def __init__(self, x, y, color_type='red'):
        super().__init__()

        self.image = pygame.Surface((36, 36), pygame.SRCALPHA)

        colors = {
            'red': (255, 50, 50),
            'green': (50, 255, 50),
            'purple': (200, 50, 255)
        }
        color = colors.get(color_type, (255, 50, 50))

        pygame.draw.circle(self.image, color, (18, 18), 14)

        pygame.draw.circle(self.image, (255, 255, 255), (12, 14), 5)
        pygame.draw.circle(self.image, (255, 255, 255), (24, 14), 5)
        pygame.draw.circle(self.image, (0, 0, 0), (12, 14), 3)
        pygame.draw.circle(self.image, (0, 0, 0), (24, 14), 3)

        pygame.draw.arc(self.image, (255, 255, 255), (12, 20, 12, 8), 0.1, 3.0, 2)

        pygame.draw.line(self.image, color, (10, 6), (6, 0), 2)
        pygame.draw.line(self.image, color, (26, 6), (30, 0), 2)
        pygame.draw.circle(self.image, (255, 200, 50), (6, 0), 4)
        pygame.draw.circle(self.image, (255, 200, 50), (30, 0), 4)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.target_x = None
        self.target_y = None
        self.earth_rect = None
        self.speed = random.uniform(0.3, 0.8)

    def update(self):
        if self.target_x is not None and self.target_y is not None:
            dx = self.target_x - self.rect.x
            dy = self.target_y - self.rect.y
            dist = (dx ** 2 + dy ** 2) ** 0.5
            if dist > 0:
                self.rect.x += (dx / dist) * self.speed
                self.rect.y += (dy / dist) * self.speed


class Explosion(Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.size = 0
        self.max_size = 35
        self.life = 70
        self.finished = False

        self.update()

    def update(self):
        if self.life > 0:
            self.life -= 1
            self.size += 0.5
            self.image.fill((0, 0, 0, 0))

            for i in range(3):
                alpha = 255 - i * 80
                size = self.size - i * 5
                if size > 0:
                    pygame.draw.circle(self.image, (255, 200, 50, alpha),
                                       (25, 25), size)

            pygame.draw.circle(self.image, (255, 255, 200, 200),
                               (25, 25), max(2, self.size // 3))

            for i in range(8):
                angle = i * 45 + self.life * 0.5
                length = self.size + 5
                dx = length * pygame.math.Vector2(1, 0).rotate(angle)[0]
                dy = length * pygame.math.Vector2(1, 0).rotate(angle)[1]
                pygame.draw.line(self.image, (255, 200, 50, 100),
                                 (25, 25), (25 + dx, 25 + dy), 1)
        else:
            self.finished = True


class Laser(Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface((4, 300), pygame.SRCALPHA)

        for i in range(300):
            alpha = 255 - i // 2
            pygame.draw.line(self.image, (255, 50, 50, alpha),
                             (2, i), (2, i), 2)

        pygame.draw.line(self.image, (255, 100, 100, 50),
                         (0, 0), (0, 300), 8)
        pygame.draw.line(self.image, (255, 100, 100, 50),
                         (4, 0), (4, 300), 8)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y

        self.life = 60
        self.finished = False

    def update(self):
        self.life -= 1
        if self.life <= 0:
            self.finished = True


class FireParticle(Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.x = float(x)
        self.y = float(y)

        self.dx = random.uniform(-0.15, 0.15)
        self.dy = random.uniform(-0.8, -0.15)

        self.size = random.randint(3, 8)
        self.max_size = self.size
        self.grow = random.uniform(0.01, 0.025)

        self.color = (
            random.randint(200, 255),
            random.randint(50, 150),
            random.randint(0, 50)
        )

        self.life = random.randint(100, 200)
        self.max_life = self.life
        self.finished = False

        self.update_surface()

    def update_surface(self):
        self.image.fill((0, 0, 0, 0))

        progress = 1 - (self.life / self.max_life)
        current_size = self.size * (1 + progress * 2)

        alpha = int(255 * (1 - progress))
        pygame.draw.circle(self.image, (self.color[0], self.color[1], self.color[2], alpha),
                           (10, 10), int(current_size))

        if current_size > 2:
            pygame.draw.circle(self.image, (255, 255, 200, alpha // 2),
                               (10, 10), max(1, int(current_size // 2)))

    def update(self):
        self.life -= 1
        if self.life <= 0:
            self.finished = True
            return

        self.x += self.dx + random.uniform(-0.03, 0.03)
        self.y += self.dy
        self.size += self.grow

        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

        self.update_surface()

        if self.rect.bottom < 0:
            self.finished = True


class BigAlien:
    def __init__(self, screen_rect):
        self.screen_rect = screen_rect

        self.image = pygame.Surface((600, 750), pygame.SRCALPHA)

        self.primary_color = (80, 30, 130)
        self.secondary_color = (130, 60, 180)

        pygame.draw.circle(self.image, self.primary_color, (300, 350), 280)

        pygame.draw.circle(self.image, (255, 255, 255), (200, 280), 80)
        pygame.draw.circle(self.image, (255, 255, 255), (400, 280), 80)
        pygame.draw.circle(self.image, (255, 0, 0), (200, 280), 45)
        pygame.draw.circle(self.image, (255, 0, 0), (400, 280), 45)
        pygame.draw.circle(self.image, (200, 0, 0), (200, 280), 30)
        pygame.draw.circle(self.image, (200, 0, 0), (400, 280), 30)
        pygame.draw.circle(self.image, (255, 255, 255), (180, 260), 20)
        pygame.draw.circle(self.image, (255, 255, 255), (380, 260), 20)
        pygame.draw.circle(self.image, (255, 255, 255), (175, 265), 10)
        pygame.draw.circle(self.image, (255, 255, 255), (375, 265), 10)

        pygame.draw.arc(self.image, (200, 50, 50), (180, 360, 240, 120), 0.1, 3.0, 12)

        for i in range(4):
            x = 220 + i * 55
            pygame.draw.polygon(self.image, (255, 255, 255), [
                (x, 390),
                (x + 15, 440),
                (x + 30, 390)
            ])
            pygame.draw.polygon(self.image, (200, 200, 200), [
                (x + 2, 390),
                (x + 15, 435),
                (x + 28, 390)
            ])

        tentacles = [
            (60, 600, 150, 120, -40),
            (150, 620, 130, 100, -20),
            (240, 640, 120, 80, -10),
            (360, 640, 120, 80, 10),
            (450, 620, 130, 100, 20),
            (540, 600, 150, 120, 40),
        ]

        for x, y, w, h, angle in tentacles:
            tentacle = pygame.Surface((w, h), pygame.SRCALPHA)
            pygame.draw.ellipse(tentacle, self.primary_color, (0, 0, w, h))
            pygame.draw.ellipse(tentacle, self.secondary_color, (5, 5, w - 10, h - 10), 2)
            tentacle = pygame.transform.rotate(tentacle, angle)
            self.image.blit(tentacle, (x - w // 2, y - h // 2))

        arm_tentacles = [
            (-80, 200, 200, 60, -20),
            (680, 200, 200, 60, 20),
        ]

        for x, y, w, h, angle in arm_tentacles:
            tentacle = pygame.Surface((w, h), pygame.SRCALPHA)
            pygame.draw.ellipse(tentacle, self.primary_color, (0, 0, w, h))
            tentacle = pygame.transform.rotate(tentacle, angle)
            self.image.blit(tentacle, (x, y - h // 2))

        for i in range(5):
            glow_size = 280 + i * 30
            alpha = 60 - i * 10
            pygame.draw.circle(self.image, (150, 80, 200, alpha),
                               (300, 350), glow_size, 4)

        for i in range(2):
            glow_size = 60 + i * 20
            pygame.draw.circle(self.image, (255, 0, 0, 30 - i * 10),
                               (200, 280), glow_size)
            pygame.draw.circle(self.image, (255, 0, 0, 30 - i * 10),
                               (400, 280), glow_size)

        self.rect = self.image.get_rect()
        self.rect.centerx = screen_rect.centerx
        self.rect.bottom = screen_rect.bottom + 100

        self.appearing = True
        self.appear_progress = 0
        self.appear_speed = 0.002

        self.wobble = 0
        self.pulse = 0

    def update(self):
        if self.appearing:
            self.appear_progress += self.appear_speed
            if self.appear_progress >= 1:
                self.appear_progress = 1
                self.appearing = False

            target_y = self.screen_rect.bottom - self.rect.height // 2 + 50
            current_y = self.screen_rect.bottom + 150 - (
                        self.appear_progress * (self.screen_rect.bottom + 150 - target_y))
            self.rect.centery = int(current_y)

        self.wobble += 0.008
        self.pulse += 0.015

        self.rect.x += pygame.math.Vector2(1, 0).rotate(self.wobble * 20)[0] * 0.15

    def draw(self, screen):
        if self.appearing:
            alpha = int(255 * self.appear_progress)
            temp_image = self.image.copy()
            temp_image.set_alpha(alpha)
            screen.blit(temp_image, self.rect)
        else:
            screen.blit(self.image, self.rect)