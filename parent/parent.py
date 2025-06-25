from abc import ABCMeta, abstractmethod
from collections.abc import KeysView, ValuesView
import json

from ..notion_object.notion_object import NotionObject


class Read(metaclass=ABCMeta):
    @abstractmethod
    def read(self):
        raise NotImplementedError


class Write(metaclass=ABCMeta):
    @abstractmethod
    def write(self):
        raise NotImplementedError


class Update(metaclass=ABCMeta):
    @abstractmethod
    def update(self):
        raise NotImplementedError


class Remove(metaclass=ABCMeta):
    @abstractmethod
    def remove(self):
        raise NotImplementedError


class NotionParent:
    def __init__(self, api_key: str, id: str):
        self.api_key = api_key
        self.id = id
        self.datas: list[dict] = []
        self.original_data: dict

        self._data_parser = NotionDataParser()

    def _add_headers(self, version: str):
        "헤더에 버젼을 추가해서 리턴"
        return {
            "Accept": "application/json",
            "Notion-Version": version,
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def __join(self, data_list: KeysView | ValuesView):
        listStr = [f"{'' if item is None else item}" for item in data_list]
        return ",".join(listStr)

    @property
    def to_string(self) -> str:
        if len(self.datas) == 1:
            return json.dumps(self.datas[0], ensure_ascii=False)
        return json.dumps(self.datas, ensure_ascii=False)

    @property
    def to_json(self) -> list[dict] | dict:
        if len(self.datas) == 1:
            return self.datas[0]
        return self.datas

    @property
    def to_csv(self) -> str:
        "csv 형식의 문자열을 반환합니다"
        datas = self.datas
        result = ""
        for i, data in enumerate(datas):
            if i == 0:
                result += self.__join(data.keys())
                result += "\n"
            print(data.values())
            result += self.__join(data.values())
            if i != len(datas)-1:
                result += "\n"
        return result

    def __repr__(self) -> str:
        if len(self.datas) == 1:
            return json.dumps(self.datas[0], ensure_ascii=False) #, indent="\t")
        return json.dumps(self.datas, ensure_ascii=False) #, indent="\t")

    def __getitem__(self, value: str | int):
        if isinstance(value, int):
            return self.datas[value]

        if len(self.datas) != 1:
            raise ValueError("값이 여러개임")

        return self.datas[0][value]


class NotionDataParser:
    def parse_database(self, data: dict, datas: list[dict], notionObject: NotionObject) -> list[dict]:
        "데이터베이스를 파싱해서 보기좋게 가공"

        if data["object"] != "list":
            raise ValueError(f"\ndatabase 아님. 아래는 내용\n{data}")

        datas = []
        results_datas: list[dict] = data["results"]

        for item in results_datas:
            result = {"result": {}}
            result["id"] = item["id"]
            result["object"] = item["object"]
            for key, value in item["properties"].items():
                type_ = value["type"]
                if hasattr(notionObject, f"get_{type_}"):
                    # result["type"] = type_
                    result["result"][key] = getattr(notionObject, f"get_{type_}")(value)
            datas.append(result)
        return datas

    def parse_page(self, data: dict, datas: list[dict], notionObject: NotionObject):
        if data["object"] != "list":
            raise ValueError(f"\npage 아님. 아래는 내용\n{data}")

        datas = []
        results_datas: list[dict] = data["results"]
        for item in results_datas:
            result = {}
            result["id"] = item["id"]
            result["object"] = item["object"]
            type_ = item["type"]
            if hasattr(notionObject, f"get_{type_}"):
                result["type"] = type_
                result[type_] = getattr(notionObject, f"get_{type_}")(item)
            datas.append(result)

        return datas

    def parse_block(self, data: dict, datas: list[dict], notionObject: NotionObject):
        if data["object"] != "block":
            raise ValueError(f"\nblock 아님. 아래는 내용\n{data}")

        result = {}
        result["id"] = data["id"]
        result["object"] = data["object"]
        type_ = data["type"]
        if hasattr(notionObject, f"get_{type_}"):
            result["type"] = type_
            result[type_] = getattr(notionObject, f"get_{type_}")(data)
        return [result]
