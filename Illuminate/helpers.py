import importlib
from pathlib import Path


def config(key=None):
    if not key:
        raise Exception("testing")

    parts = key.split(".")

    file_name = parts[0]

    file_path = Path(f"config/{file_name}.py")

    if not file_path.is_file():
        raise Exception("file not found")

    spec = importlib.util.spec_from_file_location("module_name", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module.data
