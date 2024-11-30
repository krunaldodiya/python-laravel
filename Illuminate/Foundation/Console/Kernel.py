from datetime import datetime
from typing import Any
from Illuminate.Events.Dispatcher import Dispatcher
from Illuminate.Foundation.Console.Application import Application as Commander
from Illuminate.Foundation.Console.Input.ArgvInput import ArgvInput
from Illuminate.Foundation.Console.Output.ConsoleOutput import ConsoleOutput
from Illuminate.Contracts.Foundation.Application import (
    Application as ApplicationContract,
)
from Illuminate.Foundation.Bootstrap.BootProviders import BootProviders
from Illuminate.Foundation.Bootstrap.HandleExceptions import HandleExceptions
from Illuminate.Foundation.Bootstrap.LoadConfiguration import LoadConfiguration
from Illuminate.Foundation.Bootstrap.LoadEnvironmentVariables import (
    LoadEnvironmentVariables,
)
from Illuminate.Foundation.Bootstrap.RegisterFacades import RegisterFacades
from Illuminate.Foundation.Bootstrap.RegisterProviders import RegisterProviders


class Kernel:
    def __init__(self, app: ApplicationContract, events: Dispatcher) -> None:
        self.__app = app

        self.__events = events

        self.__bootstrappers = [
            LoadEnvironmentVariables,
            LoadConfiguration,
            HandleExceptions,
            RegisterFacades,
            RegisterProviders,
            BootProviders,
        ]

        self.commander: Commander | None = None

        self.commands: list = []

    @property
    def app(self):
        return self.__app

    @property
    def events(self):
        return self.__events

    @property
    def bootstrappers(self):
        return self.__bootstrappers

    def __bootstrap(self):
        try:
            if not self.__app.has_been_bootstrapped():
                self.__app.bootstrap_with(self.bootstrappers)
        except Exception as e:
            raise e

    def handle(self, input: ArgvInput, output: ConsoleOutput):
        try:
            self.command_started_at = datetime.now()

            self.__bootstrap()

            commander = self.get_commander()

            return commander.run(input, output)
        except Exception as e:
            print(e)

    def get_commander(self):
        if not self.commander:
            self.commander = (
                Commander(self.app, self.events, self.app.version())
                .resolve_commands(self.commands)
                .set_container_command_loader()
            )

        return self.commander

    def terminate(self, input: ArgvInput, response: Any):
        if self.commander:
            self.commander.terminate()
