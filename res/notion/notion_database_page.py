
from typing import Any, override

import requests

from ..abstract.parent import NotionBase
from ..abstract.interface import Update, Remove

from ..notion_object.database_object import parser_database_object_data
from ..notion_object.database_object import DatabaseObject


class NotionDatabasePage(NotionBase, Update, Remove):
    @override
    def __init__(self, api_key: str, id: str, object: str, values: dict[str, Any], types: dict[str, str]):
        super().__init__(api_key, id, object)
        self._values = values
        self._types = types

    @override
    def update(self, update_properties_object: DatabaseObject) -> NotionDatabasePage:
        url = f"https://api.notion.com/v1/pages/{self.id}"
        headers = self._add_headers("2025-09-03")
        update_properties = update_properties_object.value

        payload = {
            "in_trash": False,
            "erase_content": False,
            "properties": update_properties
        }

        response = requests.patch(url, json=payload, headers=headers)
        if not response.ok:
            raise ValueError(response.json())

        new_page = _parser_page(self.api_key, response.json())
        # 업데이트
        self._values = new_page._values
        self._types = new_page._types
        return new_page

    @override
    def remove(self) -> bool:
        url = f"https://api.notion.com/v1/pages/{self.id}"
        headers = self._add_headers("2025-09-03")
        payload = {
            "archived": False
        }
        # self.archived = True

        response = requests.patch(url, json=payload, headers=headers)
        # 되살리고 싶다면 archived 를 True 로
        return response.ok

    @property
    def value(self):
        return self._values
    def __str__(self) -> str:
        if self.archived:
            return f"{{페이지: 삭제됨}}"
        result = [f"{key}={value}" for key, value in self._values.items()]
        if 3 < len(result):
            return f"{{페이지: {",".join(result[:3])} ...}}"
        return f"{{페이지: {",".join(result)}}}"



def _parser_page(api_key: str, data: dict) -> NotionDatabasePage:
    _id = data["id"]
    _object = data["object"]
    values = {}
    types = {}
    properties: dict = data["properties"]
    for key, value in properties.items():
        _type: str = value["type"]
        values[key] = parser_database_object_data(_type, value)
        types[key] = _type
    return NotionDatabasePage(api_key, _id, _object, values, types)



