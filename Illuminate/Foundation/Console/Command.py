import re

from abc import abstractmethod
from typing import TYPE_CHECKING, Any
from Illuminate.Foundation.Console.Input.ArgvInput import ArgvInput
from colorama import Fore, Back, Style

from Illuminate.Foundation.Console.Input.InputArgument import InputArgument
from Illuminate.Foundation.Console.Input.InputOption import InputOption
from Illuminate.Helpers.Util import Util

if TYPE_CHECKING:
    from Illuminate.Foundation.Console.Application import Application


class Command:
    name: str = ""
    signature: str = ""
    description: str = ""
    hidden = False
    silent = False

    def __init__(self):
        self.name = self.parse_command_name()

        self.segment = self._get_segment()

        self.options = self.merge_default_options(self.parse_command_options())

        self.arguments = sorted(
            self.parse_command_arguments(), key=lambda x: x["type"].value
        )

        self.input_options = []

        self.input_arguments = []

        self.commander = None

        self.application = None

    def get_default_options(self):
        return [
            [
                "help",
                "h",
                InputOption.VALUE_OPTIONAL,
                "Display help for the given command. When no command is given display help for the list command",
                None,
            ],
        ]

    def merge_default_options(self, options: list):
        default_option = [
            self.transform_options(options) for options in self.get_default_options()
        ]

        options.extend(default_option)

        return options

    def _get_segment(self) -> str:
        items = self.name.split(":")

        if len(items) == 2:
            return items[0]

        return ""

    def set_silent(self, silent: bool = False):
        self.silent = silent

    @abstractmethod
    def handle(self):
        raise NotImplementedError("Not Implemented")

    def root_namespace(self):
        return self.application.app_path()

    def parse_command_name(self):
        return self.name if self.name else self.signature.split(" ")[0]

    def get_name_input(self):
        return self.argument("name").strip()

    def parse_command_arguments(self):
        if not self.signature:
            return [
                self.transform_arguments(arguments)
                for arguments in self.get_arguments()
            ]

        argument_pattern = r"\{(\w+)(\?)?(?:=(.*?))?\}"

        matches = re.findall(argument_pattern, self.signature)

        arguments = [
            {
                "name": match[0],
                "type": (
                    InputArgument.OPTIONAL if bool(match[1]) else InputArgument.REQUIRED
                ),
                "description": "",
                "value": match[2] if match[2] != "" else None,
            }
            for match in matches
        ]

        return arguments

    def parse_command_options(self):
        if not self.signature:
            return [self.transform_options(options) for options in self.get_options()]

        option_pattern = r"\{--(\w+)?\|?(\w+)?(?:=(.*?))?\}"

        matches = re.findall(option_pattern, self.signature)

        options = []

        for match in matches:
            short_name = match[0] if match[0] and match[1] else None
            long_name = match[0] if match[0] and not short_name else match[1]

            option_entry = {
                "short_name": short_name,
                "long_name": long_name,
                "name": self.get_option_name(long_name, short_name),
                "type": InputOption.VALUE_OPTIONAL,
                "description": "",
                "value": (
                    Util.to_boolean(match[2])
                    if isinstance(match[2], str) and len(match[2]) > 0
                    else False
                ),
            }

            options.append(option_entry)

        return options

    def set_commander(self, commander: "Application"):
        self.commander = commander
        self.application = commander.application

    def argument(self, name: str) -> Any:
        return self._get_input_value(name, self.arguments, "argument")

    def option(self, name: str):
        return self._get_input_value(name, self.options, "option")

    def _get_input_value(self, name: str, inputs: list, type: str):
        search = ["name"] if type == "argument" else ["short_name", "long_name"]

        for input in inputs:
            for key in search:
                if key in input and input[key] == name:
                    return input["value"]

        self.error(f"The '{name}' {type} does not exist.")
        exit()

    def get_option_name(self, long_name: str, short_name: str | None = None):
        short_name_title = f"-{short_name}, " if short_name else " "
        long_name_title = f"--{long_name}"

        return f"{short_name_title.rjust(4)}{long_name_title}"

    def parse_input(self, input: ArgvInput):
        arguments = input.get_arguments()

        self.input_options = input.get_options()

        self.input_arguments = arguments[1::]

        self.parse_options()

        self.parse_arguments()

    def validate(self):
        self.validate_arguments()
        self.validate_options()

    def validate_arguments(self):
        for argument in self.arguments:
            if argument["type"] == InputArgument.REQUIRED and not argument["value"]:
                self.error(f"{argument['name']} is required")

    def validate_options(self):
        for option in self.options:
            if option["type"] == InputOption.VALUE_REQUIRED and not option["value"]:
                self.error(f"{option['long_name']} is required")

    def parse_arguments(self):
        for argument in self.arguments:
            try:
                argument["value"] = self.input_arguments.pop(0)
            except IndexError:
                pass

    def parse_options(self):
        while True:
            try:
                input_option = self.input_options.pop(0)

                input_option_long_name = None
                input_option_short_name = None

                if input_option.startswith("--"):
                    input_option_data = input_option[2::].split("=")
                    input_option_long_name = input_option_data[0]
                elif input_option.startswith("-"):
                    input_option_data = input_option[1::].split("=")
                    input_option_short_name = input_option_data[0]
                else:
                    input_option_data = []

                assert len(input_option_data) <= 2, "Invalid option"

                input_option_value = (
                    True if len(input_option_data) == 1 else input_option_data[1]
                )

                for option in self.options:
                    if (
                        input_option_long_name
                        and option["long_name"] == input_option_long_name
                    ) or (
                        input_option_short_name
                        and option["short_name"] == input_option_short_name
                    ):
                        option["value"] = input_option_value
            except IndexError:
                break

    def get_arguments(self):
        return []

    def get_options(self):
        return []

    def line(self, message):
        print(f"{Fore.WHITE}{message}")

    def success(self, message):
        print(f"{Fore.GREEN}{message}")

    def info(self, message):
        print(f"{Fore.YELLOW}{message}")

    def error(self, message):
        horizontal_padding = 3

        vertical_padding = 1

        line_length = len(message) + (2 * horizontal_padding)

        horizontal_pad = " " * horizontal_padding

        padded_message = f"{horizontal_pad}{message}{horizontal_pad}"

        top_bottom_border = " " * line_length

        styled_text = f"{Back.RED}{Fore.WHITE}{Style.BRIGHT}{padded_message}"

        output = (
            f"\n" * vertical_padding
            + f"{Back.RED}{top_bottom_border}\n"
            + styled_text
            + "\n"
            + f"{Back.RED}{top_bottom_border}"
            + f"\n" * vertical_padding
        )

        exit(output)

    def new_line(self, total=1):
        for i in range(0, total):
            print("\n", end="")

    def transform_arguments(self, items: list):
        assert len(items) == 4, "Invalid argument payload"

        [name, type, description, value] = items

        if not name:
            raise Exception("name is required")

        if not isinstance(type, InputArgument):
            raise Exception("type must be enum type of InputArgument")

        return {
            "name": name,
            "type": type,
            "description": description,
            "value": value,
        }

    def transform_options(self, items: list):
        assert len(items) == 5, "Invalid argument payload"

        [long_name, short_name, type, description, value] = items

        if not long_name:
            raise Exception("long_name is required")

        if not isinstance(type, InputOption):
            raise Exception("type must be enum type of InputOption")

        return {
            "long_name": long_name,
            "short_name": short_name,
            "name": self.get_option_name(long_name, short_name),
            "type": type,
            "description": description,
            "value": value,
        }
