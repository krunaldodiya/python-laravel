from abc import abstractmethod
from typing import Any


class JsonSerializable:
    @abstractmethod
    def json_serialize(self) -> Any:
        raise NotImplementedError("Not Implemented")
