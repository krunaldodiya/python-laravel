from abc import ABC, abstractmethod


class ServiceProvider(ABC):
    @abstractmethod
    def register(self):
        pass

    @abstractmethod
    def boot(self):
        pass
