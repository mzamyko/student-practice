import pygame
import os


class SoundManager:
    def __init__(self):
        pygame.mixer.init()

        self.shoot_sound = self._load_sound('shoot.mp3')
        self.hit_sound = self._load_sound('hit.mp3')

        self.shoot_volume = 0.3
        self.hit_volume = 1.0

        self.apply_volumes()

    def _load_sound(self, filename):
        try:
            sound_path = os.path.join(os.path.dirname(__file__), 'sounds', filename)
            sound = pygame.mixer.Sound(sound_path)
            return sound
        except:
            print(f"Звук {filename} не найден")
            return None

    def apply_volumes(self):
        if self.shoot_sound:
            self.shoot_sound.set_volume(self.shoot_volume)
        if self.hit_sound:
            self.hit_sound.set_volume(self.hit_volume)

    def play_shoot(self):
        if self.shoot_sound:
            self.shoot_sound.play()

    def play_hit(self):
        if self.hit_sound:
            self.hit_sound.play()

    def set_shoot_volume(self, volume):
        self.shoot_volume = max(0, min(1, volume))
        if self.shoot_sound:
            self.shoot_sound.set_volume(self.shoot_volume)

    def set_hit_volume(self, volume):
        self.hit_volume = max(0, min(1, volume))
        if self.hit_sound:
            self.hit_sound.set_volume(self.hit_volume)

    def get_shoot_volume(self):
        return self.shoot_volume

    def get_hit_volume(self):
        return self.hit_volume