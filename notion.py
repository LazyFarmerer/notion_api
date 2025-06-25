from typing import Optional
import requests

from .parent.parent import NotionParent, Read, Write, Update, Remove
from .notion_object.notion_object import DatabaseObject, PageObject, BlockObject


class Notion:
    """
    ### Notion 클래스
    database - 데이터베이스 실행을 위한 클래스
    page - 페이지 실행을 위한 클래스
    block - 블록 실행을 위한 클래스

    parameter
            api_key: 노션 api 키
            database_id: 노션 데이터베이스 id
    """
    @classmethod
    def database(cls, api_key: str, database_id: str):
        """
        ```
        write()              # 새로운 데이터 작성
        read()               # 기존 데이터들 불러오기
        update()             # 선택한 속성 업데이트
        remove()             # 선택한 속성 삭제
        find_page_id()       # 특정 속성 선택
        update_properties()  # 속성 이름 바꾸거나 지우기. 쓰일 일 없을놈
        ```
        """
        return NotionDatabase(api_key, database_id)
    @classmethod
    def page(cls, api_key: str, page_id: str):
        """
        ```
        write()              # 새로운 데이터 작성
        read()               # 기존 데이터들 불러오기
        ```
        """
        return NotionPage(api_key, page_id)
    @classmethod
    def block(cls, api_key: str, block_id: str):
        """
        ```
        read()               # 기존 데이터들 불러오기
        update()             # 선택한 속성 업데이트
        remove()             # 선택한 속성 삭제
        ```
        """
        return NotionBlock(api_key, block_id)


class NotionDatabase(NotionParent, Write, Read, Update, Remove):
    def __init__(self, key: str, DB_id: str):
        super().__init__(key, DB_id)
        self._object = DatabaseObject()
        self.payload = { "properties": {} }
        self._selected_page_id = ""

    def read(self, sorts=None, filter_=None):
        "DB 정보 가져오기"
        url = f"https://api.notion.com/v1/databases/{self.id}/query"
        headers = self._add_headers("2022-06-28")

        payload = { "page_size": 100 }
        if not sorts is None:
            payload["sorts"] = sorts
        if not filter_ is None:
            payload["filter"] = filter_

        response = requests.post(url, json=payload, headers=headers)
        self.original_data = response.json()
        self.datas = self._data_parser.parse_database(response.json(), self.datas, self._object)
        return self

    def write(self):
        "DB에 작성하기"
        url = "https://api.notion.com/v1/pages"
        headers = self._add_headers("2022-06-28")

        self.payload["parent"] = {"database_id": self.id}

        response = requests.post(url, json=self.payload, headers=headers)
        self.original_data = response.json()
        self.datas = self._data_parser.parse_database(response.json(), self.datas, self._object)
        return self

    def find_page_id(self, properties: str="", name: str = "", id_:str=""):
        """
        parameter
            properties: 기존 속성의 이름
            name: 이름
            id_: 기존 속성의 id
        """
        if (properties and name and id_):
            raise ValueError("\n뭔가 하나는 입력해야 함")

        page_id = ""

        if id_ != "":
            page_id = id_
        else:
            for item in self.datas:
                if item[properties] == name:
                    page_id = item["id"]
                    break
        
        if page_id == "":
            raise ValueError("\n해당 정보를 찾을 수 없음")

        self._selected_page_id = page_id
        return self

    def update_properties(self, properties: str, new_name: Optional[str]):
        """
        #### 페이지 속성 업데이트
        ##### 데이터베이스 속성을 제거하려면 속성 개체를 None로 설정합니다.
        parameter
            properties: 기존 속성의 이름 또는 id\n
            new_name: 새로운 이름
        """
        url = f"https://api.notion.com/v1/databases/{self.id}"
        headers = self._add_headers("2022-06-28")

        new_name_ = None if new_name is None else {"name": new_name}
        payload = {
            "properties": {
                properties: new_name_
            }
        }
        response = requests.patch(url, json=payload, headers=headers)
        self.datas = self._data_parser.parse_database(response.json(), self.datas, self._object)
        return self

    def update(self):
        "데이터베이스의 부분을 업데이트 합니다"

        if self._selected_page_id == "":
            raise ValueError("\n페이지 id 값 없음")

        url = f"https://api.notion.com/v1/pages/{self._selected_page_id}"
        headers = self._add_headers("2022-06-28")

        payload = self.payload

        response = requests.patch(url, json=payload, headers=headers)
        self.original_data = response.json()
        self.datas = self._data_parser.parse_database(response.json(), self.datas, self._object)
        return self

    def remove(self):
        "데이터베이스의 부분을 삭제 합니다"

        if self._selected_page_id == "":
            raise ValueError("\n페이지 id 값 없음")

        url = f"https://api.notion.com/v1/pages/{self._selected_page_id}"
        payload = {
            "archived": True
        }
        headers = self._add_headers("2022-06-28")

        response = requests.patch(url, json=payload, headers=headers)
        self.original_data = response.json()
        self.datas = self._data_parser.parse_database(response.json(), self.datas, self._object)
        return self

    def title(self, propertiesName: str, value: Optional[str]):
        "타이틀"
        payload = self._object.title(value)
        self.payload["properties"][propertiesName] = payload
        return self
    def date(self, propertiesName: str, start: Optional[str], end: Optional[str] = None):
        """
        날짜 ex)'2022-08-08' 아니면 '2022-08-08T09:45' 이런식으로\n
        end 날짜 똑같음
        """
        payload = self._object.date(start, end)
        self.payload["properties"][propertiesName] = payload
        return self
    def text(self, propertiesName: str, value: Optional[str]):
        "텍스트"
        payload = self._object.text(value)
        self.payload["properties"][propertiesName] = payload
        return self
    def number(self, propertiesName: str, value: Optional[int]):
        "숫자"
        self.payload["properties"][propertiesName] = self._object.number(value)
        return self
    def select(self, propertiesName: str, value: Optional[str]):
        "선택"
        payload = self._object.select(value)
        self.payload["properties"][propertiesName] = payload
        return self
    def checkbox(self, propertiesName: str, value: bool):
        "체크박스"
        self.payload["properties"][propertiesName] = self._object.checkbox(value)
        return self
    def email(self, propertiesName: str, value: bool):
        "이메일"
        self.payload["properties"][propertiesName] = self._object.email(value)
        return self
    def phone_number(self, propertiesName: str, value: Optional[str]):
        "전화번호 그런데 아무거나 다 적히긴 함"
        self.payload["properties"][propertiesName] = self._object.phone_number(value)
        return self
    def url(self, propertiesName: str, value: Optional[str]):
        "URL"
        self.payload["properties"][propertiesName] = self._object.url(value)
        return self


