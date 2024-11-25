import sys
import importlib

from abc import ABC, abstractmethod
from Illuminate.Foundation.Console.Application import Application as Commander


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
            raise e

    def commands(self, *commands):
        all_commands = []

        if len(commands) == 1 and isinstance(commands[0], list):
            all_commands.extend(commands[0])
        else:
            all_commands.extend(commands)

        Commander.starting(lambda commander: commander.resolve_commands(all_commands))
