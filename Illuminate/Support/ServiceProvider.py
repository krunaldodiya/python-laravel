from abc import ABC, abstractmethod


class ServiceProvider(ABC):
    booted_callbacks = {}

    @abstractmethod
    def register(self):
        pass

    @abstractmethod
    def boot(self):
        pass

    def booted(self, callback):
        self.booted_callbacks[self.__class__] = callback
