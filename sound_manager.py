import pygame
import os


class SoundManager:
    """Класс для управления звуками в игре."""

    def __init__(self):
        """Инициализирует звуковой менеджер."""
        pygame.mixer.init()

        # Загружаем звуки из файлов
        self.shoot_sound = self._load_sound('shoot.mp3')
        self.hit_sound = self._load_sound('hit.mp3')

        # Громкость для каждого звука (от 0 до 1)
        self.shoot_volume = 0.3  # Громкость выстрела
        self.hit_volume = 1.0  # Громкость попадания

        # Применяем громкость
        self.apply_volumes()

    def _load_sound(self, filename):
        """Загружает звук из файла."""
        try:
            sound_path = os.path.join(os.path.dirname(__file__), 'sounds', filename)
            sound = pygame.mixer.Sound(sound_path)
            return sound
        except:
            print(f"Звук {filename} не найден")
            return None

    def apply_volumes(self):
        """Применяет текущие настройки громкости."""
        if self.shoot_sound:
            self.shoot_sound.set_volume(self.shoot_volume)
        if self.hit_sound:
            self.hit_sound.set_volume(self.hit_volume)

    def play_shoot(self):
        """Воспроизводит звук выстрела."""
        if self.shoot_sound:
            self.shoot_sound.play()

    def play_hit(self):
        """Воспроизводит звук попадания."""
        if self.hit_sound:
            self.hit_sound.play()

    def set_shoot_volume(self, volume):
        """Устанавливает громкость выстрела."""
        self.shoot_volume = max(0, min(1, volume))
        if self.shoot_sound:
            self.shoot_sound.set_volume(self.shoot_volume)

    def set_hit_volume(self, volume):
        """Устанавливает громкость попадания."""
        self.hit_volume = max(0, min(1, volume))
        if self.hit_sound:
            self.hit_sound.set_volume(self.hit_volume)

    def get_shoot_volume(self):
        """Возвращает громкость выстрела."""
        return self.shoot_volume

    def get_hit_volume(self):
        """Возвращает громкость попадания."""
        return self.hit_volume