
from typing import override

import requests

from ..abstract.parent import NotionBase
from ..abstract.interface import Write, Read
from .notion_database_page import NotionDatabasePage, _parser_page


class DataSource(NotionBase, Read):
    @override
    def __init__(self, api_key: str, source_id: str, object: str, name: str) -> None:
        super().__init__(api_key, source_id, object)
        self.name = name
        self._data: list[NotionDatabasePage] = []


    @override
    def read(self):
        url = f"https://api.notion.com/v1/data_sources/{self.id}/query"
        headers = self._add_headers("2025-09-03")
        response = requests.post(url, headers=headers)
        if not response.ok:
            raise ValueError(response.text)
        self._data = self._parser(response.json())
        return self

    def append_page(self, page: NotionDatabasePage | dict):
        if isinstance(page, NotionDatabasePage):
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


def _parse_data_sources(api_key: str, data: dict) -> DataSource:
    return DataSource(api_key, data["id"], data["object"], data["name"])
