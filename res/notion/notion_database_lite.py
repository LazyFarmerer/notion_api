from typing import override, overload

import requests

from ..abstract.parent import NotionBase
from ..abstract.interface import Write, Read, Update, Remove
from .notion_database_page import NotionDatabasePage, _parser_page


from ...object.database_object import DatabaseObject
from ...query.filter import FilterBase
from ...query.sort import SortBase

class NotionDatabaseLite(NotionBase, Write, Read, Update, Remove):
    @override
    def __init__(self, key: str, DB_id: str):
        super().__init__(key, DB_id, "database")
        self._datas: list[NotionDatabasePage] = []

    @override
    def write(self, write_properties_object_: DatabaseObject):
        url = "https://api.notion.com/v1/pages"
        headers = self._add_headers("2022-06-28")

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
    def read(self, *, filter: FilterBase | dict | None = None, sort: SortBase | dict | None = None, page_size: int=100):
        """
        ㅁㄴㅇㅁㄴㅇ

        Args:
            filter:  Filter 오브젝트를 이용해서 표현하거나, 아니면 순수 딕셔너리를 이용
            sort: 정렬 기준
            page_size: 검색수 (최대 100)
        """
        url = f"https://api.notion.com/v1/databases/{self.id}/query"
        headers = self._add_headers("2022-06-28")

        payload = {}
        payload["page_size"] = max(0, min(page_size, 100))
        if filter is not None:
            if isinstance(filter, FilterBase):
                payload["filter"] = filter.value
            elif isinstance(filter, dict):
                payload["filter"] = filter
        if sort is not None:
            if isinstance(sort, SortBase):
                payload["sorts"] = sort.value
            elif isinstance(sort, dict):
                payload["sorts"] = sort

        response = requests.post(url, json=payload, headers=headers)
        if not response.ok:
            raise ValueError(response.json())
        
        self._datas = self._parse(response.json())

    @overload
    def update(self, page_or_index: NotionDatabasePage, update_properties_object_: DatabaseObject):
        """해당 페이지 업데이트"""
    @overload
    def update(self, page_or_index: int, update_properties_object_: DatabaseObject):
        """해당 인덱스 업데이트"""
    @override
    def update(self, page_or_index: NotionDatabasePage | int, update_properties_object_: DatabaseObject):
        if isinstance(page_or_index, int):
            obj = self.value[page_or_index]
        elif isinstance(page_or_index, NotionDatabasePage):
            obj = page_or_index

        # 해당 페이지 업데이트
        obj.update( update_properties_object_ )

    @overload
    def remove(self, page_or_index: NotionDatabasePage):
        """해당 페이지 삭제"""
    @overload
    def remove(self, page_or_index: int):
        """해당 인덱스 삭제"""
    @override
    def remove(self, page_or_index: NotionDatabasePage | int) -> bool:
        if isinstance(page_or_index, int):
            obj = self.value[page_or_index]
        elif isinstance(page_or_index, NotionDatabasePage):
            obj = page_or_index

        # 해당 페이지 삭제
        return obj.remove()

    def _parse(self, response_data: dict) -> list[NotionDatabasePage]:
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

