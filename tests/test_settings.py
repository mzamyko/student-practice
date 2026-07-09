import pytest
from settings import Settings


def test_settings_initialization():
    settings = Settings()

    assert settings.screen_width == 1200
    assert settings.ship_limit == 3
    assert settings.ship_speed == 1.5
    assert settings.bullet_speed == 3.0
    assert settings.alien_speed == 0.5
    assert settings.alien_points == 15
    assert settings.pink_alien_points == 30
    assert settings.fleet_direction == 1


def test_initialize_dynamic_settings():
    settings = Settings()

    settings.ship_speed = 5.0
    settings.alien_speed = 3.2
    settings.alien_points = 100
    settings.fleet_direction = -1

    settings.initialize_dynamic_settings()

    assert settings.ship_speed == 1.5
    assert settings.alien_speed == 0.5
    assert settings.alien_points == 15
    assert settings.fleet_direction == 1


def test_increase_speed():
    settings = Settings()

    old_ship_speed = settings.ship_speed
    old_bullet_speed = settings.bullet_speed
    old_alien_speed = settings.alien_speed

    settings.increase_speed()

    assert pytest.approx(settings.ship_speed) == old_ship_speed * settings.speedup_scale
    assert pytest.approx(settings.bullet_speed) == old_bullet_speed * settings.speedup_scale
    assert pytest.approx(settings.alien_speed) == old_alien_speed * settings.speedup_scale

    assert settings.alien_points == int(15 * 1.5)
    assert settings.pink_alien_points == int(30 * 1.5)
