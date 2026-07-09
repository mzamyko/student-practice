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
def mock_shop():
    shop = Mock()
    from shop import Shop
    shop.handle_click = Shop.handle_click.__get__(shop, Mock)
    shop.update_buttons = Shop.update_buttons.__get__(shop, Mock)
    shop.start = Shop.start.__get__(shop, Mock)
    shop.close = Shop.close.__get__(shop, Mock)
    shop.show_error = Shop.show_error.__get__(shop, Mock)
    shop.update = Shop.update.__get__(shop, Mock)

    shop.bullet_speed_level = 0
    shop.max_bullet_speed = 3
    shop.bullet_speed_price = 100

    shop.bullet_count_level = 0
    shop.max_bullet_count = 3
    shop.bullet_count_price = 200

    shop.ship_skin = 0
    shop.max_skins = 4
    shop.ship_skin_price = 300

    shop.active = True
    shop.error_message = ""
    shop.error_timer = 0

    shop.exit_button = Mock()
    shop.exit_button.rect = pygame.Rect(0, 0, 50, 50)

    shop.bullet_speed_button = Mock()
    shop.bullet_speed_button.rect = pygame.Rect(100, 100, 200, 50)
    shop.bullet_speed_button.disabled = False

    shop.bullet_count_button = Mock()
    shop.bullet_count_button.rect = pygame.Rect(100, 200, 200, 50)
    shop.bullet_count_button.disabled = False

    shop.ship_skin_button = Mock()
    shop.ship_skin_button.rect = pygame.Rect(100, 300, 200, 50)
    shop.ship_skin_button.disabled = False

    shop.stats = Mock()
    shop.stats.total_score = 500

    shop.settings = Mock()
    shop.settings.bullet_speed = 3.0

    shop.ai_game = Mock()
    shop.ai_game.sb = Mock()
    shop.ai_game.ship = Mock()

    shop.font_small = Mock()
    shop.font_small.render.return_value = pygame.Surface((10, 10))

    return shop


def test_purchase_bullet_speed_success(mock_shop):
    mock_shop.stats.total_score = 500
    mock_shop.bullet_speed_price = 100
    mock_shop.bullet_speed_level = 0
    mock_shop.settings.bullet_speed = 3.0

    result = mock_shop.handle_click((150, 120))

    assert result is True
    assert mock_shop.stats.total_score == 400
    assert mock_shop.bullet_speed_level == 1
    assert mock_shop.bullet_speed_price == 150
    assert mock_shop.settings.bullet_speed == 3.5
    mock_shop.ai_game.sb.prep_score.assert_called()


def test_purchase_insufficient_stars(mock_shop):
    mock_shop.stats.total_score = 50
    mock_shop.bullet_speed_price = 100
    mock_shop.bullet_speed_level = 0

    result = mock_shop.handle_click((150, 120))

    assert result is False
    assert mock_shop.stats.total_score == 50
    assert mock_shop.bullet_speed_level == 0
    assert mock_shop.error_message == "Недостаточно звёзд!"
    assert mock_shop.error_timer == 120



def test_bullet_speed_max_level_disables_button(mock_shop):
    mock_shop.bullet_speed_level = 3
    mock_shop.bullet_speed_button.disabled = False

    mock_shop.update_buttons()

    assert mock_shop.bullet_speed_button.disabled is True


def test_cannot_click_disabled_button(mock_shop):
    mock_shop.stats.total_score = 1000
    mock_shop.bullet_speed_button.disabled = True

    result = mock_shop.handle_click((150, 120))

    assert result is False
    assert mock_shop.stats.total_score == 1000


def test_shop_exit_button(mock_shop):
    mock_shop.active = True

    result = mock_shop.handle_click((20, 20))

    assert result is True
    assert mock_shop.active is False


def test_error_timer_countdown(mock_shop):
    mock_shop.error_message = "Ошибка"
    mock_shop.error_timer = 1

    mock_shop.update()

    assert mock_shop.error_timer == 0
    assert mock_shop.error_message == ""
