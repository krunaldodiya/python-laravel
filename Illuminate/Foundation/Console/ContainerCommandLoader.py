from typing import Dict
from Illuminate.Foundation.Console.Command import Command
from Illuminate.Foundation.Console.Input.ArgvInput import ArgvInput


class ContainerCommandLoader:
    def __init__(self, app, command_map: Dict[str, Command] = {}):
        self.app = app
        self.command_map: Dict[str, Command] = command_map

    def get_current_command(self, command: ArgvInput) -> Command:
        command_name = command.get_first_argument()

        if not command_name:
            return self.handle_invalid_command(command)

        try:
            return self.command_map[command_name]
        except KeyError:
            return self.handle_invalid_command(command)

    def handle_invalid_command(self, command: ArgvInput):
        print("Invalid command, available commands are:")
        print("-----------------------------")

        for item in self.command_map.values():
            if not item.hidden:
                print(item.name)
        print("-----------------------------")
        exit()
