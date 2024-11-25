import re

from abc import abstractmethod
from typing import Any
from Illuminate.Contracts.Foundation.Application import Application
from Illuminate.Foundation.Console.Input.ArgvInput import ArgvInput


class Command:
    name: str | None = None
    signature: str | None = None
    description: str | None = None
    hidden = False
    silent = False

    def __init__(self):
        self.name = self.parse_command_name()

        self.arguments = sorted(
            self.parse_command_arguments(), key=lambda x: x["optional"]
        )

        self.options = self.parse_command_options()

        self.input_arguments = []

        self.input_options = []

        self.application = None

    @abstractmethod
    def handle(self):
        raise NotImplementedError("Not Implemented")

    def root_namespace(self):
        return self.application.app_path()

    def parse_command_name(self):
        return self.name if self.name else self.signature.split(" ")[0]

    def parse_command_arguments(self):
        if not self.signature:
            return []

        argument_pattern = r"\{(\w+)(\?)?(?:=(.*?))?\}"

        matches = re.findall(argument_pattern, self.signature)

        arguments = [
            {
                "name": match[0],
                "optional": bool(match[1]),
                "type": "value",
                "default_value": match[2] if match[2] != "" else None,
                "value": None,
            }
            for match in matches
        ]

        return arguments

    def parse_command_options(self):
        if not self.signature:
            return []

        option_pattern = r"--(\w+)(?:=(.*?))?"

        matches = re.findall(option_pattern, self.signature)

        options = [
            {
                "name": match[0],
                "type": "flag" if not match[1] else "value",
                "optional": True,
                "default_value": False if not match[1] else match[1],
                "value": None,
            }
            for match in matches
        ]

        return options

    def set_application(self, application: Application):
        self.application = application

    def argument(self, name: str) -> Any:
        return self.__get_input_value(name, self.arguments)

    def option(self, name: str):
        return self.__get_input_value(name, self.options)

    def __get_input_value(self, name: str, inputs: list):
        exists = [input for input in inputs if input["name"] == name]

        return exists[0]["value"] if len(exists) == 1 else None

    def validate(self, input: ArgvInput):
        self.parse_input(input)

        self.parse_arguments()

        self.parse_options()

    def parse_input(self, input: ArgvInput):
        arguments = input.get_arguments()

        self.input_arguments = arguments[1::]

        self.input_options = input.get_options()

    def parse_arguments(self):
        def validate_argument(input_argument, item):
            if not item["optional"] and not input_argument:
                raise Exception(f"{item['name']} is required")

            item["value"] = input_argument if input_argument else item["default_value"]

        for argument in self.arguments:
            try:
                input_argument = self.input_arguments.pop(0)
            except IndexError:
                input_argument = None

            validate_argument(input_argument, argument)

    def parse_options(self):
        while True:
            try:
                input_option = self.input_options.pop(0)

                input_option_data = input_option[2::].split("=")

                assert len(input_option_data) <= 2, "Invalid option"

                input_option_name = input_option_data[0]

                input_option_value = (
                    True if len(input_option_data) == 1 else input_option_data[1]
                )

                for option in self.options:
                    if option["name"] == input_option_name:
                        option["value"] = input_option_value
                    else:
                        option["value"] = option["default_value"]
            except IndexError:
                break

    def call_silent(self, command: str, arguments: dict = {}):
        return self.call(command, arguments, True)

    def call(self, command: str, arguments: dict = {}, silent=False):
        self.silent = silent

        data = [command, *list(arguments.values())]

        argv_input = ArgvInput.from_inputs(data)

        results = self.application.handle_command(argv_input)

        return results
