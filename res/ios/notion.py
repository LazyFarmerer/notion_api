

# 한줄에 때려박기

from typing import Literal, Any, overload
import sys, re
from abc import ABC, abstractmethod

import requests


class NotionBase:
    def __init__(self, api_key: str, id: str, object: str):
        self.api_key = api_key
        self.id = id
        self.object = object
        self.archived: bool = False
        """삭제했는지 에 관한 정보"""

    def _add_headers(self, version: Literal["2025-09-03", "2022-06-28"]):
        "헤더에 버젼을 추가해서 리턴"
        return {
            "Accept": "application/json",
            "Notion-Version": version,
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

class Read(ABC):
    @abstractmethod
    def read(self):
        raise NotImplementedError


class Write(ABC):
    @abstractmethod
    def write(self):
        raise NotImplementedError


class Update(ABC):
    @abstractmethod
    def update(self):
        raise NotImplementedError


class Remove(ABC):
    @abstractmethod
    def remove(self) -> bool:
        raise NotImplementedError


class DictValueBase:
    def __init__(self, value: dict | None = None) -> None:
        if value is None:
            self._value = {}
            return

        self._value = value

    @property
    def value(self) -> dict:
        return self._value


class ListValueBase:
    def __init__(self, value: list | None = None) -> None:
        if value is None:
            self._value = []
            return

        self._value = value

    @property
    def value(self) -> list:
        return self._value


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


def _return_value(property_: str, filter_name: str, field: str, value: Any) -> dict:
    return {
        "property": property_,
        filter_name: { field: value }
    }

def _camel_to_snake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class FilterBase(DictValueBase):
    def __init__(self, value: dict | None = None) -> None:
        super().__init__(value)
        class_name = self.__class__.__name__.replace("Filter", "")
        self._filter_name = _camel_to_snake(class_name)

class CheckboxFilter(FilterBase):
    def equals(self, property_: str, value: bool):
        """속성 값이 제공된 값과 정확히 일치하는지 여부를 나타냅니다.

        값이 정확히 일치하는 모든 데이터 소스 항목을 반환하거나 제외합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, value)
        self._value.update(result)
        return self

    def does_not_equal(self, property_: str, value: bool):
        """속성 값이 제공된 값과 다른지 여부를 나타냅니다.

        값에 차이가 있는 모든 데이터 소스 항목을 반환하거나 제외합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, value)
        self._value.update(result)
        return self


