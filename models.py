from pydantic import BaseModel
from typing import Dict

class UserWords(BaseModel):
    user_id: str
    words: Dict[str, str] = {}  # англійське слово -> переклад