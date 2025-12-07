

from abc import ABCMeta, abstractmethod


class Read(metaclass=ABCMeta):
    @abstractmethod
    def read(self):
        raise NotImplementedError


class Write(metaclass=ABCMeta):
    @abstractmethod
    def write(self):
        raise NotImplementedError


class Update(metaclass=ABCMeta):
    @abstractmethod
    def update(self):
        raise NotImplementedError


class Remove(metaclass=ABCMeta):
    @abstractmethod
    def remove(self) -> bool:
        raise NotImplementedError