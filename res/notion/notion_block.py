
from typing import Any, override

import requests

from ..abstract.parent import NotionBase
from ..abstract.interface import Update, Remove

from ..object.block_object import parser_database_object_data, BlockObject


class NotionBlock(NotionBase, Update, Remove):
    @override
    def __init__(self, api_key: str, block_id: str, object: str="block", type: str = "", value: Any = ""):
        super().__init__(api_key, block_id, object)
        self._type = type
        self._value = value

    @override
    def update(self, value: Any):
        url = f"https://api.notion.com/v1/blocks/{self.id}"
        header = self._add_headers("2025-09-03")

        if hasattr(BlockObject(), self._type):
            data = getattr(BlockObject(), self._type)(value)
        payload = { self._type: data }

        response = requests.patch(url, json=payload, headers=header)
        if (response.ok == False):
            raise ValueError(response.text)

        return self


    @override
    def remove(self) -> bool:
        url = f"https://api.notion.com/v1/blocks/{self.id}"
        header = self._add_headers("2025-09-03")
        
        response = requests.delete(url, headers=header)
        if (response.ok == False):
            raise ValueError(response.text)

        self.archived = False
        return response.ok

    @property
    def type(self) -> str:
        return self._type
    @property
    def value(self) -> Any:
        return self._value
    def __repr__(self) -> str:
        if self.archived:
            return f"{{페이지: 삭제됨}}"
        return f"{{노션 블럭 타입: {self._type}, 값: {self._value}}}"


def _parser_block(api_key: str, data: dict): # -> NotionBlock:
    _id: str = data["id"]
    _object: str = data["object"]
    _type: str = data["type"]
    value = parser_database_object_data(_type, data[_type])
    return NotionBlock(api_key, _id, _object, _type, value)



