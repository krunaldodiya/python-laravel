from abc import ABC, abstractmethod
from typing import Any


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
        self.booting_callbacks[self] = callback

    def booted(self, callback):
        self.booted_callbacks[self] = callback

    def call_booting_callbacks(self):
        callbacks = self.booting_callbacks.get(self)

        if callbacks:
            callbacks()

    def call_booted_callbacks(self):
        callbacks = self.booted_callbacks.get(self)

        if callbacks:
            callbacks()
