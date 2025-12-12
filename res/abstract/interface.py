

from abc import ABC, abstractmethod


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