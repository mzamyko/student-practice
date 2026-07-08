import json
import os


class HighScores:
    """Класс для управления таблицей рекордов."""

    def __init__(self):
        self.file_name = 'high_scores.json'
        self.scores = []
        self.load_scores()

    def load_scores(self):
        """Загружает рекорды из файла."""
        if os.path.exists(self.file_name):
            try:
                with open(self.file_name, 'r') as f:
                    self.scores = json.load(f)
            except:
                self.scores = []
        else:
            self.scores = []

    def save_scores(self):
        """Сохраняет рекорды в файл."""
        with open(self.file_name, 'w') as f:
            json.dump(self.scores, f)

    def add_score(self, name, score, level, bullets_used):
        """Добавляет новый рекорд."""
        self.scores.append({
            'name': name,
            'score': score,
            'level': level,
            'bullets_used': bullets_used
        })

        # Сортируем по количеству пуль (меньше = лучше)
        self.scores.sort(key=lambda x: x['bullets_used'])

        # Оставляем только топ-10
        if len(self.scores) > 10:
            self.scores = self.scores[:10]

        self.save_scores()

    def get_scores(self):
        """Возвращает список рекордов."""
        return self.scores

    def clear_scores(self):
        """Очищает таблицу рекордов."""
        self.scores = []
        self.save_scores()