class DateFilter(FilterBase):
    def after(self, property_: str, value: str):
        """날짜 속성 값과 비교할 값입니다.

        날짜 속성 값이 제공된 날짜 이후인 데이터 소스 항목을 반환합니다.

        ex) "2021-05-10", "2021-05-10T12:00:00", "2021-10-15T12:00:00-07:00" """
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, value)
        self._value.update(result)
        return self

    def before(self, property_: str, value: str):
        """날짜 속성 값과 비교할 값입니다.

        날짜 속성 값이 제공된 날짜 이전인 데이터 소스 항목을 반환합니다.

        ex) "2021-05-10", "2021-05-10T12:00:00", "2021-10-15T12:00:00-07:00" """
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, value)
        self._value.update(result)
        return self

    def equals(self, property_: str, value: str):
        """날짜 속성 값과 비교할 값입니다.

        날짜 속성 값이 제공된 날짜인 데이터 소스 항목을 반환합니다.

        ex) "2021-05-10", "2021-05-10T12:00:00", "2021-10-15T12:00:00-07:00" """
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, value)
        self._value.update(result)
        return self

    def is_empty(self, property_: str):
        """날짜 속성 값과 비교할 값입니다.

        날짜 속성 값에 데이터가 없는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, True)
        self._value.update(result)
        return self

    def is_not_empty(self, property_: str):
        """날짜 속성 값과 비교할 값입니다.

        날짜 속성 값이 비어 있지 않은 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, True)
        self._value.update(result)
        return self

    def next_month(self, property_: str):
        """날짜 속성 값이 다음 달 이내인 데이터 소스 항목으로 결과를 제한하는 필터입니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, {})
        self._value.update(result)
        return self
    def next_week(self, property_: str):
        """날짜 속성 값이 다음 주 이내인 데이터 소스 항목으로 결과를 제한하는 필터입니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, {})
        self._value.update(result)
        return self
    def next_year(self, property_: str):
        """날짜 속성 값이 내년 이내인 데이터 소스 항목으로 결과를 제한하는 필터입니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, {})
        self._value.update(result)
        return self
    def on_or_after(self, property_: str, value: str):
        """날짜 속성 값과 비교할 값입니다.

        날짜 속성 값이 지정된 날짜와 같거나 이후인 데이터 소스 항목을 반환합니다.

        ex) "2021-05-10", "2021-05-10T12:00:00", "2021-10-15T12:00:00-07:00" """
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, value)
        self._value.update(result)
        return self

    def on_or_before(self, property_: str, value: str):
        """날짜 속성 값과 비교할 값입니다.

        날짜 속성 값이 지정된 날짜와 같거나 이전인 데이터 소스 항목을 반환합니다.

        ex) "2021-05-10", "2021-05-10T12:00:00", "2021-10-15T12:00:00-07:00" """
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, value)
        self._value.update(result)
        return self

    def past_month(self, property_: str):
        """지난달 이내의 부동산 가치가 있는 데이터 소스 항목으로 결과를 제한하는 필터입니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, {})
        self._value.update(result)
        return self
    def past_week(self, property_: str):
        """지난주 이내의 속성 값이 포함된 데이터 소스 항목으로 결과를 제한하는 필터입니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, {})
        self._value.update(result)
        return self
    def past_year(self, property_: str):
        """해당 속성 가치가 지난 1년 이내인 데이터 소스 항목으로 결과를 제한하는 필터입니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, {})
        self._value.update(result)
        return self
    def this_week(self, property_: str):
        """이번 주에 속성 값이 있는 데이터 소스 항목으로 결과를 제한하는 필터입니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, {})
        self._value.update(result)
        return self

class FilesFilter(FilterBase):
    def is_empty(self, property_: str):
        """파일 속성 값에 데이터가 포함되어 있지 않은지 여부를 나타냅니다.

        속성 값이 비어 있는 모든 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, True)
        self._value.update(result)
        return self

    def is_not_empty(self, property_: str):
        """속성 값에 데이터가 포함되어 있는지 여부를 나타냅니다.

        속성 값 이 채워진 모든 항목을 반환합니다"""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, True)
        self._value.update(result)
        return self


class FormulaFilter(FilterBase):
    def checkbox(self, property_: str, value: CheckboxFilter):
        """수식 결과를 비교할 체크박스 필터 조건입니다.

        수식 결과가 제공된 조건과 일치하는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        _value = value.value["checkbox"]
        result = _return_value(property_, self._filter_name, method_name, _value)
        self._value.update(result)
        return self

    def date(self, property_: str, value: DateFilter):
        """수식 결과를 비교할 날짜 필터 조건입니다.

        수식 결과가 제공된 조건과 일치하는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        _value = value.value["date"]
        result = _return_value(property_, self._filter_name, method_name, _value)
        self._value.update(result)
        return self

    def number(self, property_: str, value: NumberFilter):
        """수식 결과를 비교할 숫자 필터 조건입니다.

        수식 결과가 제공된 조건과 일치하는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        _value = value.value["number"]
        result = _return_value(property_, self._filter_name, method_name, _value)
        self._value.update(result)
        return self

    def string(self, property_: str, value: RichTextFilter):
        """수식 결과를 비교할 서식 있는 텍스트 필터 조건입니다.

        수식 결과가 제공된 조건과 일치하는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        _value = value.value["rich_text"]
        result = _return_value(property_, self._filter_name, method_name, _value)
        self._value.update(result)
        return self


class MultiSelectFilter(FilterBase):
    def contains(self, property_: str, value: str):
        """다중 선택 속성 값을 비교할 값입니다.

        다중 선택 값이 제공된 문자열과 일치하는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, value)
        self._value.update(result)
        return self

    def does_not_contain(self, property_: str, value: str):
        """다중 선택 속성 값을 비교할 값입니다.

        다중 선택 값이 제공된 문자열과 일치하지 않는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, value)
        self._value.update(result)
        return self

    def is_empty(self, property_: str):
        """다중 선택 속성 값이 비어 있는지 여부를 나타냅니다.

        다중 선택 값에 데이터가 없는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, True)
        self._value.update(result)
        return self

    def is_not_empty(self, property_: str):
        """다중 선택 속성 값이 비어 있지 않은지 여부를 나타냅니다.

        다중 선택 값에 데이터가 포함된 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, True)
        self._value.update(result)
        return self


