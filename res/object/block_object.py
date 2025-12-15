

# 여기 참고하기
# https://developers.notion.com/reference/block


from ..abstract.value import DictValueBase


class BlockObjectBase:
    pass


class TextObject:
    """직접 사용하진 않음
    
    그런데 다른 텍스트 관련 블록 오브젝트에서 공통으로 사용됨"""
    def object(self, value: str | None) -> dict:
        payload = {}
        if isinstance(value, str):
            payload = { "rich_text": [ { "text": { "content": value }, "type": "text" } ] }
        elif value is None:
            payload = { "rich_text": [] }
        return payload
    def get(self, value: dict) -> str | None:
        values: list = value["rich_text"]
        if len(values) == 0:
            return None

        _value: dict = values[0]
        return _value["plain_text"]


class FileObject:
    """직접 사용하지 않음
    
    그런데 다른 파일 관련 블록 오브젝트에서 공통으로 사용됨"""
    def object(self, url: str | None) -> dict:
        payload = {}
        if isinstance(url, str):
            payload = {
                "file": {
                    "type": "external",
                    "external": { "url": url }
                }
            }
        elif url is None:
            payload = { "file": None }
        return payload

    def get(self, value: dict) -> dict | None:
        _type = value["type"]
        if not value[_type]:
            return None
        result = {
            "name": value["name"],
            "file": value[_type]["url"]
        }
        return result


class AudioBlockObject:
    def object(self, url: str | None) -> dict:
        print("audio 정보")
        print(url)
        return FileObject().object(url)

    def get(self, value: dict) -> dict | None:
        return value["audio"]["external"]["url"]


class BookmarkBlockObject:
    def object(self, value: str | None) -> dict:
        """bookmark"""
        # 북마크에 url 타입 있으면 안댐 { "url": value, "type": "url" } 이렇게 안댐
        return { "url": value }

    def get(self, value: dict) -> str | None:
        return value["url"]


class BreadcrumbBlockObject:
    def object(self, value: str | None) -> dict:
        print("Breadcrumb 정보")
        print(value)
        return {}

    def get(self, value: dict) -> dict:
        print("Breadcrumb 정보")
        print(value)
        return {}


class BulletedListItemBlockObject:
    def object(self, value: str | None) -> dict:
        print("bulleted_list_item 정보")
        print(value)
        return {}
    def get(self, value: dict) -> dict:
        print("bulleted_list_item 정보")
        print(value)
        return {}


class CalloutBlockObject:
    def object(self, value: str | None) -> dict:
        print("callout 정보")
        print(value)
        return TextObject().object(value)
    def get(self, value: dict) -> str | None:
        print("callout 정보")
        print(value)
        return TextObject().get(value)


class ChildDatabaseBlockObject:
    def object(self, value: str | None) -> dict:
        print("child_database 정보")
        print(value)
        return {}
    def get(self, value: dict) -> dict:
        print("child_database 정보")
        print(value)
        return {}


class ChildPageBlockObject:
    def object(self, value: str | None) -> dict:
        print("child_page 정보")
        print(value)
        return {}
    def get(self, value: dict) -> dict:
        print("child_page 정보")
        print(value)
        return {}


class CodeBlockObject:
    def object(self, value: str | None) -> dict:
        """code"""
        return TextObject().object(value)

    def get(self, value: dict) -> dict | None:
        text = TextObject().get(value)
        if text is None:
            return None
        return {
            "code": text,
            "language": value["language"]
        }


class ColumnListAndColumnBlockObject:
    def object(self, value: str | None) -> dict:
        print("ColumnListAndColumn 정보")
        print(value)
        return {}
    def get(self, value: dict) -> dict:
        print("ColumnListAndColumn 정보")
        print(value)
        return {}


class DividerBlockObject:
    def object(self, value: str | None) -> dict:
        print("divider 정보")
        print(value)
        return {}
    def get(self, value: dict) -> dict:
        print("divider 정보")
        print(value)
        return {}


