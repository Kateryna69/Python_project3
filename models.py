from typing import Dict, List


class UserData:
    def init(self, user_id: str, words: List[Dict[str, str]] = None):
        self.user_id = user_id
        self.words = words if words else []

    def add_word(self, word: str, translation: str):
        self.words.append({"word": word, "translation": translation})

    def delete_word(self, word: str):
        self.words = [w for w in self.words if w["word"] != word]

    def to_dict(self):
        return {"words": self.words}

    @staticmethod
    def from_dict(user_id: str, data: Dict):
        return UserData(user_id, data.get("words", []))