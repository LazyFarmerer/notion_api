


class NotionBase:
    def __init__(self, api_key: str, id: str):
        self.api_key = api_key
        self.id = id
        self.archived: bool = False
        """삭제했는지 에 관한 정보"""

    def _add_headers(self, version: str):
        "헤더에 버젼을 추가해서 리턴"
        return {
            "Accept": "application/json",
            "Notion-Version": version,
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }