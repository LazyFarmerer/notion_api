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


class NotionParent:
    def __init__(self, api_key: str, id: str):
        self.api_key = api_key
        self.id = id
        self.datas: list[dict] = []

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
    def parse_response(self, data: dict, datas: list[dict], notionObject: NotionObject):
        "받은 정보를 내가 보기좋게 가공"
        result = {}
        result_list = datas

        if data["object"] == "list":
            results_datas: list[dict] = data["results"]
            if results_datas is None:
                raise ValueError("\n뭐 받음???")

            for item in results_datas:
                result = {}
                if item["object"] == "page_or_database":
                    result = self.__parse_page(item, notionObject)
                elif item["object"] == "page":
                    result = self.__parse_page(item, notionObject)
                elif item["object"] == "block":
                    result = self.__parse_block(item, notionObject)
                result_list.append(result)
            return result_list

        elif data["object"] == "page":
            result = self.__parse_page(data, notionObject)
            
            if len(result_list) == 0:
                result_list.append(result)
            for index, item in enumerate(result_list):
                if item["id"] == result["id"]:
                    result_list[index] = result
                    return result_list

        elif data["object"] == "block":
            result = self.__parse_block(data, notionObject)

            if len(result_list) == 0:
                result_list.append(result)
            for index, item in enumerate(result_list):
                if item["id"] == result["id"]:
                    result_list[index] = result
                    return result_list

        raise ValueError(f"\nlist 또는 page 아님. 아래는 내용\n{data}")

    def __parse_block(self, item: dict, notionObject: NotionObject):
        """
        parse_response() 메서드 처리하는 과정에서 떼어낸 함수\n
        일반적으로 내가 호출 X
        """

        result = {}
        result["id"] = item["id"]
        result["object"] = item["object"]
        type_ = item["type"]
        result["type"] = type_

        if type_ == "child_page":
            result["title"] = item[type_]["title"]
        if type_ == "code":
            result["language"] = item[type_]["language"]

        if hasattr(notionObject, f"get_{type_}"):
            result[type_] = getattr(notionObject, f"get_{type_}")(item)

        return result

    def __parse_page(self, item: dict, notionObject: NotionObject):
        """
        parse_response() 메서드 처리하는 과정에서 떼어낸 함수\n
        일반적으로 내가 호출 X
        """

        result = {}
        result["id"] = item["id"]
        result["object"] = item["object"]
        for key, value in item["properties"].items():
            type_ = value["type"]
            if hasattr(notionObject, f"get_{type_}"):
                result[key] = getattr(notionObject, f"get_{type_}")(value)
            
        return result