class NumberFilter(FilterBase):
    def does_not_equal(self, property_: str, value: float):
        """숫자 속성 값을 비교할 입니다.

        숫자 속성 값이 제공된 값과 다른 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, value)
        self._value.update(result)
        return self

    def equals(self, property_: str, value: float):
        """숫자 속성 값을 비교할 대상입니다.

        숫자 속성 값이 제공된 숫자와 동일한 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, value)
        self._value.update(result)
        return self

    def greater_than(self, property_: str, value: float):
        """숫자 속성 값을 비교할 대상입니다.

        숫자 속성 값이 제공된 값을 초과하는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, value)
        self._value.update(result)
        return self

    def greater_than_or_equal_to(self, property_: str, value: float):
        """숫자 속성 값을 비교할 대상입니다.

        숫자 속성 값이 제공된 값보다 크거나 같은 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, value)
        self._value.update(result)
        return self

    def is_empty(self, property_: str):
        """속성 값이 비어 있는지 여부를 나타냅니다.

        숫자 속성 값에 데이터가 없는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, True)
        self._value.update(result)
        return self

    def is_not_empty(self, property_: str):
        """숫자 속성 값이 비어 있는지 여부를 나타냅니다.

        숫자 속성 값에 데이터가 포함된 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, True)
        self._value.update(result)
        return self

    def less_than(self, property_: str, value: float):
        """숫자 속성 값을 비교할 대상입니다.

        숫자 속성 값이 제공된 값보다 작은 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, value)
        self._value.update(result)
        return self

    def less_than_or_equal_to(self, property_: str, value: float):
        """숫자 속성 값을 비교할 대상입니다.

        숫자 속성 값이 제공된 값보다 작거나 같은 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, value)
        self._value.update(result)
        return self


class PeopleFilter(FilterBase):
    def contains(self, property_: str, value: str): # UUIDv4 ex) "6c574cee-ca68-41c8-86e0-1b9e992689fb"
        """people 속성 값과 비교할 값입니다.

        people 속성 값에 제공된 .이 포함된 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, value)
        self._value.update(result)
        return self

    def does_not_contain(self, property_: str, value: str): # UUIDv4 ex) "6c574cee-ca68-41c8-86e0-1b9e992689fb"
        """people 속성 값과 비교할 값입니다.

        people 속성 값에 제공된 .이 포함되지 않은 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, value)
        self._value.update(result)
        return self

    def is_empty(self, property_: str):
        """people 속성 값에 데이터가 포함되어 있지 않은지 여부를 나타냅니다.

        people 속성 값에 데이터가 없는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, True)
        self._value.update(result)
        return self

    def is_not_empty(self, property_: str):
        """people 속성 값에 데이터가 포함되어 있는지 여부를 나타냅니다.

        people 속성 값이 비어 있지 않은 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, True)
        self._value.update(result)
        return self


class RelationFilter(FilterBase):
    def contains(self, property_: str, value: str): # UUIDv4 ex) "6c574cee-ca68-41c8-86e0-1b9e992689fb"
        """관계 속성 값과 비교할 값입니다.

        관계 속성 값에 제공된 .이 포함된 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, value)
        self._value.update(result)
        return self # UUIDv4 ex) "6c574cee-ca68-41c8-86e0-1b9e992689fb"

    def does_not_contain(self, property_: str, value: str):
        """관계 속성 값과 비교할 값입니다.

        관계 속성 값에 제공된 .이 포함되지 않은 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, value)
        self._value.update(result)
        return self

    def is_empty(self, property_: str):
        """관계 속성 값에 데이터가 포함되어 있지 않은지 여부를 나타냅니다.

        관계 속성 값에 데이터가 없는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, True)
        self._value.update(result)
        return self

    def is_not_empty(self, property_: str):
        """관계 속성 값에 데이터가 포함되어 있는지 여부를 나타냅니다.

        속성 값이 비어 있지 않은 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, True)
        self._value.update(result)
        return self


