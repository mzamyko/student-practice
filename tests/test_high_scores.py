import pytest
import json
import os
from high_scores import HighScores


@pytest.fixture
def temp_high_scores(tmp_path, monkeypatch):
    fake_file = tmp_path / "test_high_scores.json"

    monkeypatch.setattr(HighScores, "__init__",
                        lambda self: setattr(self, 'file_name', str(fake_file)) or setattr(self, 'scores',
                                                                                           []) or self.load_scores())
    hs = HighScores()
    return hs


def test_load_scores_when_file_missing(temp_high_scores):
    assert temp_high_scores.get_scores() == []


def test_add_and_save_score(temp_high_scores):
    temp_high_scores.add_score("Игрок 1", 500, 2, 30)

    scores = temp_high_scores.get_scores()
    assert len(scores) == 1
    assert scores[0]['name'] == "Игрок 1"
    assert scores[0]['score'] == 500

    assert os.path.exists(temp_high_scores.file_name)


def test_scores_sorting_by_bullets(temp_high_scores):

    temp_high_scores.add_score("Слепой", 100, 1, 100)
    temp_high_scores.add_score("Зрячий", 100, 1, 20)

    scores = temp_high_scores.get_scores()

    assert scores[0]['name'] == "Зрячий"
    assert scores[1]['name'] == "Слепой"


def test_scores_limit_to_top_10(temp_high_scores):

    for i in range(12):
        temp_high_scores.add_score(f"Игрок {i}", 100, 1, i + 10)

    scores = temp_high_scores.get_scores()

    assert len(scores) == 10


def test_clear_scores(temp_high_scores):

    temp_high_scores.add_score("Тест", 100, 1, 10)
    temp_high_scores.clear_scores()

    assert temp_high_scores.get_scores() == []
