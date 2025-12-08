from typing import override, overload

import requests

from .abstract.parent import NotionBase
from .abstract.interface import Write, Read, Update, Remove
from .notion import DatabasePage, _parser_page
from .notion_object.notion_object import NotionObject
from .notion_object.database_query import FilterBase, SortBase

class NotionDatabaseLite(NotionBase, Write, Read, Update, Remove):
    @override
    def __init__(self, key: str, DB_id: str):
        super().__init__(key, DB_id, "database")
        self._datas: list[DatabasePage] = []

    @override
    def write(self, write_properties_object_: NotionObject):
        url = "https://api.notion.com/v1/pages"
        headers = self._add_headers("2025-09-03")

        payload = {
            "parent": { "database_id": self.id },
            "properties": write_properties_object_.value
        }

        response = requests.post(url, json=payload, headers=headers)
        if not response.ok:
            raise ValueError(response.json())
        
        new_page = _parser_page(self.api_key, response.json())
        self._datas.append(new_page)
        return new_page

    @override
    def read(self, *, filter_: FilterBase | None = None, sort: SortBase | None = None):
        url = f"https://api.notion.com/v1/databases/{self.id}/query"
        headers = self._add_headers("2022-06-28")

        payload = {}
        payload["page_size"] = 100
        if filter_ is not None: payload["filter"] = filter_.value
        if sort is not None: payload["sorts"] = sort.value

        response = requests.post(url, json=payload, headers=headers)
        if not response.ok:
            raise ValueError(response.json())
        
        self._datas = self._parse(response.json())

    @overload
    def update(self, page_or_index: DatabasePage, update_properties_object_: NotionObject):
        """해당 페이지 업데이트"""
    @overload
    def update(self, page_or_index: int, update_properties_object_: NotionObject):
        """해당 인덱스 업데이트"""
    @override
    def update(self, page_or_index: DatabasePage | int, update_properties_object_: NotionObject):
        if isinstance(page_or_index, int):
            obj = self.value[page_or_index]
        elif isinstance(page_or_index, DatabasePage):
            obj = page_or_index

        # 해당 페이지 업데이트
        obj.update( update_properties_object_ )

    @overload
    def remove(self, page_or_index: DatabasePage):
        """해당 페이지 삭제"""
    @overload
    def remove(self, page_or_index: int):
        """해당 인덱스 삭제"""
    @override
    def remove(self, page_or_index: DatabasePage | int) -> bool:
        if isinstance(page_or_index, int):
            obj = self.value[page_or_index]
        elif isinstance(page_or_index, DatabasePage):
            obj = page_or_index

        # 해당 페이지 삭제
        return obj.remove()

    def _parse(self, response_data: dict) -> list[DatabasePage]:
        results: list = response_data["results"]
        result = []
        for data in results:
            database_page = _parser_page(self.api_key, data)
            result.append(database_page)
        return result

    @property
    def value(self):
        return self._datas

    def __str__(self) -> str:
        data_sources_count = len(self._datas)
        if data_sources_count == 0:
            return "데이터베이스: 데이터 소스 없음"

        stringlist = [str(source) for source in self._datas]

        if 3 < data_sources_count:
            return f"[데이터베이스: {",".join(stringlist[:3])}...]"

        return f"[데이터베이스: {",".join(stringlist)}]"