

# 여기 참고하기
# https://developers.notion.com/reference/block


from ..abstract.value import DictValueBase


class BlockObjectBase:
    pass

class BookmarkBlockObject:
    def object(self, value: str | None) -> dict:
        """bookmark"""
        # 북마크에 url 타입 있으면 안댐 { "url": value, "type": "url" } 이렇게 안댐
        return { "url": value }

    def get(self, value: dict) -> str | None:
        return value["bookmark"]["url"]

class BlockObject(DictValueBase):
    def bookmark(self, value: str | None):
        pass

def parser_database_object_data(type_: str, data: dict):

    match type_:
        case "checkbox":
            return BookmarkBlockObject().get(data)

# - "bookmark"
# - "breadcrumb"
# - "bulleted_list_item"
# - "callout"
# - "child_database"
# - "child_page"
# - "column"
# - "column_list"
# - "divider"
# - "embed"
# - "equation"
# - "file"
# - "heading_1"
# - "heading_2"
# - "heading_3"
# - "image"
# - "link_preview"
# - "numbered_list_item"
# - "paragraph"
# - "pdf"
# - "quote"
# - "synced_block"
# - "table"
# - "table_of_contents"
# - "table_row"
# - "template"
# - "to_do"
# - "toggle"
# - "unsupported"
# - "video"




# 이전 결과물들
# 다시 새롭게 가공하기

class NotionObjectBase:

    def object(self, *value) -> dict:
        return {}
    def get(self, value):
        pass

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


class RichTextObject(NotionObjectBase):
    def object(self, value: str | None) -> dict:
        return TextObject().object(value)
    def get(self, value: dict) -> str | None:
        return TextObject().get(value)

class ParagraphObject(NotionObjectBase):
    def object(self, value: str | None) -> dict:
        return TextObject().object(value)
    def get(self, value: dict) -> str | None:
        return Heading3Object().get(value)

class Heading1Object(NotionObjectBase):
    def object(self, value: str | None) -> dict:
        return TextObject().object(value)
    def get(self, value: dict) -> str | None:
        return Heading3Object().get(value)

class Heading2Object(NotionObjectBase):
    def object(self, value: str | None) -> dict:
        return TextObject().object(value)
    def get(self, value: dict) -> str | None:
        return Heading3Object().get(value)

class Heading3Object(NotionObjectBase):
    def object(self, value: str | None) -> dict:
        return TextObject().object(value)
    def get(self, value: dict) -> str | None:
        type_ = value["type"]
        if len(value[type_]) == 0:
            return None
        value[type_] = value[type_]["rich_text"]
        return TextObject().get(value)


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
