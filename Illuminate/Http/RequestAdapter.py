from abc import ABC, abstractmethod


class RequestAdapter(ABC):
    @abstractmethod
    def get_url(self):
        raise NotImplementedError("Implement get_url method")

    @abstractmethod
    def get_full_url(self):
        raise NotImplementedError("Implement get_full_url method")
