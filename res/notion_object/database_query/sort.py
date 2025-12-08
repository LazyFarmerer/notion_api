
from typing import Literal


class SortBase:
    def __init__(self, value: list | None = None) -> None:
        if value is None:
            self.value = []
            return

        self.value = value

class _Sort(SortBase):
    def sort(self, property_: str, direction: Literal["ascending", "descending"]):
        result = {
            "property": property_,
            "direction": direction }

        self.value.append(result)
        return _Sort(self.value)


class Sort(SortBase):
    @classmethod
    def sort(cls, property_: str, direction: Literal["ascending", "descending"]):
        result = {
            "property": property_,
            "direction": direction }
        return _Sort( [result] )


