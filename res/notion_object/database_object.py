

from typing import Any

from ..abstract.value import DictValueBase


# 관련 정보는 여기
# 여기를 기준으로 만들어짐
# https://developers.notion.com/reference/property-object

class CheckboxDatabaseObject:
    def object(self, value: bool) -> dict:
        return { "checkbox": value, "type": "checkbox" }

    def get(self, value: dict) -> bool:
        return value["checkbox"]


# class CreatedByDatabaseObject: ...
# class CreatedTimeDatabaseObject: ...


class DateDatabaseObject:
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


class EmailDatabaseObject:
    def object(self, value: str | None):
        return { "email": value, "type": "email" }

    def get(self, value: dict) -> str | None:
        return value["email"]


class FilesDatabaseObject:
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


class FormulaDatabaseObject:
    """ex) {{notion:block_property:BtVS:00000000-0000-0000-0000-000000000000:8994905a-074a-415f-9bcf-d1f8b4fa38e4}}/2"""
    # 와 이게 뭐고 대충 어떤 값에서 / 2 인듯????
    def object(self, value: str | None) -> dict:
        print("Formula 정보")
        print(value)
        return { "formula": { "expression": value }, "type": "formula" }

    def get(self, value: dict) -> dict:
        return value["formula"]

# {'id': 'mFdH', 'type': 'formula', 'formula': {'type': 'boolean', 'boolean': False}}

# class LastEditedByDatabaseObject: ...
# class LastEditedTimeDatabaseObject: ...


class MultiSelectDatabaseObject:
    def object(self, value: str | None) -> dict:
        print("MultiSelect 정보")
        print(value)
        return {}
    def get(self, value: dict) -> list:
        if len(value["multi_select"]) == 0:
            return []

        return [ select["name"] for select in value["multi_select"] ]


class NumberDatabaseObject:
    def object(self, value: float | None) -> dict:
        return { "number": value, "type": "number" }

    def get(self, value: Any) -> float | None:
        return value["number"]


class PeopleDatabaseObject:
    def object(self, value: float | None) -> dict:
        print("People 정보")
        print(value)
        return {}
    def get(self, value: dict) -> list:
        if len(value["people"]) == 0:
            return []

        return [ people["name"] for people in value["people"] ]


class PhoneNumberDatabaseObject:
    def object(self, value: str | None) -> dict:
        return { "phone_number": value, "type": "phone_number" }

    def get(self, value: dict) -> str | None:
        return value["phone_number"]


class PlaceDatabaseObject:
    def object(self, value: Any | None) -> dict:
        print("Place 정보")
        print(value)
        return {}
    def get(self, value: dict) -> dict | None:
        if value["place"] is None:
            return None

        return {
            "lat": value["place"]["lat"],
            "lon": value["place"]["lon"],
            "name": value["place"]["name"],
            "address": value["place"]["address"],
        }


class RelationDatabaseObject:
    def object(self, value: Any | None) -> dict:
        print("Relation 정보")
        print(value)
        return {}
    def get(self, value: dict) -> list | None:
        if len(value["relation"]) == 0:
            return None
        # value["relation"] 안에 { "id": "..." } 밖에 없음
        return [ relation["id"] for relation in value["relation"] ]


class RichTextDatabaseObject:
    def object(self, value: str | None) -> dict:
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


class RollupDatabaseObject:
    def object(self, value: str | None) -> dict:
        print("Rollup 정보")
        print(value)
        return {}
    def get(self, value: dict) -> Any:
        print("Rollup 정보")
        print(value)
        array: list = value["rollup"]["array"]
        if len(array) == 0:
            return None
        
        type_ = array[0]["type"]
        return parser_database_object_data(type_, array[0])


class SelectDatabaseObject:
    def object(self, value: str | None) -> dict:
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


class StatusDatabaseObject:
    def object(self, value: str | None) -> dict:
        print("Status 정보")
        print(value)
        return {}
    def get(self, value: dict) -> dict:
        # 항상 값이 존재 (기본값이 있음)
        return value["status"]["name"]


class TitleDatabaseObject:
    def object(self, value: str | None) -> dict:
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


class UrlDatabaseObject:
    def object(self, value: str | None) -> dict:
        """URL"""
        return { "url": value, "type": "url" }

    def get(self, value: dict) -> str | None:
        return value["url"]


class UniqueIDDatabaseObject:
    def object(self, value: str | None) -> dict:
        print("UniqueID 정보")
        print(value)
        return {}
    def get(self, value: dict) -> int:
        return value["unique_id"]["number"]


class ButtonDatabaseObject:
    def object(self, value: str | None) -> dict:
        print("Button 정보")
        print(value)
        return {}
    def get(self, value: dict) -> dict:
        return value["button"]


