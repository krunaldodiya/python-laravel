from importlib import import_module
import inspect
from typing import Any, Dict


class Container:
    def __init__(self) -> None:
        self.__bindings: Dict[str, Dict[str, Any]] = {}
        self.__singletons: Dict[str, Any] = {}

    def make(self, key: str, make_args: Dict[str, Any] = {}) -> Any:
        base_key = self.__get_base_key(key)
        binding = self.__bindings.get(base_key)

        if not binding:
            test = self.__load_module_if_exists(base_key, make_args)
            print(test)
            exit()

        is_singleton = binding["is_singleton"]

        binding_resolver = binding["binding_resolver"]

        if is_singleton:
            instance = self.__singletons.get(base_key)
            if instance is None:
                instance = self.__resolve_binding(binding_resolver, make_args)
                self.__singletons[base_key] = instance
        else:
            instance = self.__resolve_binding(binding_resolver, make_args)

        return instance

    def bind(self, key: str, binding_resolver: Any) -> None:
        base_key = self.__get_base_key(key)

        self.__bindings[base_key] = {
            "base_key": base_key,
            "binding_resolver": binding_resolver,
            "is_singleton": False,
        }

    def singleton(self, key: str, binding_resolver: Any) -> None:
        base_key = self.__get_base_key(key)

        self.__bindings[base_key] = {
            "base_key": base_key,
            "binding_resolver": binding_resolver,
            "is_singleton": True,
        }

    def __get_base_key(self, key: Any) -> str:
        if isinstance(key, str):
            return key

        return f"{key.__module__}.{key.__name__}"

    def __load_module_if_exists(self, base_key: str, make_args: Dict[str, Any]) -> Any:
        module_path, class_name = base_key.rsplit(".", 1)

        try:
            module = import_module(module_path)
            binding_resolver = getattr(module, class_name)

            return self.__resolve_binding(binding_resolver, make_args)
        except (ModuleNotFoundError, AttributeError):
            raise Exception(f"Class {class_name} does not exist")

    def __resolve_binding(
        self, binding_resolver: Any, make_args: Dict[str, Any]
    ) -> Any:
        if callable(binding_resolver):
            if inspect.isclass(binding_resolver):
                dependencies = self.__get_dependencies(binding_resolver)

                return binding_resolver(*dependencies, **make_args)

            return binding_resolver()

        raise Exception("Binding Resolution Exception")

    def __get_dependencies(self, class_info):
        def get_instance(info):
            module = import_module(info.__module__, package=None)
            module_class = getattr(module, info.__name__)

            return self.make(module_class)

        args_info = inspect.getfullargspec(class_info)

        return [
            get_instance(args_info.annotations[arg])
            for arg in args_info.args
            if arg != "self"
        ]
