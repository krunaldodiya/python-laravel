from abc import abstractmethod
from typing import Any


class Resolvable:
    @abstractmethod
    def resolve_for_display(self, resource, attribute) -> Any:
        raise NotImplementedError("Not Implemented")

    @abstractmethod
    def resolve(self, resource, attribute) -> Any:
        raise NotImplementedError("Not Implemented")
