from abc import abstractmethod
from typing import Any, Callable, Self
from Illuminate.Contracts.Collections.Collection import Collection as CollectionContract


class Enumerable(CollectionContract):
    @abstractmethod
    def map_into(self, class_name) -> Self:
        raise NotImplementedError("Not Implemented")

    @abstractmethod
    def reject(self, callback) -> Self:
        raise NotImplementedError("Not Implemented")

    @abstractmethod
    def each(self, callback: Callable[[Any], Any]) -> Self:
        raise NotImplementedError("Not Implemented")

    @abstractmethod
    def every(self, data_key, data_operator, data_value) -> int:
        raise NotImplementedError("Not Implemented")

    @abstractmethod
    def partition(self, data_key, data_operator, data_value) -> int:
        raise NotImplementedError("Not Implemented")
