import pytest
import pygame
from unittest.mock import Mock


@pytest.fixture(scope="session", autouse=True)
def init_pygame():
    pygame.init()
    pygame.display.set_mode((1, 1), pygame.NOFRAME)
    yield
    pygame.quit()


@pytest.fixture
def mock_menu():
    menu = Mock()

    from menu import Menu
    menu.check_click = Menu.check_click.__get__(menu, Mock)
    menu.check_volume_click = Menu.check_volume_click.__get__(menu, Mock)
    menu.update_shoot_volume = Menu.update_shoot_volume.__get__(menu, Mock)

    menu.current_menu = 'main'
    menu.dragging_shoot = False
    menu.dragging_hit = False

    menu.play_button = Mock()
    menu.play_button.rect = pygame.Rect(100, 100, 200, 50)

    menu.rules_button = Mock()
    menu.rules_button.rect = pygame.Rect(100, 200, 200, 50)

    menu.scores_button = Mock()
    menu.scores_button.rect = pygame.Rect(100, 300, 200, 50)

    menu.volume_button = Mock()
    menu.volume_button.rect = pygame.Rect(100, 400, 200, 50)

    menu.back_button = Mock()
    menu.back_button.rect = pygame.Rect(100, 500, 200, 50)

    menu.shoot_slider_rect = pygame.Rect(300, 400, 200, 40)
    menu.hit_slider_rect = pygame.Rect(300, 480, 200, 40)

    menu.sound_manager = Mock()

    return menu


def test_check_click_main_menu_to_rules(mock_menu):
    mock_menu.current_menu = 'main'
    result = mock_menu.check_click((150, 220))

    assert result == 'rules'
    assert mock_menu.current_menu == 'rules'


def test_check_click_miss(mock_menu):
    mock_menu.current_menu = 'main'

    result = mock_menu.check_click((0, 0))

    assert result is None
    assert mock_menu.current_menu == 'main'




def test_check_volume_click_activates_dragging(mock_menu):
    mock_menu.dragging_shoot = False

    result = mock_menu.check_volume_click((350, 420))

    assert result is True
    assert mock_menu.dragging_shoot is True


def test_update_shoot_volume_calculation(mock_menu):
    mock_menu.update_shoot_volume((400, 420))

    called_args = mock_menu.sound_manager.set_shoot_volume.call_args[0][0]
    assert pytest.approx(called_args) == 0.5


def test_update_shoot_volume_overflow_protection(mock_menu):
    mock_menu.update_shoot_volume((1500, 420))

    called_args = mock_menu.sound_manager.set_shoot_volume.call_args[0][0]
    assert called_args == 1.0
