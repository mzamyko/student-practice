import pytest
from unittest.mock import Mock
from game_stats import GameStats


@pytest.fixture
def mock_game():
    ai_game = Mock()
    ai_game.settings = Mock()
    ai_game.settings.ship_limit = 3
    return ai_game


def test_stats_initialization(mock_game):
    stats = GameStats(mock_game)

    assert stats.game_active is False
    assert stats.high_score == 0
    assert stats.ships_left == 3
    assert stats.level == 1
    assert stats.total_score == 0
    assert stats.bullets_fired == 0


def test_add_score(mock_game):
    stats = GameStats(mock_game)

    stats.add_score(150)
    assert stats.level_score == 150

    stats.add_score(50)
    assert stats.level_score == 200


def test_complete_level(mock_game):
    stats = GameStats(mock_game)

    stats.add_score(500)

    stats.complete_level()

    assert stats.total_score == 500
    assert stats.get_final_score() == 500
    assert stats.level_score == 0


def test_add_bullet(mock_game):
    stats = GameStats(mock_game)

    stats.add_bullet()
    stats.add_bullet()

    assert stats.bullets_fired == 2


def test_reset_stats(mock_game):
    stats = GameStats(mock_game)

    stats.ships_left = 1
    stats.total_score = 1000
    stats.level = 4
    stats.bullets_fired = 50

    stats.reset_stats()

    assert stats.ships_left == 3
    assert stats.total_score == 0
    assert stats.level == 1
    assert stats.bullets_fired == 0
