from abc import abstractmethod
from typing import Any, Dict


class Jsonable:
    @abstractmethod
    def to_json(self):
        raise NotImplementedError("Not Implemented")


class DictValue(Jsonable):
    def __init__(self, items: Dict[Any, Any]):
        self._items = items

    def __iter__(self):
        return iter(self._items.items())

    def to_json(self):
        return self._items
