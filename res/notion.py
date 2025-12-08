
from typing import Any, override

import requests

from .abstract.parent import NotionBase
from .abstract.interface import Write, Read, Update, Remove
from .notion_object.notion_object import NotionObject
from .notion_object.notion_object_base import notion_object_instance_register


class NotionDatabase(NotionBase, Write, Read):
    @override
    def __init__(self, api_key: str, DB_id: str):
        super().__init__(api_key, DB_id, "database")
        self._data_sources: list[DataSource] = []

    @override
    def write(self, write_properties_object_: NotionObject):
        url = "https://api.notion.com/v1/pages"
        headers = self._add_headers("2025-09-03")
        # update_properties = write_properties_object_.value
        payload = {
            "parent": { "database_id": self.id },
            "properties": write_properties_object_.value
        }

        response = requests.post(url, json=payload, headers=headers)
        if not response.ok:
            raise ValueError(response.json())

        # 생성된 페이지 각각 아래 데이터소스한테 주기
        # new_page = parser_page(self.api_key, response.json())
        # [data_sources.append_page(new_page) for data_sources in self._data_sources]

    @override
    def read(self):
        """
        data_sources 얻는 과정
        """
        url = f"https://api.notion.com/v1/databases/{self.id}"
        headers = self._add_headers("2025-09-03")

        response = requests.get(url, headers=headers)
        self._data_sources = self._parse(response.json())
        return self

    def _parse(self, response_data: dict) -> list[DataSource]:
        data_sources: list = response_data["data_sources"]
        result = []
        for data in data_sources:
            data_source = _parse_data_sources(self.api_key, data)
            result.append(data_source)
        return result

    @property
    def value(self):
        return self._data_sources

    def __str__(self) -> str:
        data_sources_count = len(self._data_sources)
        if data_sources_count == 0:
            return "데이터베이스: 데이터 소스 없음"

        stringlist = [str(source) for source in self._data_sources]

        if 3 < data_sources_count:
            return f"[데이터베이스: {",".join(stringlist[:3])}...]"

        return f"[데이터베이스: {",".join(stringlist)}]"


class DataSource(NotionBase, Read):
    @override
    def __init__(self, api_key: str, source_id: str, object: str, name: str) -> None:
        super().__init__(api_key, source_id, object)
        self.name = name
        self._data: list[DatabasePage] = []


    @override
    def read(self):
        url = f"https://api.notion.com/v1/data_sources/{self.id}/query"
        headers = self._add_headers("2025-09-03")
        response = requests.post(url, headers=headers)
        if not response.ok:
            raise ValueError(response.text)
        self._data = self._parser(response.json())
        return self

    def append_page(self, page: DatabasePage | dict):
        if isinstance(page, DatabasePage):
            self._data.append(page)
            

    def _parser(self, response_data: dict):
        results: list = response_data["results"]
        result = []
        for data in results:
            database_page = _parser_page(self.api_key, data)
            result.append(database_page)
        return result

    @property
    def value(self):
        return self._data

    def __str__(self) -> str:
        stringlist = [str(source) for source in self._data]
        if len(stringlist) == 0:
            return f"<{self.name}: 페이지 없음!>"
        if 3 < len(stringlist):
            return f"<{self.name}: {",".join(stringlist[:3]) }...>"
        return f"<{self.name}: {",".join(stringlist)}>"


class DatabasePage(NotionBase, Update, Remove):
    @override
    def __init__(self, api_key: str, id: str, object: str, values: dict[str, Any], types: dict[str, str]):
        super().__init__(api_key, id, object)
        self._values = values
        self._types = types

    @override
    def update(self, update_properties_object: NotionObject) -> DatabasePage:
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


def _parse_data_sources(api_key: str, data: dict) -> DataSource:
    return DataSource(api_key, data["id"], data["object"], data["name"])


def _parser_page(api_key: str, data: dict) -> DatabasePage:
    _id = data["id"]
    _object = data["object"]
    values = {}
    types = {}
    properties: dict = data["properties"]
    for key, value in properties.items():
        _type: str = value["type"]
        # 결과값 values 안에 넣을건데
        # 키 타입에 맞는 클래스꺼내고 .get(value) 가져와서 넣기
        values[key] = notion_object_instance_register.dict[_type].get(value)
        types[key] = _type
    return DatabasePage(api_key, _id, _object, values, types)




