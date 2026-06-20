

from abc import ABC, abstractmethod


class Read(ABC):
    @abstractmethod
    def read(self):
        raise NotImplementedError


class Write(ABC):
    @abstractmethod
    def write(self, *args, **kwargs):
        raise NotImplementedError


class Update(ABC):
    @abstractmethod
    def update(self, *args, **kwargs):
        raise NotImplementedError


class Remove(ABC):
    @abstractmethod
    def remove(self) -> bool:
        raise NotImplementedError