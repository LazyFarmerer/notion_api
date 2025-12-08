

from typing import Any, Literal
import sys


def _return_value(property_: str, filter_name: str, field: str, value: Any) -> dict:
    return {
        "property": property_,
        filter_name: { field: value }
    }


class FilterBase:
    _filter_name: str
    def __init__(self, value: dict | None = None) -> None:
        if value is None:
            self.value = {}
            return

        self.value = value


class Checkbox(FilterBase):
    _filter_name = "checkbox"
    def equals(self, property_: str, value: bool):
        """속성 값이 제공된 값과 정확히 일치하는지 여부를 나타냅니다.

        값이 정확히 일치하는 모든 데이터 소스 항목을 반환하거나 제외합니다."""
        method_name = sys._getframe().f_code.co_name
        return Checkbox(_return_value(property_, self._filter_name, method_name, value))

    def does_not_equal(self, property_: str, value: bool):
        """속성 값이 제공된 값과 다른지 여부를 나타냅니다.

        값에 차이가 있는 모든 데이터 소스 항목을 반환하거나 제외합니다."""
        method_name = sys._getframe().f_code.co_name
        return Checkbox(_return_value(property_, self._filter_name, method_name, value))


class Date(FilterBase):
    _filter_name = "date"
    def after(self, property_: str, value: str):
        """날짜 속성 값과 비교할 값입니다.

        날짜 속성 값이 제공된 날짜 이후인 데이터 소스 항목을 반환합니다.

        ex) "2021-05-10", "2021-05-10T12:00:00", "2021-10-15T12:00:00-07:00" """
        method_name = sys._getframe(0).f_code.co_name
        return Date(_return_value(property_, self._filter_name, method_name, value))

    def before(self, property_: str, value: str):
        """날짜 속성 값과 비교할 값입니다.

        날짜 속성 값이 제공된 날짜 이전인 데이터 소스 항목을 반환합니다.

        ex) "2021-05-10", "2021-05-10T12:00:00", "2021-10-15T12:00:00-07:00" """
        method_name = sys._getframe(0).f_code.co_name
        return Date(_return_value(property_, self._filter_name, method_name, value))

    def equals(self, property_: str, value: str):
        """날짜 속성 값과 비교할 값입니다.

        날짜 속성 값이 제공된 날짜인 데이터 소스 항목을 반환합니다.

        ex) "2021-05-10", "2021-05-10T12:00:00", "2021-10-15T12:00:00-07:00" """
        method_name = sys._getframe(0).f_code.co_name
        return Date(_return_value(property_, self._filter_name, method_name, value))

    def is_empty(self, property_: str):
        """날짜 속성 값과 비교할 값입니다.

        날짜 속성 값에 데이터가 없는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        return Date(_return_value(property_, self._filter_name, method_name, True))

    def is_not_empty(self, property_: str):
        """날짜 속성 값과 비교할 값입니다.

        날짜 속성 값이 비어 있지 않은 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe(0).f_code.co_name
        return Date(_return_value(property_, self._filter_name, method_name, True))

    def next_month(self, property_: str):
        """날짜 속성 값이 다음 달 이내인 데이터 소스 항목으로 결과를 제한하는 필터입니다."""
        method_name = sys._getframe(0).f_code.co_name
        return Date(_return_value(property_, self._filter_name, method_name, {}))

    def next_week(self, property_: str):
        """날짜 속성 값이 다음 주 이내인 데이터 소스 항목으로 결과를 제한하는 필터입니다."""
        method_name = sys._getframe(0).f_code.co_name
        return Date(_return_value(property_, self._filter_name, method_name, {}))

    def next_year(self, property_: str):
        """날짜 속성 값이 내년 이내인 데이터 소스 항목으로 결과를 제한하는 필터입니다."""
        method_name = sys._getframe(0).f_code.co_name
        return Date(_return_value(property_, self._filter_name, method_name, {}))

    def on_or_after(self, property_: str, value: str):
        """날짜 속성 값과 비교할 값입니다.

        날짜 속성 값이 지정된 날짜와 같거나 이후인 데이터 소스 항목을 반환합니다.

        ex) "2021-05-10", "2021-05-10T12:00:00", "2021-10-15T12:00:00-07:00" """
        method_name = sys._getframe(0).f_code.co_name
        return Date(_return_value(property_, self._filter_name, method_name, value))

    def on_or_before(self, property_: str, value: str):
        """날짜 속성 값과 비교할 값입니다.

        날짜 속성 값이 지정된 날짜와 같거나 이전인 데이터 소스 항목을 반환합니다.

        ex) "2021-05-10", "2021-05-10T12:00:00", "2021-10-15T12:00:00-07:00" """
        method_name = sys._getframe(0).f_code.co_name
        return Date(_return_value(property_, self._filter_name, method_name, value))

    def past_month(self, property_: str):
        """지난달 이내의 부동산 가치가 있는 데이터 소스 항목으로 결과를 제한하는 필터입니다."""
        method_name = sys._getframe(0).f_code.co_name
        return Date(_return_value(property_, self._filter_name, method_name, {}))

    def past_week(self, property_: str):
        """지난주 이내의 속성 값이 포함된 데이터 소스 항목으로 결과를 제한하는 필터입니다."""
        method_name = sys._getframe(0).f_code.co_name
        return Date(_return_value(property_, self._filter_name, method_name, {}))

    def past_year(self, property_: str):
        """해당 속성 가치가 지난 1년 이내인 데이터 소스 항목으로 결과를 제한하는 필터입니다."""
        method_name = sys._getframe(0).f_code.co_name
        return Date(_return_value(property_, self._filter_name, method_name, {}))

    def this_week(self, property_: str):
        """이번 주에 속성 값이 있는 데이터 소스 항목으로 결과를 제한하는 필터입니다."""
        method_name = sys._getframe(0).f_code.co_name
        return Date(_return_value(property_, self._filter_name, method_name, {}))


