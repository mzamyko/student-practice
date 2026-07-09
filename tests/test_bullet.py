import pytest
import pygame
from unittest.mock import Mock
from bullet import Bullet


@pytest.fixture(scope="session", autouse=True)
def init_pygame():
    pygame.init()
    pygame.display.set_mode((1, 1), pygame.NOFRAME)
    yield
    pygame.quit()


@pytest.fixture
def mock_game():
    ai_game = Mock()
    ai_game.screen = pygame.Surface((800, 600))

    ai_game.settings = Mock()
    ai_game.settings.bullet_color = (100, 0, 0)
    ai_game.settings.bullet_width = 3
    ai_game.settings.bullet_height = 15
    ai_game.settings.bullet_speed = 5.0

    ai_game.ship = Mock()
    ai_game.ship.rect = pygame.Rect(400, 500, 50, 50)

    return ai_game


def test_bullet_straight_flight(mock_game):
    bullet = Bullet(mock_game, angle_offset=0)

    assert bullet.speed_x == 0
    assert bullet.speed_y == -5.0

    initial_x = bullet.x
    initial_y = bullet.y

    bullet.update()

    assert bullet.rect.x == int(initial_x)
    assert bullet.rect.y == int(initial_y - 5.0)


def test_bullet_angled_flight(mock_game):
    bullet = Bullet(mock_game, angle_offset=90)

    assert pytest.approx(bullet.speed_x) == 5.0
    assert pytest.approx(bullet.speed_y) == 0.0

    initial_x = bullet.x
    bullet.update()

    assert bullet.rect.x > initial_x
