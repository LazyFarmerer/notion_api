from typing import Optional, Union, List


class NotionObject:
    pass


class Title(NotionObject):
    def title(self, value: Optional[str]) -> dict:
        "타이틀"
        payload = {}
        if isinstance(value, str):
            payload = { "title": [ { "text": { "content": value }, "type": "text" } ], "type": "title" }
        elif value is None:
            payload = { "title": [], "type": "title" }
        return payload

    def get_title(self, value: dict) -> Optional[str]:
        if len(value["title"]) == 0:
            return None
        return value["title"][0]["plain_text"]


class Date(NotionObject):
    def date(self, value: Optional[str]) -> dict:
        "날짜 ex)'2022-08-08'"
        payload = {}
        if isinstance(value, str):
            payload = { "date": { "start": value }, "type": "date" }
        elif value is None:
            payload = { "date": None, "type": "date" }
        return payload

    def get_date(self, value: dict) -> Union[str, dict, None]:
        if value["date"] is None:
            return None
        if value["date"].get("end"):
            return value["date"]
        return value["date"]["start"]


class Text(NotionObject):
    def rich_text(self, value: Optional[str]) -> dict:
        return self.text(value)
    def text(self, value: Optional[str]) -> dict:
        "텍스트"
        payload = {}
        if isinstance(value, str):
            payload = { "rich_text": [ { "text": { "content": value }, "type": "text" } ] }
        elif value is None:
            payload = { "rich_text": [] }
        return payload

    def get_paragraph(self, value: dict) -> Optional[str]:
        return self.get_heading_3(value)
    def get_heading_1(self, value: dict) -> Optional[str]:
        return self.get_heading_3(value)
    def get_heading_2(self, value: dict) -> Optional[str]:
        return self.get_heading_3(value)
    def get_heading_3(self, value: dict) -> Optional[str]:
        type_ = value["type"]
        if len(value[type_]) == 0:
            return None
        value[type_] = value[type_]["rich_text"]
        return self.get_text(value)

    def get_rich_text(self, value: dict) -> Optional[str]:
        return self.get_text(value)
    def get_text(self, value: dict) -> Optional[str]:
        type_ = value["type"]
        if len(value[type_]) == 0:
            return None
        return value[type_][0]["plain_text"]
        return None   if len(value[type_]) == 0   else value[type_][0]["plain_text"]

class Number(NotionObject):
    def number(self, value: Optional[int]) -> dict:
        "숫자"
        return { "number": value, "type": "number" }

    def get_number(self, value: dict) -> Optional[float]:
        return value["number"]


class Select(NotionObject):
    def select(self, value: Optional[str]) -> dict:
        "선택"
        payload = {}
        if isinstance(value, str):
            payload = { "select": {"name": value}, "type": "select" }
        elif value is None:
            payload = { "select": None }
        return payload

    def get_select(self, value: dict) -> Optional[str]:
        if value["select"] is None:
            return None
        return value["select"]["name"]


class Checkbox(NotionObject):
    def checkbox(self, value: bool) -> dict:
        "체크박스"
        return { "checkbox": value, "type": "checkbox" }

    def get_checkbox(self, value: dict) -> bool:
        return value["checkbox"]


class Email(NotionObject):
    def email(self, value: bool):
        "이메일"
        return { "email": value, "type": "email" }

    def get_email(self, value: dict) -> Optional[str]:
        return value["email"]


class Phone_number(NotionObject):
    def phone_number(self, value: Optional[str]) -> dict:
        "전화번호 그런데 아무거나 다 적히긴 함"
        return { "phone_number": value, "type": "phone_number" }

    def get_phone_number(self, value: dict) -> Optional[str]:
        return value["phone_number"]


class Url(NotionObject):
    def url(self, value: Optional[str]) -> dict:
        "URL"
        return { "url": value, "type": "url" }

    def get_url(self, value: dict) -> Optional[str]:
        return value["url"]


class Bookmark(NotionObject):
    def bookmark(self, value: Optional[str]) -> dict:
        "bookmark"
        # 북마크에 url 타입 있으면 안댐 { "url": value, "type": "url" } 이렇게 안댐
        return { "url": value }

    def get_bookmark(self, value: dict) -> Optional[str]:
        return value["bookmark"]["url"]


class Code(NotionObject):
    def code(self, value: Optional[str]) -> dict:
        "code"
        return Text().text(value)

    def get_code(self, value: dict) -> Optional[str]:
        type_ = value["type"]
        if len(value[type_]["rich_text"]) == 0:
            return None
        return value[type_]["rich_text"][0]["plain_text"]
        # return Text().get_text(value[type_])


class File(NotionObject):
    def files(self, value: Optional[dict]) -> dict:
        raise NotImplementedError("노션 api 에서 파일 못올림!!!.")
    def file(self, value: Optional[dict]) -> dict:
        raise NotImplementedError("노션 api 에서 파일 못올림!!!.")

    def get_files(self, value: dict) -> Optional[dict]:
        if not value["files"]:
            return None
        result = {
            "name": value["files"][0]["name"],
            "file": value["files"][0]["file"]["url"]
        }
        return result
    def get_file(self, value: dict) -> Optional[dict]:
        if not value["file"]:
            return None
        result = {
            "name": value["file"]["name"],
            "file": value["file"]["file"]["url"]
        }
        return result


class DatabaseObject(Title, Date, Text, Number, Select, Checkbox, Email, Phone_number, Url, File):
    pass


class PageObject(Text, Bookmark, Code, File):
    pass

class BlockObject(Text, Code, File):
    pass

