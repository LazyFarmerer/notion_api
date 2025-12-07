

from .notion_object_base import notion_object_instance_register


class NotionObjec:
    def __init__(self, value: dict | None = None) -> None:
        if value is None:
            self.value = {}
            return

        self.value = value

    def title(self, properties: str, value: str | None) -> NotionObjec:
        """타이틀"""
        result = { properties: notion_object_instance_register.dict["title"].object(value) }
        result.update(self.value)
        return NotionObjec(result)

    def date(self, properties: str, start: str | None, end: str | None = None) -> NotionObjec:
        """날짜 ex)'2022-08-08'"""
        result = { properties: notion_object_instance_register.dict["date"].object(start, end) }
        result.update(self.value)
        return NotionObjec(result)

    def text(self, properties: str, value: str | None) -> NotionObjec:
        """텍스트"""
        result = { properties: notion_object_instance_register.dict["text"].object(value) }
        result.update(self.value)
        return NotionObjec(result)

    def rich_text(self, properties: str, value: str | None) -> NotionObjec:
        """텍스트"""
        result = { properties: notion_object_instance_register.dict["rich_text"].object(value) }
        result.update(self.value)
        return NotionObjec(result)

    def paragraph(self, properties: str, value: str | None) -> NotionObjec:
        """텍스트"""
        result = { properties: notion_object_instance_register.dict["paragraph"].object(value) }
        result.update(self.value)
        return NotionObjec(result)

    def heading1(self, properties: str, value: str | None) -> NotionObjec:
        result = { properties: notion_object_instance_register.dict["heading1"].object(value) }
        result.update(self.value)
        return NotionObjec(result)

    def heading2(self, properties: str, value: str | None) -> NotionObjec:
        result = { properties: notion_object_instance_register.dict["heading2"].object(value) }
        result.update(self.value)
        return NotionObjec(result)

    def heading3(self, properties: str, value: str | None) -> NotionObjec:
        result = { properties: notion_object_instance_register.dict["heading3"].object(value) }
        result.update(self.value)
        return NotionObjec(result)

    def number(self, properties: str, value: float | None) -> NotionObjec:
        """숫자"""
        result = { properties: notion_object_instance_register.dict["number"].object(value) }
        result.update(self.value)
        return NotionObjec(result)

    def select(self, properties: str, value: str | None) -> NotionObjec:
        """선택"""
        result = { properties: notion_object_instance_register.dict["select"].object(value) }
        result.update(self.value)
        return NotionObjec(result)

    def checkbox(self, properties: str, value: bool) -> NotionObjec:
        """체크박스"""
        result = { properties: notion_object_instance_register.dict["checkbox"].object(value) }
        result.update(self.value)
        return NotionObjec(result)

    def email(self, properties: str, value: str | None) -> NotionObjec:
        """이메일"""
        result = { properties: notion_object_instance_register.dict["email"].object(value) }
        result.update(self.value)
        return NotionObjec(result)

    def phone_number(self, properties: str, value: str | None) -> NotionObjec:
        """전화번호 그런데 아무거나 다 적히긴 함"""
        result = { properties: notion_object_instance_register.dict["phone_number"].object(value) }
        result.update(self.value)
        return NotionObjec(result)

    def url(self, properties: str, value: str | None) -> NotionObjec:
        """URL"""
        result = { properties: notion_object_instance_register.dict["url"].object(value) }
        result.update(self.value)
        return NotionObjec(result)

    def bookmark(self, properties: str, value: str | None) -> NotionObjec:
        """bookmark"""
        result = { properties: notion_object_instance_register.dict["bookmark"].object(value) }
        result.update(self.value)
        return NotionObjec(result)

    def code(self, properties: str, value: str | None) -> NotionObjec:
        """code"""
        result = { properties: notion_object_instance_register.dict["code"].object(value) }
        result.update(self.value)
        return NotionObjec(result)

    def file(self, properties: str, value: str | None) -> NotionObjec:
        """파일은 노션 api 로 올릴 수 없음!"""
        result = { properties: notion_object_instance_register.dict["file"].object(value) }
        result.update(self.value)
        return NotionObjec(result)

    def files(self, properties: str, value: str | None) -> NotionObjec:
        """파일은 노션 api 로 올릴 수 없음!"""
        result = { properties: notion_object_instance_register.dict["files"].object(value) }
        result.update(self.value)
        return NotionObjec(result)