class NotionPage(NotionParent, Write, Read):
    def __init__(self, key: str, page_id: str):
        super().__init__(key, page_id)
        self._object = PageObject()
        self.children: list[dict] = []

    def write(self):
        url = f"https://api.notion.com/v1/blocks/{self.id}/children"
        headers = self._add_headers("2022-06-28")

        data = {
            "children": self.children
        }

        response = requests.patch(url, headers=headers, json=data)
        self.original_data = response.json()
        self.datas = self._data_parser.parse_page(response.json(), self.datas, self._object)
        return self

    def read(self):
        url = f"https://api.notion.com/v1/blocks/{self.id}/children?page_size=100"
        headers = self._add_headers("2022-06-28")

        response = requests.get(url, headers=headers)
        self.original_data = response.json()
        self.datas = self._data_parser.parse_page(response.json(), self.datas, self._object)
        # self.datas = self._data_parser.parse_response(response.json(), self.datas, self._object)
        return self

    def text(self, value: Optional[str]):
        "텍스트"
        properties = {
            "object": "block",
            "type": "paragraph",
            "paragraph": self._object.text(value)
        }
        self.children.append(properties)
        return self

    def bookmark(self, value: Optional[str]):
        "북마크"
        properties = {
            "object": "block",
            "type": "bookmark",
            "bookmark": self._object.bookmark(value)
        }
        self.children.append(properties)
        return self

    def code(self, value: Optional[str], language: str):
        "코드, 언어 안넣으면 오류와 함께 가능한 언어들 모두 표시 ㅋ"
        code = self._object.code(value)
        code["language"] = language
        properties = {
            "object": "block",
            "type": "code",
            "code": code
        }
        self.children.append(properties)
        return self


class NotionBlock(NotionParent, Read, Update, Remove):
    def __init__(self, key: str, block_id: str):
        super().__init__(key, block_id)
        self._object = BlockObject()
        self.payload = {}

    def read(self):
        url = f"https://api.notion.com/v1/blocks/{self.id}"
        headers = self._add_headers("2022-06-28")

        response = requests.patch(url, headers=headers)
        self.original_data = response.json()
        self.datas = self._data_parser.parse_block(response.json(), self.datas, self._object)
        return self

    def update(self):
        "블록 유형은 변경 불가능 ex) 텍스트블럭을 코드블럭으로 변환 X"
        url = f"https://api.notion.com/v1/blocks/{self.id}"
        headers = self._add_headers("2022-06-28")

        data = self.payload

        response = requests.patch(url, headers=headers, json=data)
        self.original_data = response.json()
        self.datas = self._data_parser.parse_block(response.json(), self.datas, self._object)
        return self

    def remove(self):
        url = f"https://api.notion.com/v1/blocks/{self.id}"
        payload = {
            "archived": True
        }
        headers = self._add_headers("2022-06-28")

        response = requests.patch(url, json=payload, headers=headers)
        self.original_data = response.json()
        self.datas = self._data_parser.parse_database(response.json(), self.datas, self._object)
        return self

    def text(self, value: Optional[str]):
        "텍스트"
        properties = {
            "object": "block",
            "type": "paragraph",
            "paragraph": self._object.text(value)
        }
        self.payload = properties
        return self

    def code(self, value: Optional[str], language: str):
        "코드, 언어 안넣으면 오류와 함께 가능한 언어들 모두 표시 ㅋ"
        code = self._object.code(value)
        code["language"] = language
        properties = {
            "object": "block",
            "type": "code",
            "code": code
        }
        self.payload = properties
        return self
