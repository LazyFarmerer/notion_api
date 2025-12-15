
from typing import Any, override

from ..abstract.parent import NotionBase
from ..abstract.interface import Update, Remove

from ..object.block_object import parser_database_object_data


class NotionBlock(NotionBase):
    @override
    def __init__(self, api_key: str, page_id: str, object: str="block", type: str = "", value: Any = ""):
        super().__init__(api_key, page_id, object)
        self._type = type
        self._value = value

    # @override
    # def update(self):
    #     return super().update()

    # @override
    # def remove(self) -> bool:
    #     return super().remove()

    @property
    def type(self) -> str:
        return self._type
    def __repr__(self) -> str:
        return f"{{노션 블럭 타입: {self._type}, 값: {self._value}}}"


def _parser_block(api_key: str, data: dict): # -> NotionBlock:
    _id: str = data["id"]
    _object: str = data["object"]
    _type: str = data["type"]
    value = parser_database_object_data(_type, data[_type])
    return NotionBlock(api_key, _id, _object, _type, value)



