from Illuminate.Collections.helpers import collect
from Illuminate.Contracts.Console.Kernel import Kernel as ConsoleKernelContract
from Illuminate.Foundation.Console.Command import Command
from colorama import Fore


class ListCommands(Command):
    name = "list"
    description = "List all commands"

    def handle(self):
        kernel = self.application.make(ConsoleKernelContract)

        commander = kernel.get_commander()

        padding = 4

        self.info(f"Flight Framework {self.commander.version}")

        self.new_line()

        self.info(f"Usage:")

        self.line(" " * padding + f"Commands [options] [arguments]")

        self.new_line()

        self.info(f"Options:")

        max_length = self._get_max_length(self.options, commander.command_map.items())

        description_start = padding + max_length + padding

        for option in self.options:
            description_text = Fore.WHITE + option["description"]

            self.success(
                " " * padding
                + option["name"].ljust(description_start + padding)
                + description_text
            )

        self.new_line()

        self.info(f"Available Commands:")

        commands = collect(commander.command_map).group_by(lambda item: item.segment)

        for group_key, group_commands in commands:
            if group_key:
                self.info(group_key.rjust(padding + 4))

            for key, item in group_commands:
                if not item.hidden:
                    description_text = Fore.WHITE + item.description

                    self.success(
                        " " * padding
                        + item.name.ljust(description_start + padding)
                        + description_text
                    )

        self.new_line()

        exit()

    def _get_max_length(self, options: list, commands: list):
        max_option_length = max(len(option["name"]) for option in options)

        max_command_length = max(
            len(item.name) for key, item in commands if not item.hidden
        )

        return max([max_option_length, max_command_length])