class Files(FilterBase):
    _filter_name = "files"
    def is_empty(self, property_: str):
        """파일 속성 값에 데이터가 포함되어 있지 않은지 여부를 나타냅니다.

        속성 값이 비어 있는 모든 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return Files(_return_value(property_, self._filter_name, method_name, True))

    def is_not_empty(self, property_: str):
        """속성 값에 데이터가 포함되어 있는지 여부를 나타냅니다.

        속성 값 이 채워진 모든 항목을 반환합니다"""
        method_name = sys._getframe().f_code.co_name
        return Files(_return_value(property_, self._filter_name, method_name, True))


class Formula(FilterBase):
    _filter_name = "formula"
    def checkbox(self, property_: str, value: Checkbox):
        """수식 결과를 비교할 체크박스 필터 조건입니다.

        수식 결과가 제공된 조건과 일치하는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        _value = value.value["checkbox"]
        return Formula(_return_value(property_, self._filter_name, method_name, _value))

    def date(self, property_: str, value: Date):
        """수식 결과를 비교할 날짜 필터 조건입니다.

        수식 결과가 제공된 조건과 일치하는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        _value = value.value["date"]
        return Formula(_return_value(property_, self._filter_name, method_name, _value))

    def number(self, property_: str, value: Number):
        """수식 결과를 비교할 숫자 필터 조건입니다.

        수식 결과가 제공된 조건과 일치하는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        _value = value.value["number"]
        return Formula(_return_value(property_, self._filter_name, method_name, _value))

    def string(self, property_: str, value: RichText):
        """수식 결과를 비교할 서식 있는 텍스트 필터 조건입니다.

        수식 결과가 제공된 조건과 일치하는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        _value = value.value["rich_text"]
        return Formula(_return_value(property_, self._filter_name, method_name, _value))


class MultiSelect(FilterBase):
    _filter_name = "multi_select"
    def contains(self, property_: str, value: str):
        """다중 선택 속성 값을 비교할 값입니다.

        다중 선택 값이 제공된 문자열과 일치하는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return MultiSelect(_return_value(property_, self._filter_name, method_name, value))

    def does_not_contain(self, property_: str, value: str):
        """다중 선택 속성 값을 비교할 값입니다.

        다중 선택 값이 제공된 문자열과 일치하지 않는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return MultiSelect(_return_value(property_, self._filter_name, method_name, value))

    def is_empty(self, property_: str):
        """다중 선택 속성 값이 비어 있는지 여부를 나타냅니다.

        다중 선택 값에 데이터가 없는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return MultiSelect(_return_value(property_, self._filter_name, method_name, True))

    def is_not_empty(self, property_: str):
        """다중 선택 속성 값이 비어 있지 않은지 여부를 나타냅니다.

        다중 선택 값에 데이터가 포함된 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return MultiSelect(_return_value(property_, self._filter_name, method_name, True))


class Number(FilterBase):
    _filter_name = "number"
    def does_not_equal(self, property_: str, value: float):
        """숫자 속성 값을 비교할 입니다.

        숫자 속성 값이 제공된 값과 다른 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return Number(_return_value(property_, self._filter_name, method_name, value))

    def equals(self, property_: str, value: float):
        """숫자 속성 값을 비교할 대상입니다.

        숫자 속성 값이 제공된 숫자와 동일한 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return Number(_return_value(property_, self._filter_name, method_name, value))

    def greater_than(self, property_: str, value: float):
        """숫자 속성 값을 비교할 대상입니다.

        숫자 속성 값이 제공된 값을 초과하는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return Number(_return_value(property_, self._filter_name, method_name, value))

    def greater_than_or_equal_to(self, property_: str, value: float):
        """숫자 속성 값을 비교할 대상입니다.

        숫자 속성 값이 제공된 값보다 크거나 같은 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return Number(_return_value(property_, self._filter_name, method_name, value))

    def is_empty(self, property_: str):
        """속성 값이 비어 있는지 여부를 나타냅니다.

        숫자 속성 값에 데이터가 없는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return Number(_return_value(property_, self._filter_name, method_name, True))

    def is_not_empty(self, property_: str):
        """숫자 속성 값이 비어 있는지 여부를 나타냅니다.

        숫자 속성 값에 데이터가 포함된 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return Number(_return_value(property_, self._filter_name, method_name, True))

    def less_than(self, property_: str, value: float):
        """숫자 속성 값을 비교할 대상입니다.

        숫자 속성 값이 제공된 값보다 작은 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return Number(_return_value(property_, self._filter_name, method_name, value))

    def less_than_or_equal_to(self, property_: str, value: float):
        """숫자 속성 값을 비교할 대상입니다.

        숫자 속성 값이 제공된 값보다 작거나 같은 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return Number(_return_value(property_, self._filter_name, method_name, value))


class People(FilterBase):
    _filter_name = "people"
    def contains(self, property_: str, value: str): # UUIDv4 ex) "6c574cee-ca68-41c8-86e0-1b9e992689fb"
        """people 속성 값과 비교할 값입니다.

        people 속성 값에 제공된 .이 포함된 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return People(_return_value(property_, self._filter_name, method_name, value))

    def does_not_contain(self, property_: str, value: str): # UUIDv4 ex) "6c574cee-ca68-41c8-86e0-1b9e992689fb"
        """people 속성 값과 비교할 값입니다.

        people 속성 값에 제공된 .이 포함되지 않은 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return People(_return_value(property_, self._filter_name, method_name, value))

    def is_empty(self, property_: str):
        """people 속성 값에 데이터가 포함되어 있지 않은지 여부를 나타냅니다.

        people 속성 값에 데이터가 없는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return People(_return_value(property_, self._filter_name, method_name, True))

    def is_not_empty(self, property_: str):
        """people 속성 값에 데이터가 포함되어 있는지 여부를 나타냅니다.

        people 속성 값이 비어 있지 않은 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return People(_return_value(property_, self._filter_name, method_name, True))


class Relation(FilterBase):
    _filter_name = "relation"
    def contains(self, property_: str, value: str): # UUIDv4 ex) "6c574cee-ca68-41c8-86e0-1b9e992689fb"
        """관계 속성 값과 비교할 값입니다.

        관계 속성 값에 제공된 .이 포함된 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return Relation(_return_value(property_, self._filter_name, method_name, value)) # UUIDv4 ex) "6c574cee-ca68-41c8-86e0-1b9e992689fb"

    def does_not_contain(self, property_: str, value: str):
        """관계 속성 값과 비교할 값입니다.

        관계 속성 값에 제공된 .이 포함되지 않은 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return Relation(_return_value(property_, self._filter_name, method_name, value))

    def is_empty(self, property_: str):
        """관계 속성 값에 데이터가 포함되어 있지 않은지 여부를 나타냅니다.

        관계 속성 값에 데이터가 없는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return Relation(_return_value(property_, self._filter_name, method_name, True))

    def is_not_empty(self, property_: str):
        """관계 속성 값에 데이터가 포함되어 있는지 여부를 나타냅니다.

        속성 값이 비어 있지 않은 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return Relation(_return_value(property_, self._filter_name, method_name, True))


class RichText(FilterBase):
    _filter_name = "rich_text"
    def contains(self, property_: str, value: str):
        """텍스트 속성 값을 비교할 대상입니다.

        제공된 값을 포함하는 텍스트 속성 값을 가진 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return RichText(_return_value(property_, self._filter_name, method_name, value))

    def does_not_contain(self, property_: str, value: str):
        """텍스트 속성 값을 비교할 대상입니다.

        제공된 값을 포함하지 않는 텍스트 속성 값을 가진 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return RichText(_return_value(property_, self._filter_name, method_name, value))

    def does_not_equal(self, property_: str, value: str):
        """텍스트 속성 값을 비교할 대상입니다.

        제공된 값과 일치하지 않는 텍스트 속성 값을 가진 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return RichText(_return_value(property_, self._filter_name, method_name, value))

    def ends_with(self, property_: str, value: str):
        """텍스트 속성 값을 비교할 대상입니다.

        제공된 값으로 끝나는 텍스트 속성 값을 가진 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return RichText(_return_value(property_, self._filter_name, method_name, value))

    def equals(self, property_: str, value: str):
        """텍스트 속성 값을 비교할 대상입니다.

        제공된 값과 일치하는 텍스트 속성 값을 가진 데이터 소스 항목을 반환합니다"""
        method_name = sys._getframe().f_code.co_name
        return RichText(_return_value(property_, self._filter_name, method_name, value))

    def is_empty(self, property_: str):
        """텍스트 속성 값에 데이터가 포함되어 있지 않은지 여부를 나타냅니다.

        텍스트 속성 값이 비어 있는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return RichText(_return_value(property_, self._filter_name, method_name, True))

    def is_not_empty(self, property_: str):
        """텍스트 속성 값에 데이터가 포함되어 있는지 여부를 나타냅니다.

        데이터가 포함된 텍스트 속성 값을 가진 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return RichText(_return_value(property_, self._filter_name, method_name, True))

    def starts_with(self, property_: str, value: str):
        """텍스트 속성 값을 비교할 대상입니다. 제공된 값으로 시작하는 텍스트 속성 값을 가진 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return RichText(_return_value(property_, self._filter_name, method_name, value))


