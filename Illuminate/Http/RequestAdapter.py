from abc import ABC, abstractmethod
from typing import Any


class RequestAdapter(ABC):
    request: Any

    @abstractmethod
    def get_url(self):
        raise NotImplementedError("Implement get_url method")

    @abstractmethod
    def get_full_url(self):
        raise NotImplementedError("Implement get_full_url method")
