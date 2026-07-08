import pygame
import pygame.font


class HighScoresDisplay:

    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.high_scores = ai_game.high_scores

        self.font = pygame.font.SysFont('Arial', 40, bold=True)
        self.font_small = pygame.font.SysFont('Arial', 30)

        self.active = False

    def show(self):
        self.active = True

    def hide(self):
        self.active = False

    def draw(self):
        if not self.active:
            return

        overlay = pygame.Surface((self.screen_rect.width, self.screen_rect.height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        title_text = "ТАБЛИЦА РЕКОРДОВ"
        title_surf = self.font.render(title_text, True, (255, 215, 0))
        title_rect = title_surf.get_rect()
        title_rect.centerx = self.screen_rect.centerx
        title_rect.top = 50
        self.screen.blit(title_surf, title_rect)

        scores = self.high_scores.get_scores()

        if not scores:
            empty_text = "Нет рекордов. Станьте первым!"
            empty_surf = self.font_small.render(empty_text, True, (200, 200, 200))
            empty_rect = empty_surf.get_rect()
            empty_rect.centerx = self.screen_rect.centerx
            empty_rect.centery = self.screen_rect.centery
            self.screen.blit(empty_surf, empty_rect)
        else:
            headers = ["#", "Имя", "Рейтинг", "Уровень", "Пули"]
            header_x = [80, 200, 450, 700, 900]

            for i, header in enumerate(headers):
                header_surf = self.font_small.render(header, True, (255, 255, 100))
                header_rect = header_surf.get_rect()
                header_rect.left = header_x[i]
                header_rect.top = 140
                self.screen.blit(header_surf, header_rect)

            pygame.draw.line(self.screen, (100, 100, 100),
                             (50, 180), (self.screen_rect.width - 50, 180), 2)

            y_offset = 200
            for i, score in enumerate(scores[:10]):
                color = (255, 215, 0) if i == 0 else (255, 255, 255)

                row_data = [
                    str(i + 1),
                    score['name'][:12],
                    str(score['score']),
                    str(score['level']),
                    str(score['bullets_used'])
                ]

                for j, data in enumerate(row_data):
                    data_surf = self.font_small.render(data, True, color)
                    data_rect = data_surf.get_rect()
                    data_rect.left = header_x[j]
                    data_rect.top = y_offset
                    self.screen.blit(data_surf, data_rect)

                y_offset += 45

        close_text = "Нажмите ESC для выхода"
        close_surf = self.font_small.render(close_text, True, (150, 150, 150))
        close_rect = close_surf.get_rect()
        close_rect.centerx = self.screen_rect.centerx
        close_rect.bottom = self.screen_rect.bottom - 30
        self.screen.blit(close_surf, close_rect)