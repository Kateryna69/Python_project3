from dataclasses import dataclass, field
from typing import Dict

@dataclass
class UserData:
    words: Dict[str, str] = field(default_factory=dict)  # англійське слово → переклад