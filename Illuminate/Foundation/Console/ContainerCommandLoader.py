from typing import Dict
from Illuminate.Foundation.Console.Command import Command
from Illuminate.Foundation.Console.Input.ArgvInput import ArgvInput


class ContainerCommandLoader:
    def __init__(self, app, command_map: Dict[str, Command] = {}):
        self.app = app
        self.command_map: Dict[str, Command] = command_map

    def get_current_command(self, io: ArgvInput) -> Command:
        command_name = io.get_first_argument()

        if not command_name:
            return self.handle_invalid_command()

        try:
            return self.command_map[command_name]
        except KeyError:
            return self.handle_invalid_command()

    def handle_invalid_command(self) -> Command:
        return self.command_map["list"]
