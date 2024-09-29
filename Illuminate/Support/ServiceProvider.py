import importlib

from abc import ABC, abstractmethod
import sys


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

    def load_routes_from(self, loader: str):
        try:
            if loader in sys.modules:
                importlib.reload(sys.modules[loader])
            else:
                importlib.import_module(loader)
        except Exception as e:
            print("Route import error:", e)
