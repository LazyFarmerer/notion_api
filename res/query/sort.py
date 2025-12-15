
from typing import Literal

from ..abstract.value import ListValueBase


class SortBase(ListValueBase): ...


class Sort(SortBase):
    @classmethod
    def sort(cls, property_: str, direction: Literal["ascending", "descending"]):
        result = {
            "property": property_,
            "direction": direction }
        return _Sort( [result] )


class _Sort(SortBase):
    def sort(self, property_: str, direction: Literal["ascending", "descending"]):
        result = {
            "property": property_,
            "direction": direction }

        self._value.append(result)
        return self

