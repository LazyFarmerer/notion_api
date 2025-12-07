from typing import Type


class Register[K, V]:
    def __init__(self):
        self.dict: dict[K, V] = {}

    def __call__(self, key: K):
        def decorator(obj: V) -> V:
            self.dict[key] = obj # 실행하지 않고 보관
            return obj
        return decorator

class InstanceRegister[K, V]:
    def __init__(self):
        self.dict: dict[K, V] = {}

    def __call__(self, key: K):
        def decorator(obj: Type[V]) -> Type[V]:
            self.dict[key] = obj() # 실행해서 인스턴스 값을 가지고 있음
            return obj
        return decorator
