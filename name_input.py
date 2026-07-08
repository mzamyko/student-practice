import pygame
import pygame.font


class NameInput:
    """Класс для окна ввода имени при победе."""

    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        self.active = False
        self.name = ""
        self.max_length = 15

        # Шрифты
        self.font = pygame.font.SysFont('Arial', 60, bold=True)
        self.font_small = pygame.font.SysFont('Arial', 40)
        self.font_tiny = pygame.font.SysFont('Arial', 30)

        # Цвета
        self.bg_color = (10, 10, 40)
        self.text_color = (255, 255, 255)
        self.highlight_color = (255, 215, 0)

        # Прямоугольник для ввода
        self.input_rect = pygame.Rect(
            self.screen_rect.centerx - 200,
            self.screen_rect.centery - 30,
            400,
            60
        )

        self.cursor_visible = True
        self.cursor_timer = 0

    def start(self):
        """Запускает окно ввода."""
        self.active = True
        self.name = ""
        self.cursor_visible = True
        self.cursor_timer = 0

    def add_char(self, char):
        """Добавляет символ к имени."""
        if len(self.name) < self.max_length:
            self.name += char

    def remove_char(self):
        """Удаляет последний символ."""
        if len(self.name) > 0:
            self.name = self.name[:-1]

    def get_name(self):
        """Возвращает введённое имя."""
        return self.name.strip() if self.name.strip() else "Player"

    def update(self):
        """Обновляет курсор."""
        if self.active:
            self.cursor_timer += 1
            if self.cursor_timer >= 30:
                self.cursor_timer = 0
                self.cursor_visible = not self.cursor_visible

    def handle_event(self, event):
        """Обрабатывает события ввода."""
        if not self.active:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.active = False
                return True
            elif event.key == pygame.K_BACKSPACE:
                self.remove_char()
            else:
                char = event.unicode
                if char.isprintable() and not char in '\r\n\t':
                    self.add_char(char)
        return False

    def draw(self):
        """Рисует окно ввода имени."""
        if not self.active:
            return

        overlay = pygame.Surface((self.screen_rect.width, self.screen_rect.height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        title_text = "ПОБЕДА!"
        title_surf = self.font.render(title_text, True, (255, 215, 0))
        title_rect = title_surf.get_rect()
        title_rect.centerx = self.screen_rect.centerx
        title_rect.top = 80
        self.screen.blit(title_surf, title_rect)

        # Общий счёт
        total_text = f"Общий счёт: {self.stats.total_score}"
        total_surf = self.font_small.render(total_text, True, (255, 255, 255))
        total_rect = total_surf.get_rect()
        total_rect.centerx = self.screen_rect.centerx
        total_rect.top = title_rect.bottom + 20
        self.screen.blit(total_surf, total_rect)

        # Счёт за уровень
        level_text = f"Счёт за уровень: {self.stats.level_score}"
        level_surf = self.font_small.render(level_text, True, (200, 200, 200))
        level_rect = level_surf.get_rect()
        level_rect.centerx = self.screen_rect.centerx
        level_rect.top = total_rect.bottom + 10
        self.screen.blit(level_surf, level_rect)

        # Пули
        bullets_text = f"Выпущено пуль: {self.stats.bullets_fired}"
        bullets_surf = self.font_small.render(bullets_text, True, (200, 200, 200))
        bullets_rect = bullets_surf.get_rect()
        bullets_rect.centerx = self.screen_rect.centerx
        bullets_rect.top = level_rect.bottom + 10
        self.screen.blit(bullets_surf, bullets_rect)

        label_text = "Введите ваше имя:"
        label_surf = self.font_small.render(label_text, True, (200, 200, 200))
        label_rect = label_surf.get_rect()
        label_rect.centerx = self.screen_rect.centerx
        label_rect.top = bullets_rect.bottom + 40
        self.screen.blit(label_surf, label_rect)

        pygame.draw.rect(self.screen, (50, 50, 80), self.input_rect, border_radius=10)
        pygame.draw.rect(self.screen, (100, 100, 150), self.input_rect, 2, border_radius=10)

        display_name = self.name
        if self.cursor_visible and len(self.name) < self.max_length:
            display_name += "|"

        name_surf = self.font_small.render(display_name, True, (255, 255, 255))
        name_rect = name_surf.get_rect()
        name_rect.centerx = self.input_rect.centerx
        name_rect.centery = self.input_rect.centery
        self.screen.blit(name_surf, name_rect)

        hint_text = "Нажмите ENTER для сохранения"
        hint_surf = self.font_tiny.render(hint_text, True, (150, 150, 150))
        hint_rect = hint_surf.get_rect()
        hint_rect.centerx = self.screen_rect.centerx
        hint_rect.top = self.input_rect.bottom + 20
        self.screen.blit(hint_surf, hint_rect)

        chars_left = self.max_length - len(self.name)
        if chars_left > 0:
            chars_text = f"Осталось символов: {chars_left}"
            chars_surf = self.font_tiny.render(chars_text, True, (150, 150, 150))
            chars_rect = chars_surf.get_rect()
            chars_rect.centerx = self.screen_rect.centerx
            chars_rect.top = hint_rect.bottom + 10
            self.screen.blit(chars_surf, chars_rect)

    def is_active(self):
        """Возвращает, активно ли окно ввода."""
        return self.active