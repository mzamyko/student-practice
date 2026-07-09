import pytest
import pygame
from unittest.mock import Mock
from ship import Ship


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
    ai_game.settings.ship_speed = 2.0
    return ai_game


def test_ship_movement_right(mock_game):
    ship = Ship(mock_game)
    ship.rect.x = 100
    ship.x = 100.0

    ship.moving_right = True
    ship.update()

    assert ship.x == 102.0
    assert ship.rect.x == 102


def test_ship_movement_left(mock_game):
    ship = Ship(mock_game)
    ship.rect.x = 100
    ship.x = 100.0

    ship.moving_left = True
    ship.update()

    assert ship.x == 98.0
    assert ship.rect.x == 98


def test_ship_cannot_move_past_right_edge(mock_game):
    ship = Ship(mock_game)

    ship.rect.right = 800
    ship.x = float(ship.rect.x)

    ship.moving_right = True
    ship.update()

    assert ship.rect.right == 800


def test_ship_cannot_move_past_left_edge(mock_game):
    ship = Ship(mock_game)

    ship.rect.left = 0
    ship.x = float(ship.rect.x)

    ship.moving_left = True
    ship.update()

    assert ship.rect.left == 0



def test_center_ship(mock_game):
    ship = Ship(mock_game)

    ship.rect.x = 50
    ship.rect.y = 50

    ship.center_ship()

    assert ship.rect.midbottom == mock_game.screen.get_rect().midbottom
    assert ship.x == float(ship.rect.x)
