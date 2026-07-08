import sys
from time import sleep
import random

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from alien_bullet import AlienBullet
from star import Star
from menu import Menu
from sound_manager import SoundManager
from intro_animation import IntroAnimation
from victory_animation import VictoryAnimation
from high_scores import HighScores
from name_input import NameInput
from shop import Shop
from victory_celebration import VictoryCelebration


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры."""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.sound_manager = SoundManager()

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()

        self.death_effects = pygame.sprite.Group()

        self.high_scores = HighScores()
        self.name_input = NameInput(self)
        self.shop = Shop(self)
        self.victory_celebration = VictoryCelebration(self)

        self._create_fleet()
        self._create_stars()

        self.menu = Menu(self)
        self.intro_animation = IntroAnimation(self)
        self.victory_animation = VictoryAnimation(self)

        self.stats.game_active = False
        self.showing_menu = True
        self.showing_intro = False
        self.showing_victory = False
        self.showing_game_over = False
        self.waiting_for_name = False
        self.showing_shop = False
        self.showing_celebration = False

        self.play_button = Button(self, "Play")

    def _create_stars(self):
        for _ in range(self.settings.star_count):
            star = Star(self)
            self.stars.add(star)

    def run_game(self):
        while True:
            self._check_events()

            if self.showing_celebration:
                self.victory_celebration.update()
                if self.victory_celebration.is_finished():
                    self.showing_celebration = False
                    self.waiting_for_name = True
                    self.name_input.start()
                self._update_screen()
                continue

            if self.waiting_for_name:
                self.name_input.update()
                self._update_screen()
                continue

            if self.showing_shop:
                self.shop.update()
                self._update_screen()
                continue

            if self.showing_victory:
                self.victory_animation.update()
                if self.victory_animation.is_finished():
                    self.showing_victory = False
                    self.waiting_for_name = True
                    self.name_input.start()
                    pygame.mouse.set_visible(True)
            elif self.showing_intro:
                self.intro_animation.update()
                if self.intro_animation.is_finished():
                    self.showing_intro = False
                    self._start_game_after_intro()
            elif self.stats.game_active and not self.showing_menu:
                self.ship.update()
                self._update_bullets()
                self._update_alien_bullets()
                self._update_aliens()
                self.stars.update()
                self._update_death_effects()
                self.sb.prep_level_score()

            self._update_screen()

    def _start_game_after_intro(self):
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        self.aliens.empty()
        self.bullets.empty()
        self.alien_bullets.empty()
        self.death_effects.empty()

        self._create_fleet()
        self.ship.center_ship()
        pygame.mouse.set_visible(False)

    def _update_death_effects(self):
        for effect in self.death_effects.copy():
            effect.update()
            if effect.is_finished():
                self.death_effects.remove(effect)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if self.showing_celebration:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.showing_celebration = False
                    self.waiting_for_name = True
                    self.name_input.start()
                    pygame.mouse.set_visible(True)
                continue

            if self.waiting_for_name:
                if self.name_input.handle_event(event):
                    name = self.name_input.get_name()
                    final_score = self.stats.get_final_score()
                    self.high_scores.add_score(
                        name,
                        final_score,
                        self.stats.level,
                        self.stats.bullets_fired
                    )
                    self.waiting_for_name = False
                    self.showing_menu = True
                    self.menu.current_menu = 'main'
                    pygame.mouse.set_visible(True)
                continue

            if self.showing_shop:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.showing_shop = False
                        self.shop.close()
                        self.stats.game_active = True
                        self.stats.level += 1
                        self.settings.increase_speed()
                        self.sb.prep_level()
                        self.sb.prep_level_score()
                        self._create_fleet()
                        pygame.mouse.set_visible(False)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self.shop.handle_click(mouse_pos)
                    if not self.shop.active:
                        self.showing_shop = False
                        self.stats.game_active = True
                        self.stats.level += 1
                        self.settings.increase_speed()
                        self.sb.prep_level()
                        self.sb.prep_level_score()
                        self._create_fleet()
                        pygame.mouse.set_visible(False)
                continue

            if event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.showing_menu:
                    action = self.menu.check_click(mouse_pos)
                    if action == 'play':
                        self.showing_menu = False
                        self.showing_intro = True
                        self.intro_animation.start()
                    elif action == 'main':
                        self.showing_menu = True
                        self.menu.current_menu = 'main'
                elif not self.stats.game_active and not self.showing_victory and not self.showing_game_over:
                    self._check_play_button(mouse_pos)
                elif self.showing_game_over:
                    self.showing_game_over = False
                    self.showing_menu = True
                    self.menu.current_menu = 'main'
                    pygame.mouse.set_visible(True)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.menu.dragging_shoot = False
                self.menu.dragging_hit = False
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                if self.showing_menu:
                    if self.menu.current_menu == 'volume':
                        if self.menu.dragging_shoot:
                            self.menu.update_shoot_volume(mouse_pos)
                        elif self.menu.dragging_hit:
                            self.menu.update_hit_volume(mouse_pos)
                    else:
                        if self.menu.current_menu == 'main':
                            self.menu.play_button.check_hover(mouse_pos)
                            self.menu.rules_button.check_hover(mouse_pos)
                            self.menu.scores_button.check_hover(mouse_pos)
                            self.menu.volume_button.check_hover(mouse_pos)
                        elif self.menu.current_menu in ['rules', 'shop', 'volume', 'scores']:
                            self.menu.back_button.check_hover(mouse_pos)
                            if self.menu.current_menu == 'scores':
                                self.menu.clear_button.check_hover(mouse_pos)

    def _start_game(self):
        self.showing_menu = False
        self.showing_intro = True
        self.intro_animation.start()

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.showing_menu = False
            self.showing_intro = True
            self.intro_animation.start()

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE and self.stats.game_active:
            self._fire_bullet()
        elif event.key == pygame.K_ESCAPE:
            if self.stats.game_active:
                self.stats.game_active = False
                self.showing_menu = True
                self.menu.current_menu = 'main'
                pygame.mouse.set_visible(True)
            elif self.showing_intro:
                self.showing_intro = False
                self._start_game_after_intro()
            elif self.showing_victory:
                self.showing_victory = False
                self.showing_menu = True
                self.menu.current_menu = 'main'
            elif self.showing_game_over:
                self.showing_game_over = False
                self.showing_menu = True
                self.menu.current_menu = 'main'
                pygame.mouse.set_visible(True)

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Создание нескольких пуль с веерным разлетом (максимум 3)."""
        if len(self.bullets) < self.settings.bullets_allowed:
            bullet_count = min(self.shop.bullet_count_level + 1, 3)

            if bullet_count == 1:
                new_bullet = Bullet(self, 0)
                self.bullets.add(new_bullet)
            else:
                if bullet_count == 2:
                    angles = [-10, 10]
                else:
                    angles = [-15, 0, 15]

                for angle in angles:
                    new_bullet = Bullet(self, angle)
                    self.bullets.add(new_bullet)

            self.sound_manager.play_shoot()
            self.stats.add_bullet()

    def _update_bullets(self):
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _update_alien_bullets(self):
        self.alien_bullets.update()

        for bullet in self.alien_bullets.copy():
            if bullet.rect.bottom > self.screen.get_rect().bottom:
                self.alien_bullets.remove(bullet)

        if pygame.sprite.spritecollideany(self.ship, self.alien_bullets):
            for bullet in self.alien_bullets.copy():
                self.alien_bullets.remove(bullet)
            self._ship_hit()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                for alien in aliens:
                    self._create_death_effect(alien.rect.centerx, alien.rect.centery)
                    self.sound_manager.play_hit()

                    if alien.alien_type == 'pink':
                        self.stats.add_score(self.settings.pink_alien_points)
                        self._pink_explosion(alien.rect.centerx, alien.rect.centery)
                    else:
                        self.stats.add_score(self.settings.alien_points)

                self.sb.prep_score()
                self.sb.prep_level_score()
                self.sb.check_high_score()

        if not self.aliens:
            self.bullets.empty()
            self.alien_bullets.empty()

            if self.stats.level >= self.settings.max_level:
                self.stats.complete_level()
                self.stats.game_active = False
                self.showing_victory = False
                self.showing_celebration = True
                self.victory_celebration.start()
                pygame.mouse.set_visible(True)
            else:
                self.stats.complete_level()
                self.stats.game_active = False
                self.showing_shop = True
                self.shop.start()
                pygame.mouse.set_visible(True)

    def _pink_explosion(self, x, y):
        for i in range(15):
            self._create_death_effect(
                x + random.randint(-120, 120),
                y + random.randint(-120, 120)
            )

        radius = 150
        aliens_to_kill = []

        for alien in self.aliens:
            dx = alien.rect.centerx - x
            dy = alien.rect.centery - y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance < radius:
                aliens_to_kill.append(alien)

        for alien in aliens_to_kill:
            self._create_death_effect(alien.rect.centerx, alien.rect.centery)
            self.sound_manager.play_hit()

            if alien.alien_type == 'pink':
                self._pink_explosion_chain(alien.rect.centerx, alien.rect.centery, depth=1)
            else:
                self.stats.add_score(self.settings.alien_points)

            self.aliens.remove(alien)

        self.sb.prep_score()
        self.sb.prep_level_score()
        self.sb.check_high_score()

        if not self.aliens:
            self.bullets.empty()
            self.alien_bullets.empty()
            if self.stats.level >= self.settings.max_level:
                self.stats.complete_level()
                self.stats.game_active = False
                self.showing_victory = False
                self.showing_celebration = True
                self.victory_celebration.start()
                pygame.mouse.set_visible(True)
            else:
                self.stats.complete_level()
                self.stats.game_active = False
                self.showing_shop = True
                self.shop.start()
                pygame.mouse.set_visible(True)

    def _pink_explosion_chain(self, x, y, depth=0):
        if depth > 3:
            return

        radius = 120
        aliens_to_kill = []

        for alien in self.aliens:
            dx = alien.rect.centerx - x
            dy = alien.rect.centery - y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance < radius:
                aliens_to_kill.append(alien)

        for alien in aliens_to_kill:
            self._create_death_effect(alien.rect.centerx, alien.rect.centery)
            self.sound_manager.play_hit()

            if alien.alien_type == 'pink':
                self._pink_explosion_chain(alien.rect.centerx, alien.rect.centery, depth + 1)
            else:
                self.stats.add_score(self.settings.alien_points)

            self.aliens.remove(alien)

        self.sb.prep_score()
        self.sb.prep_level_score()
        self.sb.check_high_score()

    def _create_death_effect(self, x, y):
        effect = DeathEffect(x, y)
        self.death_effects.add(effect)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        for alien in self.aliens:
            if alien.alien_type == 'yellow' and alien.should_shoot():
                alien_bullet = AlienBullet(self, alien.rect.centerx, alien.rect.bottom)
                self.alien_bullets.add(alien_bullet)

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            self.stats.reset_level_stats()
            self.sb.prep_level_score()

            self.aliens.empty()
            self.bullets.empty()
            self.alien_bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.stats.game_active = False
            self.showing_game_over = True
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        alien = Alien(self, 'green')
        alien_width, alien_height = alien.rect.size

        number_rows = 3
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (3 * alien_width)
        start_y = 30

        current_level = self.stats.level

        if current_level == 1:
            available_types = ['green']
        elif current_level == 2:
            available_types = ['green', 'pink']
        elif current_level == 3:
            available_types = ['green', 'pink', 'yellow']
        elif current_level >= 4:
            available_types = ['green', 'pink', 'yellow', 'blue']
        else:
            available_types = ['green']

        yellow_count = 0
        max_yellow = 4

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                alien_type = random.choice(available_types)

                if alien_type == 'yellow':
                    if yellow_count >= max_yellow:
                        alien_type = 'green'
                    else:
                        yellow_count += 1

                self._create_alien(alien_number, row_number, alien_type, start_y)

    def _create_alien(self, alien_number, row_number, alien_type='green', start_y=30):
        alien = Alien(self, alien_type)
        alien_width, alien_height = alien.rect.size

        alien.x = alien_width + 3 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 3 * alien.rect.height * row_number + start_y
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        if self.showing_celebration:
            self.victory_celebration.draw()
            pygame.display.flip()
            return

        if self.waiting_for_name:
            self.screen.fill(self.settings.bg_color)
            self.stars.draw(self.screen)
            self.name_input.draw()
            pygame.display.flip()
            return

        if self.showing_shop:
            self.screen.fill(self.settings.bg_color)
            self.stars.draw(self.screen)
            self.shop.draw()
            pygame.display.flip()
            return

        if self.showing_victory:
            self.victory_animation.draw()
        elif self.showing_intro:
            self.intro_animation.draw()
        elif self.showing_menu:
            self.screen.fill(self.settings.bg_color)
            self.stars.draw(self.screen)
            self.menu.draw()
        elif self.showing_game_over:
            self.screen.fill((0, 0, 0))

            screen_rect = self.screen.get_rect()

            font_big = pygame.font.SysFont('Arial', 100, bold=True)
            font_small = pygame.font.SysFont('Arial', 40)

            game_over_text = "GAME OVER"
            game_over_surf = font_big.render(game_over_text, True, (255, 50, 50))
            game_over_rect = game_over_surf.get_rect()
            game_over_rect.centerx = screen_rect.centerx
            game_over_rect.centery = screen_rect.centery - 80

            shadow_surf = font_big.render(game_over_text, True, (100, 0, 0))
            shadow_rect = shadow_surf.get_rect()
            shadow_rect.centerx = screen_rect.centerx + 4
            shadow_rect.centery = screen_rect.centery - 76

            self.screen.blit(shadow_surf, shadow_rect)
            self.screen.blit(game_over_surf, game_over_rect)

            info_text = f"Уровень {self.stats.level}  |  Счёт: {self.stats.total_score}"
            info_surf = font_small.render(info_text, True, (255, 255, 255))
            info_rect = info_surf.get_rect()
            info_rect.centerx = screen_rect.centerx
            info_rect.top = game_over_rect.bottom + 30
            self.screen.blit(info_surf, info_rect)

            hint_text = "Нажмите ESC или кликните для возврата в меню"
            hint_surf = font_small.render(hint_text, True, (150, 150, 150))
            hint_rect = hint_surf.get_rect()
            hint_rect.centerx = screen_rect.centerx
            hint_rect.top = info_rect.bottom + 30
            self.screen.blit(hint_surf, hint_rect)

            high_score_text = f"Рекорд: {self.stats.high_score}"
            high_score_surf = font_small.render(high_score_text, True, (255, 215, 0))
            high_score_rect = high_score_surf.get_rect()
            high_score_rect.centerx = screen_rect.centerx
            high_score_rect.top = hint_rect.bottom + 20
            self.screen.blit(high_score_surf, high_score_rect)
        else:
            self.screen.fill(self.settings.bg_color)
            self.stars.draw(self.screen)
            self.ship.blitme()

            for bullet in self.bullets.sprites():
                bullet.draw_bullet()

            for bullet in self.alien_bullets.sprites():
                bullet.draw_bullet()

            self.aliens.draw(self.screen)
            self.death_effects.draw(self.screen)
            self.sb.show_score()

            if not self.stats.game_active:
                self.play_button.draw_button()

        pygame.display.flip()


