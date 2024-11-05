from enum import Enum


class WhisperModels(Enum):
    TINY = "tiny"
    BASE = "base"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"

    @classmethod
    def from_string(cls, value: str):
        for member in cls:
            if member.value == value:
                return member
        return None
