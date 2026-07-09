import pytest
import pygame
from unittest.mock import Mock
from name_input import NameInput


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
    ai_game.stats = Mock()
    ai_game.stats.total_score = 1000
    ai_game.stats.level_score = 200
    ai_game.stats.bullets_fired = 50
    return ai_game



def test_name_input_default_fallback(mock_game):
    ni = NameInput(mock_game)
    ni.name = ""
    assert ni.get_name() == "Player"
    ni.name = "   "
    assert ni.get_name() == "Player"

def test_add_char_limits_max_length(mock_game):
    ni = NameInput(mock_game)
    ni.name = "123456789012345"

    ni.add_char("A")

    assert len(ni.name) == 15
    assert ni.name == "123456789012345"


def test_remove_char(mock_game):
    ni = NameInput(mock_game)
    ni.name = "Alex"

    ni.remove_char()
    assert ni.name == "Ale"


def test_handle_event_ignored_when_inactive(mock_game):
    ni = NameInput(mock_game)
    ni.active = False

    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    result = ni.handle_event(event)

    assert result is False


def test_handle_event_add_text_char(mock_game):
    ni = NameInput(mock_game)
    ni.active = True
    ni.name = "Max"

    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_i, unicode="i")
    ni.handle_event(event)

    assert ni.name == "Maxi"


def test_handle_event_backspace(mock_game):
    ni = NameInput(mock_game)
    ni.active = True
    ni.name = "Tom"

    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_BACKSPACE)
    ni.handle_event(event)

    assert ni.name == "To"


def test_handle_event_enter_saves(mock_game):
    ni = NameInput(mock_game)
    ni.active = True

    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    result = ni.handle_event(event)

    assert result is True
    assert ni.active is False



def test_cursor_blinking(mock_game):
    ni = NameInput(mock_game)
    ni.active = True
    ni.cursor_visible = True
    ni.cursor_timer = 29

    ni.update()

    assert ni.cursor_timer == 0
    assert ni.cursor_visible is False
