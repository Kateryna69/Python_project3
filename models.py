from dataclasses import dataclass
from typing import List

@dataclass
class UserWords:
    user_id: int
    words: List[str]