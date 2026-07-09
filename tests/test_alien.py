import pytest
import pygame
from unittest.mock import Mock
from alien import Alien


@pytest.fixture(scope="session", autouse=True)
def init_pygame():
    pygame.init()
    pygame.display.set_mode((1, 1), pygame.NOFRAME)
    yield
    pygame.quit()
@pytest.fixture
def mock_alien():
    ai_game = Mock()
    ai_game.screen = pygame.Surface((800, 600))
    ai_game.settings = Mock()

    alien = Alien(ai_game, alien_type='yellow')
    alien.rect = pygame.Rect(0, 0, 50, 50)
    return alien

def test_only_yellow_aliens_can_shoot(mock_alien):
    mock_alien.alien_type = 'green'
    mock_alien.shoot_timer = 100
    mock_alien.shoot_delay = 100

    assert mock_alien.should_shoot() is False


def test_shoot_timer_increments(mock_alien):
    mock_alien.shoot_timer = 0
    mock_alien.shoot_delay = 10
    mock_alien.should_shoot()
    assert mock_alien.shoot_timer == 1


def test_alien_shoots_when_delay_reached(mock_alien):
    mock_alien.shoot_timer = 9
    mock_alien.shoot_delay = 10

    assert mock_alien.should_shoot() is True
    assert mock_alien.shoot_timer == 0



def test_check_edges_inside_screen(mock_alien):
    mock_alien.rect.left = 400
    assert mock_alien.check_edges() is False


def test_check_edges_hits_right_edge(mock_alien):
    mock_alien.rect.right = 800
    assert mock_alien.check_edges() is True


def test_check_edges_hits_left_edge(mock_alien):
    mock_alien.rect.left = -5
    assert mock_alien.check_edges() is True