class DatabaseObject(DictValueBase):
    def checkbox(self, properties: str, value: bool):
        """체크박스"""
        result = { properties : CheckboxDatabaseObject().object(value) }
        self._value.update(result)
        return self
    
    # def created_by(self, properties: str): ...
    # def created_time(self, properties: str): ...

    def date(self, properties: str, start: str | None, end: str | None=None):
        """날짜 ex)'2022-08-08'"""
        result = { properties : DateDatabaseObject().object(start, end) }
        self._value.update(result)
        return self

    def email(self, properties: str, value: str | None):
        """이메일"""
        result = { properties : EmailDatabaseObject().object(value) }
        self._value.update(result)
        return self

    def files(self, properties: str, value: dict | None):
        """파일은 노션 api 로 올릴 수 없음!"""
        result = { properties : FilesDatabaseObject().object(value) }
        self._value.update(result)
        return self

    def formula(self, properties: str, value: str | None):
        result = { properties : FormulaDatabaseObject().object(value) }
        self._value.update(result)
        return self

    # def last_edited_by(self, properties: str): ...
    # def last_edited_time(self, properties: str): ...

    def multi_select(self, properties: str, value: Any | None):
        result = { properties : MultiSelectDatabaseObject().object(value) }
        self._value.update(result)
        return self

    def number(self, properties: str, value: float | None):
        """숫자"""
        result = { properties : NumberDatabaseObject().object(value) }
        self._value.update(result)
        return self

    def people(self, properties: str, value: Any | None):
        result = { properties : PeopleDatabaseObject().object(value) }
        self._value.update(result)
        return self

    def phone_number(self, properties: str, value: str | None):
        """전화번호 그런데 아무거나 다 적히긴 함"""
        result = { properties : PhoneNumberDatabaseObject().object(value) }
        self._value.update(result)
        return self

    def place(self, properties: str, value: Any | None):
        result = { properties : PlaceDatabaseObject().object(value) }
        self._value.update(result)
        return self

    def relation(self, properties: str, value: Any | None):
        result = { properties : RelationDatabaseObject().object(value) }
        self._value.update(result)
        return self

    def text(self, properties: str, value: str | None):
        """텍스트"""
        result = { properties : RichTextDatabaseObject().object(value) }
        self._value.update(result)
        return self

    def rollup(self, properties: str, value: str | None):
        result = { properties : RollupDatabaseObject().object(value) }
        self._value.update(result)
        return self

    def select(self, properties: str, value: str | None):
        """선택"""
        result = { properties : SelectDatabaseObject().object(value) }
        self._value.update(result)
        return self

    def status(self, properties: str, value: str | None):
        result = { properties : StatusDatabaseObject().object(value) }
        self._value.update(result)
        return self

    def title(self, properties: str, value: str | None):
        """타이틀"""
        result = { properties : TitleDatabaseObject().object(value) }
        self._value.update(result)
        return self

    def url(self, properties: str, value: str | None):
        """URL"""
        result = { properties : UrlDatabaseObject().object(value) }
        self._value.update(result)
        return self

    def unique_id(self, properties: str, value: str | None):
        result = { properties : UniqueIDDatabaseObject().object(value) }
        self._value.update(result)
        return self

    def button(self, properties: str, value: str | None):
        result = { properties : ButtonDatabaseObject().object(value) }
        self._value.update(result)
        return self


def parser_database_object_data(type_: str, data: dict):

    match type_:
        case "checkbox":
            return CheckboxDatabaseObject().get(data)
        case "created_by":
            return # CreatedByDatabaseObject().get(data)
        case "created_time":
            return # CreatedTimeDatabaseObject().get(data)
        case "date":
            return DateDatabaseObject().get(data)
        case "email":
            return EmailDatabaseObject().get(data)
        case "files":
            return FilesDatabaseObject().get(data)
        case "formula":
            return FormulaDatabaseObject().get(data)
        case "last_edited_by":
            return # LastEditedByDatabaseObject().get(data)
        case "last_edited_time":
            return # LastEditedTimeDatabaseObject().get(data)
        case "multi_select":
            return MultiSelectDatabaseObject().get(data)
        case "number":
            return NumberDatabaseObject().get(data)
        case "people":
            return PeopleDatabaseObject().get(data)
        case "phone_number":
            return PhoneNumberDatabaseObject().get(data)
        case "place":
            return PlaceDatabaseObject().get(data)
        case "relation":
            return RelationDatabaseObject().get(data)
        case "rich_text":
            return RichTextDatabaseObject().get(data)
        case "rollup":
            return RollupDatabaseObject().get(data)
        case "select":
            return SelectDatabaseObject().get(data)
        case "status":
            return StatusDatabaseObject().get(data)
        case "title":
            return TitleDatabaseObject().get(data)
        case "url":
            return UrlDatabaseObject().get(data)
        case "unique_id":
            return UniqueIDDatabaseObject().get(data)
        case "button":
            return ButtonDatabaseObject().get(data)
        case _:
            print(f"이건 무슨 타입?: {type_}")
            print(f"이건 그래서?: {data}")
            return {}

