from sys import argv
from typing import Self


class ArgvInput:
    def __init__(self):
        self.__inputs = argv[1:] if len(argv) > 1 else []

    def set_inputs(self, inputs: list = []):
        self.__inputs = inputs

    def get_all(self):
        return self.__inputs

    def get_options(self):
        return [input for input in self.__inputs if input.startswith("-")]

    def get_arguments(self):
        return [input for input in self.__inputs if not input.startswith("-")]

    def get_first_argument(self):
        arguments = self.get_arguments()

        return arguments[0] if arguments else None

    @classmethod
    def from_inputs(cls, inputs) -> Self:
        instance = cls()

        instance.set_inputs(inputs)

        return instance
