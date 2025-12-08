

from .notion_object_base import notion_object_instance_register


class NotionObject:
    def __init__(self, value: dict | None = None) -> None:
        if value is None:
            self.value = {}
            return

        self.value = value

    def title(self, properties: str, value: str | None) -> NotionObject:
        """타이틀"""
        result = { properties: notion_object_instance_register.dict["title"].object(value) }
        result.update(self.value)
        return NotionObject(result)

    def date(self, properties: str, start: str | None, end: str | None = None) -> NotionObject:
        """날짜 ex)'2022-08-08'"""
        result = { properties: notion_object_instance_register.dict["date"].object(start, end) }
        result.update(self.value)
        return NotionObject(result)

    def text(self, properties: str, value: str | None) -> NotionObject:
        """텍스트"""
        result = { properties: notion_object_instance_register.dict["text"].object(value) }
        result.update(self.value)
        return NotionObject(result)

    def rich_text(self, properties: str, value: str | None) -> NotionObject:
        """텍스트"""
        result = { properties: notion_object_instance_register.dict["rich_text"].object(value) }
        result.update(self.value)
        return NotionObject(result)

    def paragraph(self, properties: str, value: str | None) -> NotionObject:
        """텍스트"""
        result = { properties: notion_object_instance_register.dict["paragraph"].object(value) }
        result.update(self.value)
        return NotionObject(result)

    def heading1(self, properties: str, value: str | None) -> NotionObject:
        result = { properties: notion_object_instance_register.dict["heading1"].object(value) }
        result.update(self.value)
        return NotionObject(result)

    def heading2(self, properties: str, value: str | None) -> NotionObject:
        result = { properties: notion_object_instance_register.dict["heading2"].object(value) }
        result.update(self.value)
        return NotionObject(result)

    def heading3(self, properties: str, value: str | None) -> NotionObject:
        result = { properties: notion_object_instance_register.dict["heading3"].object(value) }
        result.update(self.value)
        return NotionObject(result)

    def number(self, properties: str, value: float | None) -> NotionObject:
        """숫자"""
        result = { properties: notion_object_instance_register.dict["number"].object(value) }
        result.update(self.value)
        return NotionObject(result)

    def select(self, properties: str, value: str | None) -> NotionObject:
        """선택"""
        result = { properties: notion_object_instance_register.dict["select"].object(value) }
        result.update(self.value)
        return NotionObject(result)

    def checkbox(self, properties: str, value: bool) -> NotionObject:
        """체크박스"""
        result = { properties: notion_object_instance_register.dict["checkbox"].object(value) }
        result.update(self.value)
        return NotionObject(result)

    def email(self, properties: str, value: str | None) -> NotionObject:
        """이메일"""
        result = { properties: notion_object_instance_register.dict["email"].object(value) }
        result.update(self.value)
        return NotionObject(result)

    def phone_number(self, properties: str, value: str | None) -> NotionObject:
        """전화번호 그런데 아무거나 다 적히긴 함"""
        result = { properties: notion_object_instance_register.dict["phone_number"].object(value) }
        result.update(self.value)
        return NotionObject(result)

    def url(self, properties: str, value: str | None) -> NotionObject:
        """URL"""
        result = { properties: notion_object_instance_register.dict["url"].object(value) }
        result.update(self.value)
        return NotionObject(result)

    def bookmark(self, properties: str, value: str | None) -> NotionObject:
        """bookmark"""
        result = { properties: notion_object_instance_register.dict["bookmark"].object(value) }
        result.update(self.value)
        return NotionObject(result)

    def code(self, properties: str, value: str | None) -> NotionObject:
        """code"""
        result = { properties: notion_object_instance_register.dict["code"].object(value) }
        result.update(self.value)
        return NotionObject(result)

    def file(self, properties: str, value: str | None) -> NotionObject:
        """파일은 노션 api 로 올릴 수 없음!"""
        result = { properties: notion_object_instance_register.dict["file"].object(value) }
        result.update(self.value)
        return NotionObject(result)

    def files(self, properties: str, value: str | None) -> NotionObject:
        """파일은 노션 api 로 올릴 수 없음!"""
        result = { properties: notion_object_instance_register.dict["files"].object(value) }
        result.update(self.value)
        return NotionObject(result)

