import json
import os

SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"

def load_settings():
    """Загрузка настроек при запуске"""
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {"car_color": (255, 0, 0), "difficulty": 1}

def save_settings(settings):
    """Сохранение настроек"""
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)

def get_top_scores():
    """Получение топ-10 результатов"""
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    return []

def save_score(name, score, distance):
    """Обновление таблицы лидеров"""
    scores = get_top_scores()
    scores.append({"name": name, "score": score, "distance": int(distance)})
    # Сортировка по очкам (топ-10)
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:10]
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(scores, f)