class RichTextFilter(FilterBase):
    def contains(self, property_: str, value: str):
        """텍스트 속성 값을 비교할 대상입니다.

        제공된 값을 포함하는 텍스트 속성 값을 가진 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, value)
        self._value.update(result)
        return self

    def does_not_contain(self, property_: str, value: str):
        """텍스트 속성 값을 비교할 대상입니다.

        제공된 값을 포함하지 않는 텍스트 속성 값을 가진 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, value)
        self._value.update(result)
        return self

    def does_not_equal(self, property_: str, value: str):
        """텍스트 속성 값을 비교할 대상입니다.

        제공된 값과 일치하지 않는 텍스트 속성 값을 가진 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, value)
        self._value.update(result)
        return self

    def ends_with(self, property_: str, value: str):
        """텍스트 속성 값을 비교할 대상입니다.

        제공된 값으로 끝나는 텍스트 속성 값을 가진 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, value)
        self._value.update(result)
        return self

    def equals(self, property_: str, value: str):
        """텍스트 속성 값을 비교할 대상입니다.

        제공된 값과 일치하는 텍스트 속성 값을 가진 데이터 소스 항목을 반환합니다"""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, value)
        self._value.update(result)
        return self

    def is_empty(self, property_: str):
        """텍스트 속성 값에 데이터가 포함되어 있지 않은지 여부를 나타냅니다.

        텍스트 속성 값이 비어 있는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, True)
        self._value.update(result)
        return self

    def is_not_empty(self, property_: str):
        """텍스트 속성 값에 데이터가 포함되어 있는지 여부를 나타냅니다.

        데이터가 포함된 텍스트 속성 값을 가진 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, True)
        self._value.update(result)
        return self

    def starts_with(self, property_: str, value: str):
        """텍스트 속성 값을 비교할 대상입니다. 제공된 값으로 시작하는 텍스트 속성 값을 가진 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, value)
        self._value.update(result)
        return self


# class RollupFilter(FilterBase): ... # 일단 패스


class SelectFilter(FilterBase):
    def equals(self, property_: str, value: str):
        """select 속성 값을 비교할 대상입니다.

        select 속성 값이 제공된 문자열과 일치하는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, value)
        self._value.update(result)
        return self

    def does_not_equal(self, property_: str, value: str):
        """select 속성 값을 비교할 입니다.

        select 속성 값이 제공된 문자열과 일치하지 않는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, value)
        self._value.update(result)
        return self

    def is_empty(self, property_: str):
        """select 속성 값에 데이터가 포함되어 있지 않은지 여부를 나타냅니다.

        select 속성 값이 비어 있는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, True)
        self._value.update(result)
        return self

    def is_not_empty(self, property_: str):
        """select 속성 값에 데이터가 포함되어 있는지 여부를 나타냅니다.

        select 속성 값이 비어 있지 않은 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, True)
        self._value.update(result)
        return self


class StatusFilter(FilterBase):
    def equals(self, property_: str, value: str):
        """상태 속성 값을 비교할 문자열입니다.

        상태 속성 값이 제공된 문자열과 일치하는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, value)
        self._value.update(result)
        return self

    def does_not_equal(self, property_: str, value: str):
        """상태 속성 값을 비교할 문자열입니다.

        상태 속성 값이 제공된 문자열과 일치하지 않는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, value)
        self._value.update(result)
        return self

    def is_empty(self, property_: str):
        """상태 속성 값에 데이터가 포함되어 있지 않은지 여부를 나타냅니다.

        상태 속성 값이 비어 있는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, True)
        self._value.update(result)
        return self

    def is_not_empty(self, property_: str):
        """상태 속성 값에 데이터가 포함되어 있는지 여부를 나타냅니다.

        상태 속성 값이 비어 있지 않은 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, True)
        self._value.update(result)
        return self


# class TimestampFilter(FilterBase): ...
# 얘 혼자 이상함 남들 전부 property 쓸 때 얘는 timestamp 씀
# {
#   "filter": {
#     "timestamp": "created_time",
#     "created_time": {
#       "on_or_before": "2022-10-13"
#     }
#   }
# }


class VerificationFilter(FilterBase):
    def status(self, property_: str, value: Literal["verified", "expired", None]):
        """쿼리 중인 확인 상태입니다. 유효한 옵션은 다음과 같습니다.

        "verified", "expired", null 현재 확인 상태가 쿼리된 상태와 일치하는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, value)
        self._value.update(result)
        return self

