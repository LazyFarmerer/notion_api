
from typing import override

from ..abstract.parent import NotionBase
from ..abstract.interface import Update, Remove


class NotionBlock(NotionBase):
    @override
    def __init__(self, key: str, page_id: str, object: str="block", value: dict | None=None):
        super().__init__(key, page_id, object)
        self._type = type
        if value is None:
            self._value = {}
            return
        self._value = value

    # @override
    # def update(self):
    #     return super().update()

    # @override
    # def remove(self) -> bool:
    #     return super().remove()


def _parser_block(api_key: str, data: dict) -> NotionBlock:
    _id: str = data["id"]
    _object: str = data["object"]
    _type: str = data["type"]
    notiono_bject_class = notion_object_instance_register.dict.get(_type)
    # 있으면 있는대로, 없으면 None
    if notiono_bject_class is None:
        _data = None
    else:
        _data = notiono_bject_class.get( data )

    _value = {
        "type": _type,
        _type: _data
    }
    return NotionBlock(api_key, _id, _object, _value)



