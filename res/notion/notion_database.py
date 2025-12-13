

from typing import override

import requests

from ..abstract.parent import NotionBase
from ..abstract.interface import Write, Read
from .notion_data_source import DataSource, _parse_data_sources
from ..notion_object.database_object import DatabaseObject


class NotionDatabase(NotionBase, Write, Read):
    @override
    def __init__(self, api_key: str, DB_id: str, object: str="database"):
        super().__init__(api_key, DB_id, object)
        self._data_sources: list[DataSource] = []

    @override
    def write(self, properties_object: DatabaseObject):
        url = "https://api.notion.com/v1/pages"
        headers = self._add_headers("2025-09-03")

        payload = {
            "parent": { "database_id": self.id },
            "properties": properties_object.value
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
            joined = ",".join(stringlist[:3])
            return f"[데이터베이스: {joined}...]"

        joined = ",".join(stringlist)
        return f"[데이터베이스: {joined}]"
