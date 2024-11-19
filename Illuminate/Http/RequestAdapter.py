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
    def get_method(self):
        raise NotImplementedError("Implement get_method method")

    @abstractmethod
    def get_user(self):
        raise NotImplementedError("Implement get_user method")

    @abstractmethod
    def query_data(self):
        raise NotImplementedError("Implement query_data method")

    @abstractmethod
    def post_data(self):
        raise NotImplementedError("Implement post_data method")

    @abstractmethod
    def form_data(self):
        raise NotImplementedError("Implement form_data method")

    @abstractmethod
    def json_data(self):
        raise NotImplementedError("Implement json_data method")

    @abstractmethod
    def files_data(self):
        raise NotImplementedError("Implement files_data method")

    @abstractmethod
    def headers_data(self):
        raise NotImplementedError("Implement headers_data method")

    @abstractmethod
    def sessions_data(self):
        raise NotImplementedError("Implement sessions_data method")

    @abstractmethod
    def cookies_data(self):
        raise NotImplementedError("Implement cookies_data method")
