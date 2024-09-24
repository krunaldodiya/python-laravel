from abc import ABC, abstractmethod
from typing import Any, Callable, List


class Gate(ABC):
    @abstractmethod
    def check(self, ability: str, arguments: List[Any] = []) -> bool:
        pass

    @abstractmethod
    def define(self, ability: str, callback: Callable[[Any], Any]) -> None:
        pass