class IDFilter(FilterBase):
    def does_not_equal(self, property_: str, value: float):
        """unique_id 속성 값과 비교할 값입니다.

        unique_id 속성 값이 제공된 값과 다른 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, value)
        self._value.update(result)
        return self

    def equals(self, property_: str, value: float):
        """unique_id 속성 값과 비교할 값입니다.

        unique_id 속성 값이 제공된 값과 동일한 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, value)
        self._value.update(result)
        return self

    def greater_than(self, property_: str, value: float):
        """unique_id 속성 값과 비교할 값입니다.

        unique_id 속성 값이 제공된 값을 초과하는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, value)
        self._value.update(result)
        return self

    def greater_than_or_equal_to(self, property_: str, value: float):
        """unique_id 속성 값과 비교할 값입니다.

        unique_id 속성 값이 제공된 값과 같거나 큰 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, value)
        self._value.update(result)
        return self

    def less_than(self, property_: str, value: float):
        """unique_id 속성 값과 비교할 값입니다.

        unique_id 속성 값이 제공된 값보다 작은 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, value)
        self._value.update(result)
        return self

    def less_than_or_equal_to(self, property_: str, value: float):
        """unique_id 속성 값과 비교할 값입니다.

        unique_id 속성 값이 제공된 값보다 작거나 같은 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        result = _return_value(property_, self._filter_name, method_name, value)
        self._value.update(result)
        return self


class Filter(FilterBase):
    checkbox = CheckboxFilter()
    date = DateFilter()
    files = FilesFilter()
    formula = FormulaFilter()
    multi_select = MultiSelectFilter()
    number = NumberFilter()
    people = PeopleFilter()
    relation = RelationFilter()
    text = RichTextFilter()
    # rollu = RollupFilter()
    select = SelectFilter()
    status = StatusFilter()
    # timestamp = Timestamp()
    verification = VerificationFilter()
    id = IDFilter()

    @classmethod
    def and_(cls, filter_: FilterBase, *filters: FilterBase):
        filter_list = [filter_.value]
        filter_list.extend( [_filter.value for _filter in filters] )
        value = { "and": filter_list }
        return Filter(value)
    @classmethod
    def or_(cls, filter_: FilterBase, *filters: FilterBase):
        filter_list = [filter_.value]
        filter_list.extend( [_filter.value for _filter in filters] )
        value = { "or": filter_list }
        return Filter(value)


class SortBase(ListValueBase): ...


class Sort(SortBase):
    @classmethod
    def sort(cls, property_: str, direction: Literal["ascending", "descending"]):
        result = {
            "property": property_,
            "direction": direction }
        return _Sort( [result] )


class _Sort(SortBase):
    def sort(self, property_: str, direction: Literal["ascending", "descending"]):
        result = {
            "property": property_,
            "direction": direction }

        self._value.append(result)
        return self