class EmbedBlockObject:
    def object(self, url: str | None) -> dict:
        print("embed 정보")
        print(url)
        return {}
    def get(self, value: dict) -> dict:
        print("embed 정보")
        print(value)
        return value["embed"]["url"]


class EquationBlockObject:
    def object(self, value: str | None) -> dict:
        print("equation 정보")
        print(value)
        return {}
    def get(self, value: dict) -> dict:
        print("equation 정보")
        print(value)
        return value["equation"]["expression"]


class FileBlockObject:
    def object(self, value: str | None) -> dict:
        print("file 정보")
        print(value)
        return FileObject().object(value)
    def get(self, value: dict) -> dict | None:
        return FileObject().get(value)


class Heading123BlockObject:
    def object(self, value: str | None) -> dict:
        return TextObject().object(value)
    def get(self, value: dict) -> str | None:
        return TextObject().get(value)


class ImageBlockObject:
    def object(self, value: str | None) -> dict:
        print("image 정보")
        print(value)
        return FileObject().object(value)
    def get(self, value: dict) -> dict:
        print("image 정보")
        print(value)
        return value["image"]["external"]["url"]


class LinkPreviewBlockObject:
    def object(self, value: str | None) -> dict:
        print("link_preview 정보")
        print(value)
        return {}
    def get(self, value: dict) -> dict:
        print("link_preview 정보")
        print(value)
        return {}


class MentionBlockObject:
    def object(self, value: str | None) -> dict:
        print("mention 정보")
        print(value)
        return {}
    def get(self, value: dict) -> dict:
        print("mention 정보")
        print(value)
        return {}


class NumberedListItemBlockObject:
    def object(self, value: str | None) -> dict:
        print("numbered_list_item 정보")
        print(value)
        return {}
    def get(self, value: dict) -> dict:
        print("numbered_list_item 정보")
        print(value)
        return {}


class ParagraphBlockObject:
    def object(self, value: str | None) -> dict:
        return TextObject().object(value)
    def get(self, value: dict) -> str | None:
        return Heading123BlockObject().get(value)


class PDFBlockObject:
    def object(self, value: str | None) -> dict:
        print("pdf 정보")
        print(value)
        return FileObject().object(value)
    def get(self, value: dict) -> dict:
        print("pdf 정보")
        print(value)
        return value["pdf"]["external"]["url"]


class QuoteBlockObject:
    def object(self, value: str | None) -> dict:
        print("quote 정보")
        print(value)
        return {}
    def get(self, value: dict) -> dict:
        print("quote 정보")
        print(value)
        return {}


class SyncedBlockBlockObject:
    def object(self, value: str | None) -> dict:
        print("synced_block 정보")
        print(value)
        return {}
    def get(self, value: dict) -> dict:
        print("synced_block 정보")
        print(value)
        return {}


class TableBlockObject:
    def object(self, value: str | None) -> dict:
        print("table 정보")
        print(value)
        return {}
    def get(self, value: dict) -> dict:
        print("table 정보")
        print(value)
        return {}


class ToDoBlockObject:
    def object(self, value: str | None) -> dict:
        print("to_do 정보")
        print(value)
        return TextObject().object(value)
    def get(self, value: dict) -> str | None:
        print("to_do 정보")
        print(value)
        return TextObject().get(value)


class ToggleBlocksBlockObject:
    def object(self, value: str | None) -> dict:
        print("toggle 정보")
        print(value)
        return TextObject().object(value)
    def get(self, value: dict) -> str | None:
        print("toggle 정보")
        print(value)
        return Heading123BlockObject().get(value)


class VideoBlockObject:
    def object(self, value: str | None) -> dict:
        print("video 정보")
        print(value)
        return FileObject().object(value)
    def get(self, value: dict) -> dict:
        print("video 정보")
        print(value)
        return value["video"]["external"]["url"]


