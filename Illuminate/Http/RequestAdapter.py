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

    @abstractmethod
    def query_data(self):
        raise NotImplementedError("Implement query_data method")

    @abstractmethod
    def post_data(self):
        raise NotImplementedError("Implement post_data method")
