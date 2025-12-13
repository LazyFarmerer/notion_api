

from typing import Any

from ..res.abstract.value import DictValueBase


# 관련 정보는 여기
# 여기를 기준으로 만들어짐
# https://developers.notion.com/reference/property-object

class CheckboxDatabaseObject:
    def object(self, value: bool) -> dict:
        return { "checkbox": value, "type": "checkbox" }

    def get(self, value: dict) -> bool:
        return value["checkbox"]


class CreatedByDatabaseObject:
    def get(self, value: dict) -> bool:
        return value["created_by"]["id"]


class CreatedTimeDatabaseObject:
    def get(self, value: dict) -> bool:
        return value["created_time"]


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
    def object(self, name: str, url: str) -> dict:
        return {
            "type": "files",
            "files": [
                {
                    "name": name,
                    "external": { "url": url }
                }
            ]
        }
    def get(self, value: dict) -> dict | None:
        if not value["files"]:
            return None
        result = {
            "name": value["files"][0]["name"],
            "file": value["files"][0]["external"]["url"]
        }
        return result


class FormulaDatabaseObject:
        # 업데이트 불가능
    def get(self, value: dict) -> dict:
        return value["formula"]


class LastEditedByDatabaseObject:
    def get(self, value: dict) -> bool:
        return value["last_edited_by"]["id"]
class LastEditedTimeDatabaseObject:
    def get(self, value: dict) -> bool:
        return value["last_edited_time"]


class MultiSelectDatabaseObject:
    def object(self, value: str, *values: str) -> dict:
        result = [{ "name": value }]
        result.extend( [ { "name": value } for value in values ] )
        return { "multi_select": result, "type": "multi_select" }
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
    def object(self, id: str, *ids: str) -> dict:
        result = [{ "id": id }]
        result.extend( [ { "id": people_id } for people_id in ids ] )
        return { "people": result, "type": "people" }
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
    def object(self, id: str, *ids: str) -> dict:
        result = [{"id": id}]
        result.extend( [ { "id": relation_id } for relation_id in ids ] )
        return { "relation": result, "type": "relation" }
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
    def get(self, value: dict) -> Any:
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
        return { "status": { "name": value }, "type": "status" }
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
    def get(self, value: dict) -> int:
        return value["unique_id"]["number"]


class ButtonDatabaseObject:
    def get(self, value: dict) -> dict:
        return value["button"]


class DatabaseObject(DictValueBase):
    def checkbox(self, properties: str, value: bool):
        """체크박스가 선택되었는지(True) 또는 선택되지 않았는지(False)를 나타냅니다."""
        result = { properties : CheckboxDatabaseObject().object(value) }
        self._value.update(result)
        return self

    def date(self, properties: str, start: str | None, end: str | None=None):
        """페이지 속성 값의 가 인 경우 , 해당 속성 값에는 다음과 같은 필드를 가진 객체가 포함됩니다.
        
        예시값 "2020-12-08T12:00:00Z", "2020-12-08T12:00:00Z” """
        result = { properties : DateDatabaseObject().object(start, end) }
        self._value.update(result)
        return self

    def email(self, properties: str, value: str | None):
        """이메일 주소를 설명하는 문자열입니다."""
        result = { properties : EmailDatabaseObject().object(value) }
        self._value.update(result)
        return self

    def files(self, properties: str, name: str, url: str):
        """파일에 대한 정보를 담고 파일 이름과 url"""
        result = { properties : FilesDatabaseObject().object(name, url) }
        self._value.update(result)
        return self

    def multi_select(self, properties: str, value: str, *values: str):
        """표시되는 옵션 이름입니다"""
        result = { properties : MultiSelectDatabaseObject().object(value, *values) }
        self._value.update(result)
        return self

    def number(self, properties: str, value: float | None):
        """어떤 값을 나타내는 숫자."""
        result = { properties : NumberDatabaseObject().object(value) }
        self._value.update(result)
        return self

    def people(self, properties: str, id: str, *ids: str):
        """유저의 id 값을 넣으면 되긴 한데 구하기 쉽지 않음"""
        result = { properties : PeopleDatabaseObject().object(id, *ids) }
        self._value.update(result)
        return self

    def phone_number(self, properties: str, value: str | None):
        """전화번호를 나타내는 문자열입니다. 전화번호 형식은 지정되어 있지 않습니다."""
        result = { properties : PhoneNumberDatabaseObject().object(value) }
        self._value.update(result)
        return self

    def relation(self, properties: str, id: str, *ids: str):
        """다른 데이터베이스의 페이지 id 값을 넣어주면 됨"""
        result = { properties : RelationDatabaseObject().object(id, *ids) }
        self._value.update(result)
        return self

    def text(self, properties: str, value: str | None):
        """텍스트"""
        result = { properties : RichTextDatabaseObject().object(value) }
        self._value.update(result)
        return self

    def select(self, properties: str, value: str | None):
        """표시되는 옵션 이름입니다"""
        result = { properties : SelectDatabaseObject().object(value) }
        self._value.update(result)
        return self

    def status(self, properties: str, value: str | None):
        """표시되는 옵션 이름입니다"""
        result = { properties : StatusDatabaseObject().object(value) }
        self._value.update(result)
        return self

    def title(self, properties: str, value: str | None):
        """타이틀"""
        result = { properties : TitleDatabaseObject().object(value) }
        self._value.update(result)
        return self

    def url(self, properties: str, value: str | None):
        """웹 주소를 설명하는 문자열입니다."""
        result = { properties : UrlDatabaseObject().object(value) }
        self._value.update(result)
        return self


def parser_database_object_data(type_: str, data: dict):

    match type_:
        case "checkbox":
            return CheckboxDatabaseObject().get(data)
        case "created_by":
            return CreatedByDatabaseObject().get(data)
        case "created_time":
            return CreatedTimeDatabaseObject().get(data)
        case "date":
            return DateDatabaseObject().get(data)
        case "email":
            return EmailDatabaseObject().get(data)
        case "files":
            return FilesDatabaseObject().get(data)
        case "formula":
            return FormulaDatabaseObject().get(data)
        case "last_edited_by":
            return LastEditedByDatabaseObject().get(data)
        case "last_edited_time":
            return LastEditedTimeDatabaseObject().get(data)
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

