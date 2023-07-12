from importlib import import_module
from pathlib import Path


def load_files(path_string: str):
    path = Path(path_string)

    files = [file for file in path.glob("*.py")]

    for file in files:
        module_path = f"{path}/{file.stem}"
        module_path = module_path.replace("/", ".")

        import_module(module_path, package=None)
