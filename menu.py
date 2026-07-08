import pygame
import pygame.font


class Menu:

    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.sound_manager = ai_game.sound_manager

        self.title_font = pygame.font.SysFont('Arial', 90, bold=True)
        self.font = pygame.font.SysFont('Arial', 48)
        self.small_font = pygame.font.SysFont('Arial', 30)
        self.tiny_font = pygame.font.SysFont('Arial', 22)

        self.title_color = (255, 215, 0)
        self.text_color = (255, 255, 255)
        self.button_color = (0, 150, 255)
        self.button_text_color = (255, 255, 255)

        self._create_buttons()

        self.current_menu = 'main'
        self.dragging_shoot = False
        self.dragging_hit = False
        self.shoot_slider_rect = None
        self.hit_slider_rect = None

    def _create_buttons(self):
        center_x = self.screen_rect.centerx
        start_y = self.screen_rect.centery - 80

        self.play_button = MenuButton(
            self.screen, "Играть", center_x, start_y,
            self.font, self.button_color, self.button_text_color
        )

        self.rules_button = MenuButton(
            self.screen, "Правила", center_x, start_y + 80,
            self.font, self.button_color, self.button_text_color
        )

        self.scores_button = MenuButton(
            self.screen, "Рекорды", center_x, start_y + 160,
            self.font, self.button_color, self.button_text_color
        )

        self.volume_button = MenuButton(
            self.screen, "Громкость", center_x, start_y + 240,
            self.font, self.button_color, self.button_text_color
        )

        self.back_button = MenuButton(
            self.screen, "Назад", center_x, self.screen_rect.bottom - 80,
            self.small_font, (200, 50, 50), self.button_text_color
        )

        self.clear_button = MenuButton(
            self.screen, "🗑 Удалить все",
            self.screen_rect.centerx, self.screen_rect.bottom - 140,
            self.small_font, (200, 50, 50), (255, 255, 255)
        )

    def draw_title(self):
        title_text = "ALIEN SKY"
        title_surf = self.title_font.render(title_text, True, self.title_color)
        title_rect = title_surf.get_rect()
        title_rect.centerx = self.screen_rect.centerx
        title_rect.top = 80

        shadow_surf = self.title_font.render(title_text, True, (100, 100, 50))
        shadow_rect = shadow_surf.get_rect()
        shadow_rect.centerx = self.screen_rect.centerx + 4
        shadow_rect.top = 84

        self.screen.blit(shadow_surf, shadow_rect)
        self.screen.blit(title_surf, title_rect)

    def draw_main_menu(self):
        self.draw_title()
        self.play_button.draw()
        self.rules_button.draw()
        self.scores_button.draw()
        self.volume_button.draw()

        version_text = "v1.0"
        version_surf = self.small_font.render(version_text, True, (100, 100, 100))
        version_rect = version_surf.get_rect()
        version_rect.bottomright = self.screen_rect.bottomright
        version_rect.x -= 20
        version_rect.y -= 20
        self.screen.blit(version_surf, version_rect)

    def draw_rules(self):
        title_surf = self.font.render("Правила игры", True, self.title_color)
        title_rect = title_surf.get_rect()
        title_rect.centerx = self.screen_rect.centerx
        title_rect.top = 50
        self.screen.blit(title_surf, title_rect)

        rules = [
            "1. Управляйте кораблём с помощью стрелок ← →",
            "2. Стреляйте по пришельцам клавишей ПРОБЕЛ",
            "3. Уничтожайте всех пришельцев для перехода на новый уровень",
            "4. Не дайте пришельцам коснуться вашего корабля",
            "5. У вас есть 3 жизни (красные сердечки)",
            "6. За каждого пришельца вы получаете очки",
            "7. С каждым уровнем игра становится быстрее",
            "8. Розовые пришельцы взрываются цепной реакцией",
            "9. Жёлтые пришельцы стреляют (очень редко)",
            "10. Голубые пришельцы меняют размер",
            "",
            "Удачи, капитан! "
        ]

        y_offset = 150
        for line in rules:
            if line == "":
                y_offset += 30
                continue
            text_surf = self.small_font.render(line, True, self.text_color)
            text_rect = text_surf.get_rect()
            text_rect.centerx = self.screen_rect.centerx
            text_rect.top = y_offset
            self.screen.blit(text_surf, text_rect)
            y_offset += 45

        self.back_button.draw()

    def draw_shop(self):
        title_surf = self.font.render("Магазин", True, self.title_color)
        title_rect = title_surf.get_rect()
        title_rect.centerx = self.screen_rect.centerx
        title_rect.top = 50
        self.screen.blit(title_surf, title_rect)

        shop_texts = [
            "Здесь будут улучшения для вашего корабля!",
            " Очки: " + str(self.stats.total_score),
            "",
            "Доступные улучшения:",
            " Скорость корабля - 100 очков",
            " Скорость пуль - 150 очков",
            " Дополнительная жизнь - 200 очков",
            " Больше пуль - 250 очков"
        ]

        y_offset = 150
        for line in shop_texts:
            if line == "":
                y_offset += 20
                continue
            color = self.text_color
            if "💰" in line:
                color = (255, 215, 0)
            text_surf = self.small_font.render(line, True, color)
            text_rect = text_surf.get_rect()
            text_rect.centerx = self.screen_rect.centerx
            text_rect.top = y_offset
            self.screen.blit(text_surf, text_rect)
            y_offset += 40

        self.back_button.draw()

    def draw_volume_slider(self, x, y, width, height, value, label, color=(0, 200, 0)):
        label_surf = self.small_font.render(label, True, self.text_color)
        label_rect = label_surf.get_rect()
        label_rect.left = x
        label_rect.centery = y - 30
        self.screen.blit(label_surf, label_rect)

        value_text = str(int(value * 100)) + "%"
        value_surf = self.small_font.render(value_text, True, self.title_color)
        value_rect = value_surf.get_rect()
        value_rect.right = x + width
        value_rect.centery = y - 30
        self.screen.blit(value_surf, value_rect)

        pygame.draw.rect(self.screen, (50, 50, 50), (x, y, width, height))
        pygame.draw.rect(self.screen, (80, 80, 80), (x, y, width, height), 2)

        fill_width = int(width * value)
        pygame.draw.rect(self.screen, color, (x, y, fill_width, height))

        handle_x = x + fill_width
        handle_radius = 12
        pygame.draw.circle(self.screen, (255, 255, 255), (handle_x, y + height // 2), handle_radius)
        pygame.draw.circle(self.screen, (200, 200, 200), (handle_x, y + height // 2), handle_radius, 2)

        return pygame.Rect(x - 10, y - 20, width + 20, height + 40)

    def draw_volume(self):
        title_surf = self.font.render("Настройки громкости", True, self.title_color)
        title_rect = title_surf.get_rect()
        title_rect.centerx = self.screen_rect.centerx
        title_rect.top = 50
        self.screen.blit(title_surf, title_rect)

        slider_width = 400
        slider_height = 16
        slider_x = self.screen_rect.centerx - slider_width // 2
        slider_y = 220

        shoot_vol = self.sound_manager.get_shoot_volume()
        hit_vol = self.sound_manager.get_hit_volume()

        self.shoot_slider_rect = self.draw_volume_slider(
            slider_x, slider_y, slider_width, slider_height,
            shoot_vol, " Выстрелы", (0, 150, 255)
        )

        slider_y2 = 320
        self.hit_slider_rect = self.draw_volume_slider(
            slider_x, slider_y2, slider_width, slider_height,
            hit_vol, " Взрывы", (255, 100, 50)
        )

        control_text = "Перетаскивайте ползунки мышью для изменения громкости"
        control_surf = self.tiny_font.render(control_text, True, (150, 150, 150))
        control_rect = control_surf.get_rect()
        control_rect.centerx = self.screen_rect.centerx
        control_rect.top = 400
        self.screen.blit(control_surf, control_rect)

        self.back_button.draw()

    def draw_scores(self):
        title_surf = self.font.render("Таблица рекордов", True, self.title_color)
        title_rect = title_surf.get_rect()
        title_rect.centerx = self.screen_rect.centerx
        title_rect.top = 50
        self.screen.blit(title_surf, title_rect)

        scores = self.ai_game.high_scores.get_scores()

        if not scores:
            empty_text = "Нет рекордов. Станьте первым!"
            empty_surf = self.small_font.render(empty_text, True, (200, 200, 200))
            empty_rect = empty_surf.get_rect()
            empty_rect.centerx = self.screen_rect.centerx
            empty_rect.centery = self.screen_rect.centery
            self.screen.blit(empty_surf, empty_rect)
        else:
            headers = ["#", "Имя", "Счёт", "Уровень", "Пули"]
            header_x = [80, 200, 500, 700, 900]

            for i, header in enumerate(headers):
                header_surf = self.small_font.render(header, True, (255, 255, 100))
                header_rect = header_surf.get_rect()
                header_rect.left = header_x[i]
                header_rect.top = 140
                self.screen.blit(header_surf, header_rect)

            pygame.draw.line(self.screen, (100, 100, 100),
                             (50, 180), (self.screen_rect.width - 50, 180), 2)

            y_offset = 200
            for i, score in enumerate(scores[:10]):
                if i == 0:
                    color = (255, 215, 0)
                elif i == 1:
                    color = (192, 192, 192)
                elif i == 2:
                    color = (205, 127, 50)
                else:
                    color = (255, 255, 255)

                row_data = [
                    str(i + 1),
                    score['name'][:12],
                    str(score['score']),
                    str(score['level']),
                    str(score['bullets_used'])
                ]

                for j, data in enumerate(row_data):
                    data_surf = self.small_font.render(data, True, color)
                    data_rect = data_surf.get_rect()
                    data_rect.left = header_x[j]
                    data_rect.top = y_offset
                    self.screen.blit(data_surf, data_rect)

                y_offset += 45

        self.clear_button.draw()
        self.back_button.draw()

    def check_volume_click(self, mouse_pos):
        if self.shoot_slider_rect and self.shoot_slider_rect.collidepoint(mouse_pos):
            self.dragging_shoot = True
            self.update_shoot_volume(mouse_pos)
            return True
        elif self.hit_slider_rect and self.hit_slider_rect.collidepoint(mouse_pos):
            self.dragging_hit = True
            self.update_hit_volume(mouse_pos)
            return True
        return False

    def update_shoot_volume(self, mouse_pos):
        if self.shoot_slider_rect:
            x = mouse_pos[0]
            slider_x = self.shoot_slider_rect.left + 10
            slider_width = self.shoot_slider_rect.width - 20
            if slider_width > 0:
                volume = (x - slider_x) / slider_width
                volume = max(0, min(1, volume))
                self.sound_manager.set_shoot_volume(volume)

    def update_hit_volume(self, mouse_pos):
        if self.hit_slider_rect:
            x = mouse_pos[0]
            slider_x = self.hit_slider_rect.left + 10
            slider_width = self.hit_slider_rect.width - 20
            if slider_width > 0:
                volume = (x - slider_x) / slider_width
                volume = max(0, min(1, volume))
                self.sound_manager.set_hit_volume(volume)

    def check_click(self, mouse_pos):
        if self.current_menu == 'main':
            if self.play_button.rect.collidepoint(mouse_pos):
                return 'play'
            elif self.rules_button.rect.collidepoint(mouse_pos):
                self.current_menu = 'rules'
                return 'rules'
            elif self.scores_button.rect.collidepoint(mouse_pos):
                self.current_menu = 'scores'
                return 'scores'
            elif self.volume_button.rect.collidepoint(mouse_pos):
                self.current_menu = 'volume'
                return 'volume'

        elif self.current_menu == 'volume':
            if self.check_volume_click(mouse_pos):
                return 'volume'
            elif self.back_button.rect.collidepoint(mouse_pos):
                self.current_menu = 'main'
                return 'main'

        elif self.current_menu == 'rules':
            if self.back_button.rect.collidepoint(mouse_pos):
                self.current_menu = 'main'
                return 'main'

        elif self.current_menu == 'shop':
            if self.back_button.rect.collidepoint(mouse_pos):
                self.current_menu = 'main'
                return 'main'

        elif self.current_menu == 'scores':
            if self.clear_button.rect.collidepoint(mouse_pos):
                self.ai_game.high_scores.clear_scores()
                return 'scores'
            elif self.back_button.rect.collidepoint(mouse_pos):
                self.current_menu = 'main'
                return 'main'

        return None

    def draw(self):
        if self.current_menu == 'main':
            self.draw_main_menu()
        elif self.current_menu == 'rules':
            self.draw_rules()
        elif self.current_menu == 'shop':
            self.draw_shop()
        elif self.current_menu == 'volume':
            self.draw_volume()
        elif self.current_menu == 'scores':
            self.draw_scores()


class MenuButton:
    def __init__(self, screen, msg, x, y, font, color, text_color):
        self.screen = screen
        self.msg = msg
        self.x = x
        self.y = y
        self.font = font
        self.color = color
        self.text_color = text_color

        self.text_surf = self.font.render(msg, True, text_color)
        self.text_rect = self.text_surf.get_rect()
        self.text_rect.center = (x, y)

        padding = 20
        self.rect = pygame.Rect(
            x - self.text_rect.width // 2 - padding,
            y - self.text_rect.height // 2 - padding // 2,
            self.text_rect.width + padding * 2,
            self.text_rect.height + padding
        )

        self.hovered = False

    def draw(self):
        color = self.color
        if self.hovered:
            r = min(255, color[0] + 50)
            g = min(255, color[1] + 50)
            b = min(255, color[2] + 50)
            color = (r, g, b)

        pygame.draw.rect(self.screen, color, self.rect, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 2, border_radius=10)
        self.screen.blit(self.text_surf, self.text_rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
        return self.hovered