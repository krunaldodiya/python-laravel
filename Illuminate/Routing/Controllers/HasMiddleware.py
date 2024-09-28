from abc import ABC, abstractmethod
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

    def set_only(self, only: List[str] = []) -> Self:
        """Sets the routes where this middleware should apply."""
        self.__only = only
        return self

    def set_exclude(self, exclude: List[str] = []) -> Self:
        """Sets the routes where this middleware should NOT apply."""
        self.__exclude = exclude
        return self

    def filter(self, method) -> bool:
        """
        Determines if the middleware applies to the given method.

        - If 'only' is defined, it applies only to those methods.
        - If 'only' is empty, but 'exclude' is defined, it excludes those methods.
        - If both are empty, it applies to all methods.
        """
        if self.__only:
            return method in self.__only
        elif self.__exclude:
            return method not in self.__exclude

        return True


class HasMiddleware(ABC):
    @staticmethod
    def middleware() -> List[Union[str, Middleware]]:
        raise NotImplementedError("Must implement middleware method")
