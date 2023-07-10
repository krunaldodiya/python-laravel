import importlib
from pathlib import Path

from core.application import Application
from core.controller import Controller


def load_files(path: Path):
    files = [file for file in path.glob("*.py")]

    for file in files:
        module_path = f"{path}/{file.stem}"
        module_path = module_path.replace("/", ".")

        importlib.import_module(module_path, package=None)


load_files(Path("app/Http/Controllers"))
load_files(Path("app/routes"))

application = Application()

for controller in Controller.__subclasses__():
    application.bind(controller.__name__, controller)

test = application.resolve(controller.__name__)

application.boot()

application.run()
