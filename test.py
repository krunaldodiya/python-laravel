import inspect

from importlib import import_module


def get_instance(info):
    module = import_module(info.__module__)
    Module_class = getattr(module, info.__name__)

    return Module_class()


class Hello:
    def __init__(self) -> None:
        self.name = "hello"


class Test:
    def __init__(self, hello: Hello) -> None:
        self.hello = hello


info = inspect.getfullargspec(Test)

dependencies = [
    get_instance(info.annotations[arg]) for arg in info.args if arg != "self"
]

test = Test(*dependencies)

print(test.hello.name)