class NotionDatabaseLite(NotionBase, Write, Read, Update, Remove):
    def __init__(self, key: str, DB_id: str):
        super().__init__(key, DB_id, "database")
        self._datas: list[NotionDatabasePage] = []

    def write(self, write_properties_object_: DatabaseObject):
        url = "https://api.notion.com/v1/pages"
        headers = self._add_headers("2025-09-03")

        payload = {
            "parent": { "database_id": self.id },
            "properties": write_properties_object_.value
        }

        response = requests.post(url, json=payload, headers=headers)
        if not response.ok:
            raise ValueError(response.json())
        
        new_page = _parser_page(self.api_key, response.json())
        self._datas.append(new_page)
        return new_page

    def read(self, *, filter: FilterBase | dict | None = None, sort: SortBase | dict | None = None, page_size: int=100):
        """
        ㅁㄴㅇㅁㄴㅇ

        Args:
            filter:  Filter 오브젝트를 이용해서 표현하거나, 아니면 순수 딕셔너리를 이용
            sort: 정렬 기준
            page_size: 검색수 (최대 100)
        """
        url = f"https://api.notion.com/v1/databases/{self.id}/query"
        headers = self._add_headers("2022-06-28")

        payload = {}
        payload["page_size"] = max(0, min(page_size, 100))
        if filter is not None:
            if isinstance(filter, FilterBase):
                payload["filter"] = filter.value
            elif isinstance(filter, dict):
                payload["filter"] = filter
        if sort is not None:
            if isinstance(sort, SortBase):
                payload["sorts"] = sort.value
            elif isinstance(sort, dict):
                payload["sorts"] = sort

        response = requests.post(url, json=payload, headers=headers)
        if not response.ok:
            raise ValueError(response.json())
        
        self._datas = self._parse(response.json())

    @overload
    def update(self, page_or_index: NotionDatabasePage, update_properties_object_: DatabaseObject):
        """해당 페이지 업데이트"""
    @overload
    def update(self, page_or_index: int, update_properties_object_: DatabaseObject):
        """해당 인덱스 업데이트"""
    def update(self, page_or_index: NotionDatabasePage | int, update_properties_object_: DatabaseObject):
        if isinstance(page_or_index, int):
            obj = self.value[page_or_index]
        elif isinstance(page_or_index, NotionDatabasePage):
            obj = page_or_index

        # 해당 페이지 업데이트
        obj.update( update_properties_object_ )

    @overload
    def remove(self, page_or_index: NotionDatabasePage):
        """해당 페이지 삭제"""
    @overload
    def remove(self, page_or_index: int):
        """해당 인덱스 삭제"""
    def remove(self, page_or_index: NotionDatabasePage | int) -> bool:
        if isinstance(page_or_index, int):
            obj = self.value[page_or_index]
        elif isinstance(page_or_index, NotionDatabasePage):
            obj = page_or_index

        # 해당 페이지 삭제
        return obj.remove()

    def _parse(self, response_data: dict) -> list[NotionDatabasePage]:
        results: list = response_data["results"]
        result = []
        for data in results:
            database_page = _parser_page(self.api_key, data)
            result.append(database_page)
        return result

    @property
    def value(self):
        return self._datas

    def __str__(self) -> str:
        data_sources_count = len(self._datas)
        if data_sources_count == 0:
            return "데이터베이스: 데이터 소스 없음"

        stringlist = [str(source) for source in self._datas]

        if 3 < data_sources_count:
            return f"[데이터베이스: {",".join(stringlist[:3])}...]"

        return f"[데이터베이스: {",".join(stringlist)}]"


class NotionDatabasePage(NotionBase, Update, Remove):
    def __init__(self, api_key: str, id: str, object: str, values: dict[str, Any], types: dict[str, str]):
        super().__init__(api_key, id, object)
        self._values = values
        self._types = types

    def update(self, update_properties_object: DatabaseObject) -> NotionDatabasePage:
        url = f"https://api.notion.com/v1/pages/{self.id}"
        headers = self._add_headers("2025-09-03")
        update_properties = update_properties_object.value

        payload = {
            "in_trash": False,
            "erase_content": False,
            "properties": update_properties
        }

        response = requests.patch(url, json=payload, headers=headers)
        if not response.ok:
            raise ValueError(response.json())

        new_page = _parser_page(self.api_key, response.json())
        # 업데이트
        self._values = new_page._values
        self._types = new_page._types
        return new_page

    def remove(self) -> bool:
        url = f"https://api.notion.com/v1/pages/{self.id}"
        headers = self._add_headers("2025-09-03")
        payload = {
            "archived": False
        }
        # self.archived = True

        response = requests.patch(url, json=payload, headers=headers)
        # 되살리고 싶다면 archived 를 True 로
        return response.ok

    @property
    def value(self):
        return self._values
    def __str__(self) -> str:
        if self.archived:
            return f"{{페이지: 삭제됨}}"
        result = [f"{key}={value}" for key, value in self._values.items()]
        if 3 < len(result):
            return f"{{페이지: {",".join(result[:3])} ...}}"
        return f"{{페이지: {",".join(result)}}}"



def _parser_page(api_key: str, data: dict) -> NotionDatabasePage:
    _id = data["id"]
    _object = data["object"]
    values = {}
    types = {}
    properties: dict = data["properties"]
    for key, value in properties.items():
        _type: str = value["type"]
        values[key] = parser_database_object_data(_type, value)
        types[key] = _type
    return NotionDatabasePage(api_key, _id, _object, values, types)

