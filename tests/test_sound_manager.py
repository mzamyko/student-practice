import pytest
from unittest.mock import Mock


@pytest.fixture
def mock_sound_manager():
    sm = Mock()

    from sound_manager import SoundManager
    sm.set_shoot_volume = SoundManager.set_shoot_volume.__get__(sm, Mock)
    sm.set_hit_volume = SoundManager.set_hit_volume.__get__(sm, Mock)
    sm.get_shoot_volume = SoundManager.get_shoot_volume.__get__(sm, Mock)
    sm.get_hit_volume = SoundManager.get_hit_volume.__get__(sm, Mock)

    sm.shoot_volume = 0.3
    sm.hit_volume = 1.0

    sm.shoot_sound = Mock()
    sm.hit_sound = Mock()

    return sm



def test_set_shoot_volume_valid(mock_sound_manager):
    mock_sound_manager.set_shoot_volume(0.6)

    assert mock_sound_manager.get_shoot_volume() == 0.6
    mock_sound_manager.shoot_sound.set_volume.assert_called_with(0.6)


def test_set_hit_volume_valid(mock_sound_manager):
    mock_sound_manager.set_hit_volume(0.1)

    assert mock_sound_manager.get_hit_volume() == 0.1
    mock_sound_manager.hit_sound.set_volume.assert_called_with(0.1)



def test_volume_limits_underflow(mock_sound_manager):
    mock_sound_manager.set_shoot_volume(-0.5)

    assert mock_sound_manager.get_shoot_volume() == 0.0
    mock_sound_manager.shoot_sound.set_volume.assert_called_with(0.0)


def test_volume_limits_overflow(mock_sound_manager):
    mock_sound_manager.set_hit_volume(2.5)

    assert mock_sound_manager.get_hit_volume() == 1.0
    mock_sound_manager.hit_sound.set_volume.assert_called_with(1.0)
