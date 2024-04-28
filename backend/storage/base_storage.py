from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Iterator, Type, TypeVar, Generic

T = TypeVar("T", bound=BaseModel)


class BaseStorage(ABC, Generic[T]):
    def __init__(self, clazz: Type[T]):
        self.clazz = clazz

    @abstractmethod
    def put(self, key: str, value: T) -> None:
        pass

    @abstractmethod
    def get(self, key: str) -> T:
        pass

    @abstractmethod
    def keys(self) -> Iterator[T] | list[T]:
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        pass

    def drop(self) -> None:
        for key in self.keys():
            self.delete(key)

    def get_all(self) -> Iterator[T] | list[T]:
        for key in self.keys():
            yield self.get(key)
