import pytest
import pygame
from unittest.mock import Mock
from alien_bullet import AlienBullet


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
    return ai_game


def test_bullet_moves_down(mock_game):
    bullet = AlienBullet(mock_game, x=400, y=100)

    initial_y = bullet.rect.y
    bullet.update()

    assert bullet.rect.y == initial_y + bullet.speed


def test_bullet_removes_itself_when_off_screen(mock_game):
    bullet = AlienBullet(mock_game, x=400, y=599)

    test_group = pygame.sprite.Group()
    test_group.add(bullet)

    bullet.update()

    assert bullet not in test_group
