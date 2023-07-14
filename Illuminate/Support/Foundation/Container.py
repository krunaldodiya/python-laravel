from importlib import import_module
import inspect
from typing import Any, Dict


class Container:
    def __init__(self) -> None:
        self.__bindings: Dict[str, Dict[str, Any]] = {}
        self.__singletons: Dict[str, Any] = {}

    def make(self, key: str, make_args: Dict[str, Any] = {}) -> Any:
        try:
            if make_args:
                return key(**make_args)

            base_key = self.__get_base_key(key)

            binding = self.__bindings.get(base_key)

            if binding:
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

            module = self.__check_module_exists(base_key)

            return self.__load_module(module, {})
        except Exception as e:
            print("make", e)
            exit()

    def __check_module_exists(self, base_key: str) -> None:
        try:
            print(base_key)

            splitted = [spl for spl in base_key.rsplit(".", 1) if len(spl)]

            if len(splitted) == 0:
                raise Exception(f"Class does not exist")

            if len(splitted) == 1:
                raise Exception(f"Class does not exist")

            module_path, class_name = splitted

            module = import_module(module_path)

            return getattr(module, class_name)
        except Exception:
            raise Exception("Invalid arguments")

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

    def __load_module(self, binding_resolver: Any, make_args: Dict[str, Any]) -> Any:
        try:
            return self.__resolve_binding(binding_resolver, make_args)
        except Exception:
            raise Exception(f"Class does not exist")

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
        try:
            args_info = inspect.getfullargspec(class_info)

            return [
                self.make(args_info.annotations[arg])
                for arg in args_info.args
                if arg != "self"
            ]
        except Exception as e:
            print("__get_dependencies", e)
            exit()
