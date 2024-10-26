from abc import abstractmethod
from typing import Any, Dict


class Arrayable:
    @abstractmethod
    def to_array(self):
        raise NotImplementedError("Not Implemented")


class ListValue(Arrayable):
    def __init__(self, items: Dict[Any, Any]):
        self._items = items

    def __iter__(self):
        return iter(self._items.values())

    def to_array(self):
        return list(self._items.values())
