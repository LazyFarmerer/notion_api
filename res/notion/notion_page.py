
from typing import override

import requests

from ..abstract.parent import NotionBase
from ..abstract.interface import Write, Read
from .notion_block import NotionBlock
from ..notion_object.block_object import BlockObject, parser_database_object_data


class NotionPage(NotionBase, Write, Read):
    @override
    def __init__(self, key: str, page_id: str, object: str="page"):
        super().__init__(key, page_id, object)
        self._blocks: list[NotionBlock] = []

    @override
    def write(self, properties_object: BlockObject, *args: BlockObject):
        url = f"https://api.notion.com/v1/blocks/{self.id}/children"
        headers = self._add_headers("2025-09-03")

        notion_objects = [ properties_object.value ]
        notion_objects.extend( [ notion_obj.value for notion_obj in args ] )
        payload = {
            "children": notion_objects
        }

        response = requests.patch(url, json=payload, headers=headers)
        print(response.json())
        notion_blocks = self._parse(response.json())
        self._blocks.extend(notion_blocks)

    @override
    def read(self):
        url = f"https://api.notion.com/v1/blocks/{self.id}/children?page_size=100"
        headers = self._add_headers("2022-06-28")

        response = requests.get(url, headers=headers)
        self._blocks = self._parse(response.json())
        return response

    def _parse(self, response_data: dict) -> list[NotionBlock]:
        _blocks_data: list = response_data["results"]
        result: list[NotionBlock] = []
        for block_data in _blocks_data:
            notion_block = parser_database_object_data(self.api_key, block_data)
            print(notion_block)
            result.append(notion_block)
        return result