from abc import abstractmethod
from typing import Any, Dict, Self
from Illuminate.Contracts.Support.JsonSerializable import JsonSerializable


class Collection(JsonSerializable):
    @abstractmethod
    def map(self, callback: Any) -> Self:
        raise NotImplementedError("Not Implemented")

    @abstractmethod
    def filter(self, callback: Any) -> Self:
        raise NotImplementedError("Not Implemented")

    @abstractmethod
    def all(self) -> Dict[Any, Any]:
        raise NotImplementedError("Not Implemented")

    @abstractmethod
    def count(self) -> int:
        raise NotImplementedError("Not Implemented")
