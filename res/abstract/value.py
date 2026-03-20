
from abc import ABC

class DictValueBase(ABC):
    def __init__(self, value: dict | None = None) -> None:
        self._value = value if isinstance(value, dict) else {}

    @property
    def value(self) -> dict:
        return self._value


class ListValueBase(ABC):
    def __init__(self, value: list | None = None) -> None:
        self._value = value if isinstance(value, list) else []

    @property
    def value(self) -> list:
        return self._value
