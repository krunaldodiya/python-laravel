from abc import ABC
from typing import List, Self, Union


class Middleware:
    def __init__(
        self, name: str, only: List[str] = [], exclude: List[str] = []
    ) -> None:
        self.__name = name
        self.__only = only
        self.__exclude = exclude

    @property
    def name(self):
        return self.__name

    @property
    def only(self):
        return self.__only

    @property
    def exclude(self):
        return self.__exclude

    def set_only(self, only: Union[str | List[str]] = []) -> Self:
        self.__only = only if isinstance(only, list) else [only]

        return self

    def set_exclude(self, exclude: Union[str | List[str]] = []) -> Self:
        self.__exclude = exclude if isinstance(exclude, list) else [exclude]

        return self

    def filter(self, method) -> bool:
        if self.__only:
            return method in self.__only
        elif self.__exclude:
            return method not in self.__exclude

        return True


class HasMiddleware(ABC):
    @classmethod
    def middleware(cls) -> List[Union[str, Middleware]]:
        raise NotImplementedError("Must implement middleware method")