class Rollup(FilterBase):
    _filter_name = "rollup"
    pass # 일단 패스


class Select(FilterBase):
    _filter_name = "select"
    def equals(self, property_: str, value: str):
        """select 속성 값을 비교할 대상입니다.

        select 속성 값이 제공된 문자열과 일치하는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return Select(_return_value(property_, self._filter_name, method_name, value))

    def does_not_equal(self, property_: str, value: str):
        """select 속성 값을 비교할 입니다.

        select 속성 값이 제공된 문자열과 일치하지 않는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return Select(_return_value(property_, self._filter_name, method_name, value))

    def is_empty(self, property_: str):
        """select 속성 값에 데이터가 포함되어 있지 않은지 여부를 나타냅니다.

        select 속성 값이 비어 있는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return Select(_return_value(property_, self._filter_name, method_name, True))

    def is_not_empty(self, property_: str):
        """select 속성 값에 데이터가 포함되어 있는지 여부를 나타냅니다.

        select 속성 값이 비어 있지 않은 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return Select(_return_value(property_, self._filter_name, method_name, True))


class Status(FilterBase):
    _filter_name = "status"
    def equals(self, property_: str, value: str):
        """상태 속성 값을 비교할 문자열입니다.

        상태 속성 값이 제공된 문자열과 일치하는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return Status(_return_value(property_, self._filter_name, method_name, value))

    def does_not_equal(self, property_: str, value: str):
        """상태 속성 값을 비교할 문자열입니다.

        상태 속성 값이 제공된 문자열과 일치하지 않는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return Status(_return_value(property_, self._filter_name, method_name, value))

    def is_empty(self, property_: str):
        """상태 속성 값에 데이터가 포함되어 있지 않은지 여부를 나타냅니다.

        상태 속성 값이 비어 있는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return Status(_return_value(property_, self._filter_name, method_name, True))

    def is_not_empty(self, property_: str):
        """상태 속성 값에 데이터가 포함되어 있는지 여부를 나타냅니다.

        상태 속성 값이 비어 있지 않은 데이터 소스 항목을 반환합니다.	"""
        method_name = sys._getframe().f_code.co_name
        return Status(_return_value(property_, self._filter_name, method_name, True))


class Timestamp(FilterBase):
    _filter_name = "timestamp"
    pass
# 얘 혼자 이상함 남들 전부 property 쓸 때 얘는 timestamp 씀
# {
#   "filter": {
#     "timestamp": "created_time",
#     "created_time": {
#       "on_or_before": "2022-10-13"
#     }
#   }
# }


class Verification(FilterBase):
    _filter_name = "verification"
    def status(self, property_: str, value: Literal["verified", "expired", None]):
        """쿼리 중인 확인 상태입니다. 유효한 옵션은 다음과 같습니다.

        "verified", "expired", null 현재 확인 상태가 쿼리된 상태와 일치하는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return Verification(_return_value(property_, self._filter_name, method_name, value))

