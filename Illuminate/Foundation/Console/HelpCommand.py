from Illuminate.Foundation.Console.Command import Command
from colorama import Fore


class HelpCommand(Command):
    signature = "help {name}"
    description = "help for given command"
    hidden = True

    def handle(self):
        command = self._get_current_command()

        padding = 4

        self.info(f"Description:")

        self.line(" " * padding + command.description)

        self.new_line()

        self.info(f"Usage:")

        options = f" [options] [--] " if len(command.options) > 1 else " "

        arguments = [f"<{argument['name']}>" for argument in command.arguments]

        self.line(" " * padding + f"{command.name}{options}{' '.join(arguments)}")

        self.new_line()

        max_length = self._get_max_length(
            command.options,
            [argument["name"] for argument in command.arguments if not command.hidden],
        )

        description_start = padding + max_length + padding

        if len(command.arguments):
            self.info(f"Arguments:")

            for argument in command.arguments:
                description_text = Fore.WHITE + argument["description"]

                self.success(
                    " " * padding
                    + argument["name"].ljust(description_start + padding)
                    + description_text
                )

            self.new_line()

        self.info(f"Options:")

        for option in command.options:
            description_text = (
                Fore.WHITE + option["description"] if "description" in option else ""
            )

            self.success(
                " " * padding
                + option["name"].ljust(description_start + padding)
                + description_text
            )

        self.new_line()

        exit()

    def _get_current_command(self):
        name = self.get_name_input()

        return self.commander.command_map[name]

    def _get_max_length(self, options: list, arguments: list):
        max_option_length = max(len(option["name"]) for option in options)

        max_argument_length = (
            max(len(argument) for argument in arguments) if len(arguments) else 0
        )

        return max([max_option_length, max_argument_length])
