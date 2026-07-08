import pygame
import pygame.font


class Shop:

    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        self.active = False
        self.font = pygame.font.SysFont('Arial', 50, bold=True)
        self.font_small = pygame.font.SysFont('Arial', 32)
        self.font_tiny = pygame.font.SysFont('Arial', 24)

        self.text_color = (255, 255, 255)
        self.title_color = (255, 215, 0)
        self.button_color = (0, 150, 255)
        self.button_hover_color = (0, 200, 255)
        self.button_text_color = (255, 255, 255)

        self.bullet_speed_level = 0
        self.bullet_count_level = 0
        self.ship_skin = 0

        self.bullet_speed_price = 100
        self.bullet_count_price = 150
        self.ship_skin_price = 200

        self.max_bullet_speed = 3
        self.max_bullet_count = 2
        self.max_skins = 4

        self.error_message = ""
        self.error_timer = 0

        self._create_buttons()

    def _create_buttons(self):
        center_x = self.screen_rect.centerx
        start_y = self.screen_rect.centery + 20

        self.bullet_speed_button = ShopButton(
            self.screen, f"Скорость пуль +1", center_x, start_y,
            self.font_small, self.button_color, self.button_text_color
        )
        self.bullet_speed_button.price = self.bullet_speed_price

        self.bullet_count_button = ShopButton(
            self.screen, f"Пули +1 (веер)", center_x, start_y + 70,
            self.font_small, self.button_color, self.button_text_color
        )
        self.bullet_count_button.price = self.bullet_count_price

        self.ship_skin_button = ShopButton(
            self.screen, f"Скин корабля", center_x, start_y + 140,
            self.font_small, self.button_color, self.button_text_color
        )
        self.ship_skin_button.price = self.ship_skin_price

        self.exit_button = ShopButton(
            self.screen, "Выйти", center_x, self.screen_rect.bottom - 80,
            self.font_small, (200, 50, 50), self.button_text_color
        )

    def start(self):
        self.active = True
        self.error_message = ""
        self.error_timer = 0
        self.update_buttons()

    def close(self):
        self.active = False

    def show_error(self, message):
        self.error_message = message
        self.error_timer = 120

    def update_buttons(self):
        if self.bullet_speed_level >= self.max_bullet_speed:
            text = "Скорость пуль MAX"
            self.bullet_speed_button.text_surf = self.font_small.render(text, True, (100, 255, 100))
            self.bullet_speed_button.disabled = True
        else:
            text = f"Скорость пуль +1 ({self.bullet_speed_price} звёзд)"
            self.bullet_speed_button.text_surf = self.font_small.render(text, True, self.button_text_color)
            self.bullet_speed_button.disabled = False

        if self.bullet_count_level >= self.max_bullet_count:
            text = "Пули MAX (3)"
            self.bullet_count_button.text_surf = self.font_small.render(text, True, (100, 255, 100))
            self.bullet_count_button.disabled = True
        else:
            text = f"Пули +1 ({self.bullet_count_price} звёзд)"
            self.bullet_count_button.text_surf = self.font_small.render(text, True, self.button_text_color)
            self.bullet_count_button.disabled = False

        skins = ["Синий", "Красный", "Золотой", "Фиолетовый"]
        if self.ship_skin >= self.max_skins:
            text = "Все скины MAX"
            self.ship_skin_button.text_surf = self.font_small.render(text, True, (100, 255, 100))
            self.ship_skin_button.disabled = True
        else:
            next_skin_index = (self.ship_skin + 1) % self.max_skins
            text = f"Скин: {skins[self.ship_skin]} -> {skins[next_skin_index]} ({self.ship_skin_price} звёзд)"
            self.ship_skin_button.text_surf = self.font_small.render(text, True, self.button_text_color)
            self.ship_skin_button.disabled = False

        for button in [self.bullet_speed_button, self.bullet_count_button, self.ship_skin_button]:
            button.update_rect()

    def handle_click(self, mouse_pos):
        if not self.active:
            return False

        if self.exit_button.rect.collidepoint(mouse_pos):
            self.close()
            return True

        if self.bullet_speed_button.rect.collidepoint(mouse_pos) and not self.bullet_speed_button.disabled:
            if self.stats.total_score >= self.bullet_speed_price:
                self.stats.total_score -= self.bullet_speed_price
                self.bullet_speed_level += 1
                self.bullet_speed_price = int(self.bullet_speed_price * 1.5)
                self.settings.bullet_speed += 0.5
                self.update_buttons()
                self.ai_game.sb.prep_score()
                return True
            else:
                self.show_error("Недостаточно звёзд!")
                return False

        if self.bullet_count_button.rect.collidepoint(mouse_pos) and not self.bullet_count_button.disabled:
            if self.stats.total_score >= self.bullet_count_price:
                self.stats.total_score -= self.bullet_count_price
                self.bullet_count_level += 1
                self.bullet_count_price = int(self.bullet_count_price * 1.5)
                self.update_buttons()
                self.ai_game.sb.prep_score()
                return True
            else:
                self.show_error("Недостаточно звёзд!")
                return False

        if self.ship_skin_button.rect.collidepoint(mouse_pos) and not self.ship_skin_button.disabled:
            if self.stats.total_score >= self.ship_skin_price:
                self.stats.total_score -= self.ship_skin_price
                self.ship_skin += 1
                self.ship_skin_price = int(self.ship_skin_price * 1.5)
                self._apply_skin()
                self.update_buttons()
                self.ai_game.sb.prep_score()
                return True
            else:
                self.show_error("Недостаточно звёзд!")
                return False

        return False

    def _apply_skin(self):
        colors = [
            (0, 150, 255),    # Синий
            (255, 50, 50),    # Красный
            (255, 215, 0),    # Золотой
            (200, 50, 255),   # Фиолетовый
        ]
        skin_index = self.ship_skin % len(colors)
        color = colors[skin_index]
        self.ai_game.ship.change_color(color, skin_index + 1)

    def update(self):
        if self.error_timer > 0:
            self.error_timer -= 1
            if self.error_timer == 0:
                self.error_message = ""

    def draw(self):
        if not self.active:
            return

        overlay = pygame.Surface((self.screen_rect.width, self.screen_rect.height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        level_title = f"УРОВЕНЬ {self.stats.level} УСПЕШНО ПРОЙДЕН!"
        level_surf = self.font.render(level_title, True, (100, 255, 100))
        level_rect = level_surf.get_rect()
        level_rect.centerx = self.screen_rect.centerx
        level_rect.top = 30
        self.screen.blit(level_surf, level_rect)

        title_text = "МАГАЗИН"
        title_surf = self.font.render(title_text, True, self.title_color)
        title_rect = title_surf.get_rect()
        title_rect.centerx = self.screen_rect.centerx
        title_rect.top = level_rect.bottom + 10
        self.screen.blit(title_surf, title_rect)

        score_text = f"Звёзды: {self.stats.total_score}"
        score_surf = self.font_small.render(score_text, True, (255, 215, 0))
        score_rect = score_surf.get_rect()
        score_rect.centerx = self.screen_rect.centerx
        score_rect.top = title_rect.bottom + 15
        self.screen.blit(score_surf, score_rect)

        info_text = f"Скорость: {self.bullet_speed_level}  |  Пули: {self.bullet_count_level + 1}  |  Скин: {self.ship_skin + 1}"
        info_surf = self.font_tiny.render(info_text, True, (200, 200, 200))
        info_rect = info_surf.get_rect()
        info_rect.centerx = self.screen_rect.centerx
        info_rect.top = score_rect.bottom + 10
        self.screen.blit(info_surf, info_rect)

        if self.error_timer > 0:
            error_surf = self.font_small.render(self.error_message, True, (255, 50, 50))
            error_rect = error_surf.get_rect()
            error_rect.centerx = self.screen_rect.centerx
            error_rect.top = info_rect.bottom + 20
            self.screen.blit(error_surf, error_rect)

        self.bullet_speed_button.draw()
        self.bullet_count_button.draw()
        self.ship_skin_button.draw()
        self.exit_button.draw()

        hint_text = "Нажмите ESC или Выйти для продолжения"
        hint_surf = self.font_tiny.render(hint_text, True, (150, 150, 150))
        hint_rect = hint_surf.get_rect()
        hint_rect.centerx = self.screen_rect.centerx
        hint_rect.bottom = self.exit_button.rect.top - 15
        self.screen.blit(hint_surf, hint_rect)


class ShopButton:
    def __init__(self, screen, msg, x, y, font, color, text_color):
        self.screen = screen
        self.msg = msg
        self.x = x
        self.y = y
        self.font = font
        self.color = color
        self.text_color = text_color
        self.disabled = False
        self.price = 0

        self.text_surf = self.font.render(msg, True, text_color)
        self.update_rect()

    def update_rect(self):
        padding = 20
        self.rect = pygame.Rect(
            self.x - self.text_surf.get_width() // 2 - padding,
            self.y - self.text_surf.get_height() // 2 - padding // 2,
            self.text_surf.get_width() + padding * 2,
            self.text_surf.get_height() + padding
        )

    def draw(self):
        color = self.color
        if self.disabled:
            color = (80, 80, 80)
        elif self.rect.collidepoint(pygame.mouse.get_pos()):
            r = min(255, color[0] + 50)
            g = min(255, color[1] + 50)
            b = min(255, color[2] + 50)
            color = (r, g, b)

        pygame.draw.rect(self.screen, color, self.rect, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 2, border_radius=10)
        self.screen.blit(self.text_surf, self.text_surf.get_rect(center=self.rect.center))