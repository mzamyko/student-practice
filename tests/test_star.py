import pytest
import pygame
from unittest.mock import Mock
from star import Star


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
    ai_game.settings.screen_width = 800
    ai_game.settings.screen_height = 600
    return ai_game



def test_star_brightness_changes(mock_game):
    star = Star(mock_game)

    star.brightness = 150.0
    star.twinkle_speed = 2.0
    star.direction = 1

    star.update()

    assert star.brightness == 152.0


def test_star_reaches_max_brightness_limit(mock_game):
    star = Star(mock_game)

    star.brightness = 254.0
    star.twinkle_speed = 5.0
    star.direction = 1

    star.update()

    assert star.brightness == 255.0

    assert star.direction == -1


def test_star_reaches_min_brightness_limit(mock_game):
    star = Star(mock_game)

    star.brightness = 51.0
    star.twinkle_speed = 5.0
    star.direction = -1

    star.update()

    assert star.brightness == 50.0

    assert star.direction == 1
