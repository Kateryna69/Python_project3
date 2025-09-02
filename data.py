import json
from pathlib import Path
from models import UserWords

DATA_FILE = Path("data.json")

def load_data() -> dict:
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data: dict):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_word(user_id: int, word: str):
    data = load_data()
    words = data.get(str(user_id), [])
    if word not in words:
        words.append(word)
    data[str(user_id)] = words
    save_data(data)

def delete_word(user_id: int, word: str):
    data = load_data()
    words = data.get(str(user_id), [])
    if word in words:
        words.remove(word)
    data[str(user_id)] = words
    save_data(data)

def get_words(user_id: int) -> list:
    data = load_data()
    return data.get(str(user_id), [])