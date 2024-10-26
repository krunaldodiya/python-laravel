from abc import abstractmethod
from typing import Any, Dict
from Illuminate.Contracts.Support.JsonSerializable import JsonSerializable


class Enumerable(JsonSerializable):
    @abstractmethod
    def all(self) -> Dict[Any, Any]:
        raise NotImplementedError("Not Implemented")

    @abstractmethod
    def count(self) -> int:
        raise NotImplementedError("Not Implemented")
