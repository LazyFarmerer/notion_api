from typing import Optional, List
import json
import requests

class Notion:
    """
    ### Notion 클래스
    노션의 DB 실행을 위한 클래스

    메서드 종류
    ```
    DB_load()            # 기존 데이터들 불러오기
    DB_write()           # 새로운 데이터 작성
    select_page_id()     # 특정 속성 선택
    update_page()        # 선택한 속성 업데이트
    update_properties()  # 속성 이름 바꾸거나 지우기. 쓰일 일 없을놈

    "데이터 작성 또는 업데이트 시 사용하는 메서드"
    title(), date(), text(), number(), select(), checkbox(), email(), phone_number()
    ```

    ### Notion.Option() 클래스
    DB_load() 메서드 사용 시 sorts, filter 사용하기 위한 옵션 클래스
    """
    class Option:
        오름차순 = "ascending"
        내림차순 = "descending"
        @staticmethod
        def sorts(property_: str ="", direction: str =""):
            """
            DB_load() 메서드 옵션용으로 사용하세요\n
            property: 정렬 기준, 무엇을 기준으로 정렬 할것인지\n
            direction: 오름차순 or 내림차순 선택
            """
            if not (property_ or direction):
                raise ValueError("\n'입력할거면 둘 다 입력하시오")

            result = [ { } ]
            if property_ != "":
                result[0]["property"] = property_
            if direction != "":
                if direction in ["ascending", "descending"]:
                    result[0]["direction"] = direction
                else:
                    raise ValueError("\n'ascending', 'descending' 둘 중 하나만 사용하기\nOption.오름차순, Option.내림차순 사용 가능")

            return result

        @staticmethod
        def filter(property_: str ="", query: str =""):
            """
            DB_load() 메서드 옵션용으로 사용하세요\n
            property: 필터 기준, 무엇을 기준으로 필터 할것인지\n
            query: 검색할 일부
            """
            if not (property_ or query):
                raise ValueError("\n'입력할거면 둘 다 입력하시오")

            result = {
                "property": property_,
                "rich_text": {
                    "contains": query
                }
            }

            return result

    def __init__(self, key: str, DB_id: str):
        self.key = key
        self.DB_id = DB_id
        self.payload = {}
        self.datas: List[dict] = []

        self.__selectPageId = ""

    def DB_load(self, sorts=None, filter_=None):
        "DB 정보 가져오기"
        url = f"https://api.notion.com/v1/databases/{self.DB_id}/query"
        headers = self.__add_headers("2022-06-28")

        payload = { "page_size": 100 }
        if not sorts is None:
            payload["sorts"] = sorts
        if not filter_ is None:
            payload["filter"] = filter_

        response = requests.post(url, json=payload, headers=headers)
        # print(response.text)
        self.datas = self.__precleaning(response.json())
        return self

    def DB_write(self):
        "DB에 작성하기"
        url = "https://api.notion.com/v1/pages"
        headers = self.__add_headers("2022-06-28")

        self.payload["parent"] = {"database_id": self.DB_id}

        response = requests.post(url, json=self.payload, headers=headers)
        self.datas = self.__precleaning(response.json())
        return self

    def select_page_id(self, properties: str="", name: str = "", id_:str=""):
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

        self.__selectPageId = page_id
        return self

    def update_properties(self, properties: str, new_name: Optional[str]):
        """
        #### 페이지 속성 업데이트
        ##### 데이터베이스 속성을 제거하려면 속성 개체를 None로 설정합니다.
        parameter
            properties: 기존 속성의 이름 또는 id\n
            new_name: 새로운 이름
        """
        url = f"https://api.notion.com/v1/databases/{self.DB_id}"
        headers = self.__add_headers("2022-06-28")

        new_name_ = None if new_name is None else {"name": new_name}
        payload = {
            "properties": {
                properties: new_name_
            }
        }
        response = requests.patch(url, json=payload, headers=headers)
        self.datas = self.__precleaning(response.json())
        return self
    
    def update_page(self):
        "데이터베이스의 부분을 업데이트 합니다"

        if self.__selectPageId == "":
            raise ValueError("\n페이지 id 값 없음")

        url = f"https://api.notion.com/v1/pages/{self.__selectPageId}"
        headers = self.__add_headers("2022-06-28")

        payload = self.payload

        response = requests.patch(url, json=payload, headers=headers)
        self.datas = self.__precleaning(response.json())
        return self

    def remove_page(self):
        "데이터베이스의 부분을 삭제 합니다"

        if self.__selectPageId == "":
            raise ValueError("\n페이지 id 값 없음")

        url = f"https://api.notion.com/v1/pages/{self.__selectPageId}"
        payload = {
            "archived": True
        }
        headers = self.__add_headers("2022-06-28")

        response = requests.patch(url, json=payload, headers=headers)
        self.datas = self.__precleaning(response.json())
        return self

    def title(self, propertiesName: str, value: Optional[str]):
        "타이틀"
        self.__check_properties()
        payload = {}
        if isinstance(value, str):
            payload = { "title": [ { "text": { "content": value } } ] }
        elif value is None:
            payload = { "title": [] }
        self.payload["properties"][propertiesName] = payload
        return self
    def date(self, propertiesName: str, value: Optional[str]):
        "날짜 ex)'2022-08-08'"
        self.__check_properties()
        payload = {}
        if isinstance(value, str):
            payload = { "date": { "start": value } }
        elif value is None:
            payload = { "date": None }

        self.payload["properties"][propertiesName] = payload
        return self
    def text(self, propertiesName: str, value: Optional[str]):
        "텍스트"
        self.__check_properties()
        payload = {}
        if isinstance(value, str):
            payload = { "rich_text": [ { "text": { "content": value } } ] }
        elif value is None:
            payload = { "rich_text": [] }
        self.payload["properties"][propertiesName] = payload
        return self
    def number(self, propertiesName: str, value: Optional[int]):
        "숫자"
        self.__check_properties()
        self.payload["properties"][propertiesName] = { "number": value }
        return self
    def select(self, propertiesName: str, value: Optional[str]):
        "선택"
        self.__check_properties()
        payload = {}
        if isinstance(value, str):
            payload = { "select": {"name": value} }
        elif value is None:
            payload = { "select": None }
        self.payload["properties"][propertiesName] = payload

        return self
    def checkbox(self, propertiesName: str, value: bool):
        "체크박스"
        self.__check_properties()
        self.payload["properties"][propertiesName] = { "checkbox": value }
        return self
    def email(self, propertiesName: str, value: bool):
        "이메일"
        self.__check_properties()
        self.payload["properties"][propertiesName] = { "email": value }
        return self
    def phone_number(self, propertiesName: str, value: Optional[str]):
        "전화번호 그런데 아무거나 다 적히긴 함"
        self.__check_properties()
        self.payload["properties"][propertiesName] = { "phone_number": value }
        return self
    def url(self, propertiesName: str, value: Optional[str]):
        "URL"
        self.__check_properties()
        self.payload["properties"][propertiesName] = { "url": value }
        return self

    def __check_properties(self):
        if not self.payload.get("properties"):
            self.payload["properties"] = {}

    def __add_headers(self, version: str):
        "헤더에 버젼을 추가해서 리턴"
        return {
            "Accept": "application/json",
            "Notion-Version": version,
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.key}"
        }
    
    def __precleaning(self, data: dict):
        "받은 정보를 내가 보기좋게 가공"
        result = {}
        result_list: List[dict] = self.datas

        if data["object"] == "list":
            results_datas: List[dict] = data["results"]
            if results_datas is None:
                raise ValueError("\n뭐 받음???")

            for item in results_datas:
                result = self.__precleaning2(item)
                result_list.append(result)

            return result_list

        elif data["object"] == "page":
            result = self.__precleaning2(data)
            
            if len(result_list) == 0:
                result_list.append(result)
            for index, item in enumerate(result_list):
                if item["id"] == result["id"]:
                    result_list[index] = result
                    return result_list

        raise ValueError(f"\nlist 또는 page 아님. 아래는 내용\n{data}")

    def __precleaning2(self, item: dict):
        """
        __precleaning() 메서드 처리하는 과정에서 떼어낸 함수\n
        일반적으로 내가 호출 X
        """

        result = {}
        result["id"] = item["id"]
        for key, value in item["properties"].items():
            type_ = value["type"]
            if (type_ == "title") or (type_ == "rich_text"):
                if len(value[type_]) == 0:
                    result[key] = None
                else:
                    result[key] = value[type_][0]["plain_text"]
                continue
            elif type_ == "date":
                if value.get("date") is None:
                    result[key] = None
                else:
                    result[key] = value["date"]["start"]
                continue
            elif type_ == "select":
                if value.get("select") is None:
                    result[key] = None
                else:
                    result[key] = value["select"]["name"]
                continue
            elif type_ == "formula":
                if value.get("formula") is None:
                    result[key] = None
                else:
                    formula = value["formula"]
                    result[key] = formula[formula["type"]]
                continue

            result[key] = value[type_]

        return result

    def __join(self, dataList: list):
        listStr = [f"{"" if item is None else item}" for item in dataList]
        return ",".join(listStr)

    @property
    def txt(self) -> str:
        return json.dumps(self.datas)

    @property
    def csv(self) -> str:
        "csv 형식의 문자열을 반환합니다"
        datas = self.datas
        result = ""
        for i, data in enumerate(datas):
            if i == 0:
                result += self.__join(data.keys())
                result += "\n"
            result += self.__join(data.values())
            if i != len(datas)-1:
                result += "\n"
        return result

    def __repr__(self) -> str:
        return json.dumps(self.datas, ensure_ascii=False) #, indent="\t")