class DeathEffect(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.size = 3
        self.max_size = 40
        self.image = pygame.Surface((self.max_size * 2, self.max_size * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.color = (50, 255, 80)
        self.life = 50
        self.max_life = 50
        self.finished = False
        self.update_surface()

    def update_surface(self):
        self.image.fill((0, 0, 0, 0))
        progress = 1 - (self.life / self.max_life)
        current_size = self.size + (self.max_size - self.size) * progress
        pygame.draw.circle(self.image, self.color, (self.max_size, self.max_size), int(current_size))

        for i in range(6):
            angle = i * 60 + progress * 40
            distance = current_size * (0.5 + progress * 0.8)
            dx = int(distance * pygame.math.Vector2(1, 0).rotate(angle)[0])
            dy = int(distance * pygame.math.Vector2(1, 0).rotate(angle)[1])
            splash_size = int(current_size * (0.4 - progress * 0.2))
            if splash_size > 2:
                pygame.draw.circle(self.image, (self.color[0], self.color[1], self.color[2]),
                                   (self.max_size + dx, self.max_size + dy), splash_size)

        glow_color = (self.color[0], self.color[1], self.color[2], 40)
        for i in range(4):
            glow_size = current_size + i * 6
            pygame.draw.circle(self.image, glow_color, (self.max_size, self.max_size), int(glow_size), 2)

    def update(self):
        self.life -= 1
        if self.life <= 0:
            self.finished = True
        else:
            self.update_surface()

    def is_finished(self):
        return self.finished


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()