class BlockObject(DictValueBase):
    def audio(self, url: str | None):
        return AudioBlockObject().object(url)
    def bookmark(self, value: str | None):
        return BookmarkBlockObject().object(value)
    def breadcrumb(self, value: str | None):
        return BreadcrumbBlockObject().object(value)
    def bulleted_list_item(self, value: str | None):
        return BulletedListItemBlockObject().object(value)
    def callout(self, value: str | None):
        return CalloutBlockObject().object(value)
    def child_database(self, value: str | None):
        return ChildDatabaseBlockObject().object(value)
    def child_page(self, value: str | None):
        return ChildPageBlockObject().object(value)
    def code(self, value: str | None):
        return CodeBlockObject().object(value)
    def column(self, value: str | None):
        return ColumnListAndColumnBlockObject().object(value)
    def column_list(self, value: str | None):
        return ColumnListAndColumnBlockObject().object(value)
    def divider(self, value: str | None):
        return DividerBlockObject().object(value)
    def embed(self, url: str | None):
        return EmbedBlockObject().object(url)
    def equation(self, value: str | None):
        return EquationBlockObject().object(value)
    def file(self, url: str | None):
        return FileBlockObject().object(url)
    def heading_1(self, value: str | None):
        return Heading123BlockObject().object(value)
    def heading_2(self, value: str | None):
        return Heading123BlockObject().object(value)
    def heading_3(self, value: str | None):
        return Heading123BlockObject().object(value)
    def image(self, value: str | None):
        return ImageBlockObject().object(value)
    def link_preview(self, value: str | None):
        return LinkPreviewBlockObject().object(value)
    def mention(self, value: str | None):
        return MentionBlockObject().object(value)
    def numbered_list_item(self, value: str | None):
        return NumberedListItemBlockObject().object(value)
    def paragraph(self, value: str | None):
        return ParagraphBlockObject().object(value)
    def pdf(self, value: str | None):
        return PDFBlockObject().object(value)
    def quote(self, value: str | None):
        return QuoteBlockObject().object(value)
    def synced_block(self, value: str | None):
        return SyncedBlockBlockObject().object(value)
    def table(self, value: str | None):
        return TableBlockObject().object(value)
    def to_do(self, value: str | None):
        return ToDoBlockObject().object(value)
    def toggle(self, value: str | None):
        return ToggleBlocksBlockObject().object(value)
    def video(self, url: str | None):
        return VideoBlockObject().object(url)

def parser_database_object_data(type_: str, data: dict):

    match type_:
        case "audio":
            return AudioBlockObject().get(data)
        case "bookmark":
            return BookmarkBlockObject().get(data)
        case "breadcrumb":
            return BreadcrumbBlockObject().get(data)
        case "bulleted_list_item":
            return BulletedListItemBlockObject().get(data)
        case "callout":
            return CalloutBlockObject().get(data)
        case "child_database":
            return ChildDatabaseBlockObject().get(data)
        case "child_page":
            return ChildPageBlockObject().get(data)
        case "code":
            return CodeBlockObject().get(data)
        case "column_list" | "column":
            return ColumnListAndColumnBlockObject().get(data)
        case "divider":
            return DividerBlockObject().get(data)
        case "embed":
            return EmbedBlockObject().get(data)
        case "equation":
            return EquationBlockObject().get(data)
        case "file":
            return FileBlockObject().get(data)
        case "heading_1" | "heading_2" | "heading_3":
            return Heading123BlockObject().get(data)
        case "image":
            return ImageBlockObject().get(data)
        case "link_preview":
            return LinkPreviewBlockObject().get(data)
        case "mention":
            return MentionBlockObject().get(data)
        case "numbered_list_item":
            return NumberedListItemBlockObject().get(data)
        case "paragraph":
            return ParagraphBlockObject().get(data)
        case "pdf":
            return PDFBlockObject().get(data)
        case "quote":
            return QuoteBlockObject().get(data)
        case "synced_block":
            return SyncedBlockBlockObject().get(data)
        case "table":
            return TableBlockObject().get(data)
        case "to_do":
            return ToDoBlockObject().get(data)
        case "toggle":
            return ToggleBlocksBlockObject().get(data)
        case "video":
            return VideoBlockObject().get(data)
    
    return data

