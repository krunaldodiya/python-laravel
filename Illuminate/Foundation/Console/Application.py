import inspect
from typing import Self
from Illuminate.Contracts.Foundation.Application import (
    Application as ApplicationContract,
)
from Illuminate.Events.Dispatcher import Dispatcher
from Illuminate.Foundation.Console.ContainerCommandLoader import ContainerCommandLoader
from Illuminate.Foundation.Console.Events.CommanderStarting import CommanderStarting
from Illuminate.Foundation.Console.Input.ArgvInput import ArgvInput
from Illuminate.Foundation.Console.Output.ConsoleOutput import ConsoleOutput
from Illuminate.Helpers.Util import Util
from Illuminate.Foundation.Console.Command import Command


class Application:
    bootstrappers: list = []
    command_map: dict = {}

    def __init__(self, app: ApplicationContract, events: Dispatcher, version):
        self.__app = app

        self.__events = events

        self.__version = version

        self.__events.dispatch(CommanderStarting(self))

        self.bootstrap()

        self.command_loader: ContainerCommandLoader | None = None

    @classmethod
    def starting(cls, callbacks):
        cls.bootstrappers.append(callbacks)

    def bootstrap(self):
        for bootstapper in self.bootstrappers:
            Util.callback_with_dynamic_args(bootstapper, [self])

    def run(self, input: ArgvInput, output: ConsoleOutput):
        assert self.command_loader is not None, "no command loader set"

        command = self.command_loader.get_current_command(input)

        command.validate(input)

        action = getattr(command, "handle")

        return action()

    def terminate(self):
        pass

    def resolve_commands(self, commands) -> Self:
        all_commands = []

        if len(commands) == 1 and isinstance(commands[0], list):
            all_commands.extend(commands[0])
        else:
            all_commands.extend(commands)

        for command in all_commands:
            self.resolve(command)

        return self

    def resolve(self, command):
        if inspect.isclass(command) and issubclass(command, Command):
            return self.add(self.__app.make(command))

        if isinstance(command, Command):
            return self.add(command)

        return self.add(self.__app.make(command))

    def add(self, command: Command) -> Command:
        command.set_application(self.__app)

        self.command_map[command.name] = command

        return command

    def set_container_command_loader(self) -> Self:
        self.command_loader = ContainerCommandLoader(self.__app, self.command_map)

        return self
