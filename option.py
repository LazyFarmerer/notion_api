class Option:
    오름차순 = "ascending"
    내림차순 = "descending"
    @staticmethod
    def sorts(property_: str ="", direction: str =""):
        """
        load() 메서드 옵션용으로 사용하세요\n
        property: 정렬 기준, 무엇을 기준으로 정렬 할것인지\n
        direction: 오름차순 or 내림차순 선택
        """
        if not (property_ or direction):
            raise ValueError("\n'입력할거면 둘 다 입력하시오")

        result = [ { } ]
        if property_ != "":
            result[0]["property"] = property_
        if direction != "":
            if direction in ["ascending", "descending"]:
                result[0]["direction"] = direction
            else:
                raise ValueError("\n'ascending', 'descending' 둘 중 하나만 사용하기\nOption.오름차순, Option.내림차순 사용 가능")

        return result

    @staticmethod
    def filter(property_: str ="", query: str =""):
        """
        load() 메서드 옵션용으로 사용하세요\n
        property: 필터 기준, 무엇을 기준으로 필터 할것인지\n
        query: 검색할 일부
        """
        if not (property_ or query):
            raise ValueError("\n'입력할거면 둘 다 입력하시오")

        result = {
            "property": property_,
            "rich_text": {
                "contains": query
            }
        }

        return result