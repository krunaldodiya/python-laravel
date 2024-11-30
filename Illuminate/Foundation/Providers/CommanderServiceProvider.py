from typing import TYPE_CHECKING, Type

from Illuminate.Foundation.Console.HelpCommand import HelpCommand
from Illuminate.Foundation.Console.ListCommands import ListCommands
from Illuminate.Support.ServiceProvider import ServiceProvider

if TYPE_CHECKING:
    from Illuminate.Foundation.Application import Application


class CommanderServiceProvider(ServiceProvider):
    def __init__(self, app: Type["Application"]) -> None:
        self.__app = app

        self._commands = [
            ListCommands,
            HelpCommand,
        ]

    def register(self):
        self._register_commands(self._commands)

    def boot(self):
        pass

    def _register_commands(self, commands: list):
        self.commands(commands)
