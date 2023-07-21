from abc import ABC, abstractmethod


class ServiceProvider(ABC):
    booting_callbacks = {}
    booted_callbacks = {}

    @abstractmethod
    def register(self):
        pass

    @abstractmethod
    def boot(self):
        pass

    def booting(self, callback):
        self.booting_callbacks[self.__class__] = callback

    def booted(self, callback):
        self.booted_callbacks[self.__class__] = callback