class ID(FilterBase):
    _filter_name = "verification"
    def does_not_equal(self, property_: str, value: float):
        """unique_id 속성 값과 비교할 값입니다.

        unique_id 속성 값이 제공된 값과 다른 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return ID(_return_value(property_, self._filter_name, method_name, value))

    def equals(self, property_: str, value: float):
        """unique_id 속성 값과 비교할 값입니다.

        unique_id 속성 값이 제공된 값과 동일한 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return ID(_return_value(property_, self._filter_name, method_name, value))

    def greater_than(self, property_: str, value: float):
        """unique_id 속성 값과 비교할 값입니다.

        unique_id 속성 값이 제공된 값을 초과하는 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return ID(_return_value(property_, self._filter_name, method_name, value))

    def greater_than_or_equal_to(self, property_: str, value: float):
        """unique_id 속성 값과 비교할 값입니다.

        unique_id 속성 값이 제공된 값과 같거나 큰 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return ID(_return_value(property_, self._filter_name, method_name, value))

    def less_than(self, property_: str, value: float):
        """unique_id 속성 값과 비교할 값입니다.

        unique_id 속성 값이 제공된 값보다 작은 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return ID(_return_value(property_, self._filter_name, method_name, value))

    def less_than_or_equal_to(self, property_: str, value: float):
        """unique_id 속성 값과 비교할 값입니다.

        unique_id 속성 값이 제공된 값보다 작거나 같은 데이터 소스 항목을 반환합니다."""
        method_name = sys._getframe().f_code.co_name
        return ID(_return_value(property_, self._filter_name, method_name, value))








class RichText2(FilterBase):
    _filter_name = "rich_text"








# https://developers.notion.com/reference/filter-data-source-entries#formula
# 이어서 계속 적기




class Filter(FilterBase):
    checkbox = Checkbox()
    date = Date()
    files = Files()
    formula = Formula()
    multi_select = MultiSelect()
    number = Number()
    people = People()
    relation = Relation()
    richText = RichText()
    select = Select()
    status = Status()
    # timestamp = Timestamp()

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

