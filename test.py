import inspect

from importlib import import_module


class AnotherService:
    def get_name(self):
        return "AnotherService"


class Service:
    def __init__(self, another_service: AnotherService) -> None:
        self.another_service = another_service

    def get_name(self):
        return "Service"


class Test:
    def __init__(self, service: Service) -> None:
        self.service = service


def get_dependencies(class_info):
    def get_instance(info):
        module = import_module(info.__module__)
        module_class = getattr(module, info.__name__)

        return create_instance(module_class)

    def create_instance(class_info):
        dependencies = get_dependencies(class_info)
        return class_info(*dependencies)

    args_info = inspect.getfullargspec(class_info)

    return [
        get_instance(args_info.annotations[arg])
        for arg in args_info.args
        if arg != "self"
    ]


dependencies = get_dependencies(Test)

test = Test(*dependencies)

print(test.service.another_service.get_name())
