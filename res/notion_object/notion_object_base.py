

from ..utill.register import InstanceRegister


class NotionObjectBase:

    def object(self, *value) -> dict:
        return {}
    def get(self, value):
        pass

notion_object_instance_register = InstanceRegister[str, NotionObjectBase] ()


@notion_object_instance_register("title")
class TitleObject(NotionObjectBase):
    def object(self, value: str | None) -> dict:
        """타이틀"""
        payload = {}
        if isinstance(value, str):
            payload = { "title": [ { "text": { "content": value }, "type": "text" } ], "type": "title" }
        elif value is None:
            payload = { "title": [], "type": "title" }
        return payload

    def get(self, value: dict) -> str | None:
        if len(value["title"]) == 0:
            return None
        return value["title"][0]["plain_text"]


@notion_object_instance_register("date")
class DateObject(NotionObjectBase):
    def object(self, start: str | None, end: str | None) -> dict:
        """날짜 ex)'2022-08-08'"""
        payload = {}
        if isinstance(start, str):
            payload = { "date": { "start": start, "end": end }, "type": "date" }
        elif start is None:
            payload = { "date": None, "type": "date" }
        return payload

    def get(self, value: dict) -> str | dict | None:
        if value["date"] is None:
            return None
        return {
            "start": value["date"]["start"],
            "end": value["date"]["end"]
        }

@notion_object_instance_register("text")
class TextObject(NotionObjectBase):
    def object(self, value: str | None) -> dict:
        """텍스트"""
        payload = {}
        if isinstance(value, str):
            payload = { "rich_text": [ { "text": { "content": value }, "type": "text" } ] }
        elif value is None:
            payload = { "rich_text": [] }
        return payload
    def get(self, value: dict) -> str | None:
        type_ = value["type"]
        if len(value[type_]) == 0:
            return None
        return value[type_][0]["plain_text"]
        return None   if len(value[type_]) == 0   else value[type_][0]["plain_text"]


@notion_object_instance_register("rich_text")
class RichTextObject(NotionObjectBase):
    def object(self, value: str | None) -> dict:
        return TextObject().object(value)
    def get(self, value: dict) -> str | None:
        return TextObject().get(value)

@notion_object_instance_register("paragraph")
class ParagraphObject(NotionObjectBase):
    def object(self, value: str | None) -> dict:
        return TextObject().object(value)
    def get_paragraph(self, value: dict) -> str | None:
        return Heading3Object().get(value)

@notion_object_instance_register("heading1")
class Heading1Object(NotionObjectBase):
    def object(self, value: str | None) -> dict:
        return TextObject().object(value)
    def get(self, value: dict) -> str | None:
        return Heading3Object().get(value)

@notion_object_instance_register("heading2")
class Heading2Object(NotionObjectBase):
    def object(self, value: str | None) -> dict:
        return TextObject().object(value)
    def get(self, value: dict) -> str | None:
        return Heading3Object().get(value)

@notion_object_instance_register("heading3")
class Heading3Object(NotionObjectBase):
    def object(self, value: str | None) -> dict:
        return TextObject().object(value)
    def get(self, value: dict) -> str | None:
        type_ = value["type"]
        if len(value[type_]) == 0:
            return None
        value[type_] = value[type_]["rich_text"]
        return TextObject().get(value)


@notion_object_instance_register("number")
class NumberObject(NotionObjectBase):
    def object(self, value: float | None) -> dict:
        """숫자"""
        return { "number": value, "type": "number" }

    def get(self, value: dict) -> float | None:
        return value["number"]


@notion_object_instance_register("select")
class SelectObject(NotionObjectBase):
    def object(self, value: str | None) -> dict:
        """선택"""
        payload = {}
        if isinstance(value, str):
            payload = { "select": {"name": value}, "type": "select" }
        elif value is None:
            payload = { "select": None }
        return payload

    def get(self, value: dict) -> str | None:
        if value["select"] is None:
            return None
        return value["select"]["name"]

@notion_object_instance_register("checkbox")
class CheckboxObject(NotionObjectBase):
    def object(self, value: bool) -> dict:
        """체크박스"""
        return { "checkbox": value, "type": "checkbox" }

    def get(self, value: dict) -> bool:
        return value["checkbox"]

@notion_object_instance_register("email")
class EmailObject(NotionObjectBase):
    def object(self, value: str | None):
        """이메일"""
        return { "email": value, "type": "email" }

    def get(self, value: dict) -> str | None:
        return value["email"]

@notion_object_instance_register("phone_number")
class Phone_numberObject(NotionObjectBase):
    def object(self, value: str | None) -> dict:
        """전화번호 그런데 아무거나 다 적히긴 함"""
        return { "phone_number": value, "type": "phone_number" }

    def get(self, value: dict) -> str | None:
        return value["phone_number"]

@notion_object_instance_register("url")
class UrlObject(NotionObjectBase):
    def object(self, value: str | None) -> dict:
        """URL"""
        return { "url": value, "type": "url" }

    def get(self, value: dict) -> str | None:
        return value["url"]

@notion_object_instance_register("bookmark")
class BookmarkObject(NotionObjectBase):
    def object(self, value: str | None) -> dict:
        """bookmark"""
        # 북마크에 url 타입 있으면 안댐 { "url": value, "type": "url" } 이렇게 안댐
        return { "url": value }

    def get(self, value: dict) -> str | None:
        return value["bookmark"]["url"]

@notion_object_instance_register("code")
class CodeObject(NotionObjectBase):
    def object(self, value: str | None) -> dict:
        """code"""
        return TextObject().object(value)

    def get(self, value: dict) -> dict | None:
        type_ = value["type"]
        if len(value[type_]["rich_text"]) == 0:
            return None
        return {
            "code": value[type_]["rich_text"][0]["plain_text"],
            "language": value[type_]["language"]
        }
        # return Text().get_text(value[type_])


@notion_object_instance_register("file")
class FileObject(NotionObjectBase):
    """파일은 노션 api 로 올릴 수 없음!"""
    def object(self, value: dict | None) -> dict:
        raise NotImplementedError("노션 api 에서 파일 못올림!!!.")

    def get(self, value: dict) -> dict | None:
        if not value["file"]:
            return None
        result = {
            "name": value["file"]["name"],
            "file": value["file"]["file"]["url"]
        }
        return result


@notion_object_instance_register("files")
class FilesObject(NotionObjectBase):
    """파일은 노션 api 로 올릴 수 없음!"""
    def object(self, value: dict | None) -> dict:
        raise NotImplementedError("노션 api 에서 파일 못올림!!!.")
    def get(self, value: dict) -> dict | None:
        if not value["files"]:
            return None
        result = {
            "name": value["files"][0]["name"],
            "file": value["files"][0]["file"]["url"]
        }
        return result
