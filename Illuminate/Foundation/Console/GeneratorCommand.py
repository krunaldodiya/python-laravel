import re
import os

from pathlib import Path
from Illuminate.Foundation.Console.Command import Command
from Illuminate.Foundation.Console.Input.InputArgument import InputArgument


class GeneratorCommand(Command):
    def handle(self):
        try:
            self.generate_file_from_stub(
                self.get_stub(),
                self.get_path(),
                self.get_stub_vars(),
            )

            self.response()
        except Exception as e:
            self.error(str(e))

    def get_arguments(self):
        return [
            ["name", InputArgument.REQUIRED, f"The name of the {self.type}", None],
        ]

    def response(self):
        if not self.silent:
            self.success(f"{self.type} [{self.get_path()}] created successfully.")

    def get_path(self):
        namespace = self.get_default_namespace(self.root_namespace())

        namespace = str(namespace).rstrip("/")

        name = self.get_name_input()

        return f"{namespace}/{name}.py"

    def resolve_stub_path(self, stub: str, console_path="/"):
        return Path(console_path) / stub.strip("/")

    def get_stub(self):
        pass

    def get_stub_vars(self):
        return {}

    def get_default_namespace(self, root_namespace):
        return root_namespace

    def generate_file_from_stub(self, stub_file, main_file, variables={}):
        os.makedirs(os.path.dirname(main_file), exist_ok=True)

        if os.path.exists(main_file):
            if not self.silent:
                raise Exception(f"{self.type} already exists.")

        with open(stub_file, "r") as stub_file:
            stub_content = stub_file.read()

        modified_content = self.__replace_placeholders(stub_content, variables)

        with open(main_file, "w") as output_file:
            output_file.write(modified_content)

    def __replace_placeholders(self, content, replacements):
        def replacer(match):
            placeholder = match.group(1)

            return replacements.get(placeholder, match.group(0))

        pattern = r"\{\{(\w+)\}\}"

        return re.sub(pattern, replacer, content)
