import pygame
import random
from pygame.sprite import Sprite


class VictoryCelebration:
    """Класс для анимации победы с салютом."""

    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.active = False
        self.finished = False
        self.timer = 0
        self.duration = 300  # 5 секунд

        self.particles = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()

        self.font = pygame.font.SysFont('Arial', 120, bold=True)
        self.small_font = pygame.font.SysFont('Arial', 40)

    def start(self):
        """Запускает анимацию победы."""
        self.active = True
        self.finished = False
        self.timer = 0
        self.particles.empty()
        self.stars.empty()

        # Создаём звёздочки для фона
        for _ in range(50):
            star = CelebrationStar(self.screen_rect)
            self.stars.add(star)

        # Первый залп салюта
        self._create_salvo()

    def _create_salvo(self):
        """Создаёт залп салюта."""
        for _ in range(8):
            x = random.randint(100, self.screen_rect.width - 100)
            y = random.randint(100, self.screen_rect.height // 2)
            particle = FireworkParticle(x, y, random.choice(['red', 'blue', 'green', 'yellow', 'purple', 'orange']))
            self.particles.add(particle)

    def update(self):
        """Обновляет анимацию."""
        if not self.active:
            return

        self.timer += 1

        # Обновляем частицы
        for particle in self.particles.copy():
            particle.update()
            if particle.finished:
                self.particles.remove(particle)

        # Обновляем звёзды
        for star in self.stars.copy():
            star.update()

        # Каждые 15 кадров новый залп
        if self.timer % 15 == 0 and self.timer < self.duration - 30:
            self._create_salvo()

        # Завершение
        if self.timer >= self.duration:
            self.active = False
            self.finished = True

    def draw(self):
        """Рисует анимацию."""
        if not self.active:
            return

        # Тёмный фон
        self.screen.fill((5, 5, 30))

        # Звёзды
        self.stars.draw(self.screen)

        # Частицы салюта
        self.particles.draw(self.screen)

        # Надпись "ПОБЕДА!"
        pulse = abs(pygame.math.Vector2(1, 0).rotate(self.timer * 3)[1])
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

        # Счёт
        score_text = f"Счёт: {self.ai_game.stats.total_score}  |  Пули: {self.ai_game.stats.bullets_fired}"
        score_surf = self.small_font.render(score_text, True, (200, 200, 200))
        score_surf.set_alpha(alpha)
        score_rect = score_surf.get_rect()
        score_rect.centerx = self.screen_rect.centerx
        score_rect.top = sub_rect.bottom + 15
        self.screen.blit(score_surf, score_rect)

    def is_finished(self):
        return self.finished


class FireworkParticle(Sprite):
    """Класс для частицы салюта."""

    def __init__(self, x, y, color_type='red'):
        super().__init__()

        colors = {
            'red': (255, 50, 50),
            'blue': (50, 150, 255),
            'green': (50, 255, 50),
            'yellow': (255, 215, 0),
            'purple': (200, 50, 255),
            'orange': (255, 150, 50),
        }
        self.color = colors.get(color_type, (255, 255, 255))

        self.size = random.randint(3, 8)
        self.image = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.x = float(x)
        self.y = float(y)

        # Скорость в случайном направлении
        angle = random.uniform(0, 360)
        speed = random.uniform(2, 6)
        self.speed_x = speed * pygame.math.Vector2(1, 0).rotate(angle)[0]
        self.speed_y = speed * pygame.math.Vector2(1, 0).rotate(angle)[1]

        self.life = random.randint(30, 60)
        self.max_life = self.life
        self.finished = False

        # След частицы
        self.trail = []

        self.update_surface()

    def update_surface(self):
        """Обновляет изображение частицы."""
        self.image.fill((0, 0, 0, 0))

        progress = 1 - (self.life / self.max_life)
        current_size = self.size * (1 - progress * 0.5)

        if current_size > 1:
            alpha = int(255 * (1 - progress))
            pygame.draw.circle(self.image, (self.color[0], self.color[1], self.color[2], alpha),
                             (self.size, self.size), int(current_size))
            # Свечение
            pygame.draw.circle(self.image, (255, 255, 200, alpha // 2),
                             (self.size, self.size), int(current_size * 1.5), 1)

    def update(self):
        """Обновляет частицу."""
        self.life -= 1
        if self.life <= 0:
            self.finished = True
            return

        self.x += self.speed_x
        self.y += self.speed_y
        self.speed_y += 0.05  # Гравитация

        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

        self.update_surface()


class CelebrationStar(Sprite):
    """Класс для мерцающей звезды на фоне."""

    def __init__(self, screen_rect):
        super().__init__()

        self.screen_rect = screen_rect
        self.size = random.randint(1, 3)
        self.brightness = random.randint(100, 255)
        self.direction = 1
        self.speed = random.uniform(0.01, 0.03)

        self.image = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_rect.width)
        self.rect.y = random.randint(0, screen_rect.height)

        self.update_surface()

    def update_surface(self):
        """Обновляет изображение звезды."""
        self.image.fill((0, 0, 0, 0))
        color = int(self.brightness)
        pygame.draw.circle(self.image, (color, color, color), (self.size, self.size), self.size)

    def update(self):
        """Обновляет мерцание звезды."""
        self.brightness += self.speed * self.direction
        if self.brightness > 255:
            self.brightness = 255
            self.direction = -1
        elif self.brightness < 50:
            self.brightness = 50
            self.direction = 1
        self.update_surface()