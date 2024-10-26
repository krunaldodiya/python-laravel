from abc import abstractmethod
from typing import Any


class Resolvable:
    @abstractmethod
    def resolve_for_display(self) -> Any:
        raise NotImplementedError("Not Implemented")
