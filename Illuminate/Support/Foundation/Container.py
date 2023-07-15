from abc import ABC, abstractmethod
from importlib import import_module
import inspect
import re
from typing import Any, Dict


class AttributeNotFound(Exception):
    pass


class BindingNotFound(Exception):
    pass


class BindingResolutionException(Exception):
    pass


class Container(ABC):
    def __init__(self) -> None:
        self.__bindings: Dict[str, Dict[str, Any]] = {}
        self.__singletons: Dict[str, Any] = {}

    @abstractmethod
    def bind(self, key: str, binding_resolver: Any) -> None:
        base_key = self.__get_base_key(key)

        self.__bindings[base_key] = {
            "base_key": base_key,
            "binding_resolver": binding_resolver,
            "is_singleton": False,
        }

    @abstractmethod
    def singleton(self, key: str, binding_resolver: Any) -> None:
        base_key = self.__get_base_key(key)

        self.__bindings[base_key] = {
            "base_key": base_key,
            "binding_resolver": binding_resolver,
            "is_singleton": True,
        }

    @abstractmethod
    def make(self, key: str, make_args: Dict[str, Any] = {}) -> Any:
        try:
            base_key = self.__get_base_key(key)
            return self.__get_binding_if_exists(base_key, make_args)
        except BindingNotFound:
            binding_resolver = self.__get_class_if_exists(base_key)
            return self.__resolve_binding(binding_resolver, make_args)

    def __get_binding_if_exists(self, base_key: str, make_args: Dict[str, Any] = {}):
        binding = self.__bindings.get(base_key)

        if not binding:
            raise BindingNotFound("Binding not found.")

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

    def __validate_class_string(self, base_key: str):
        return bool(re.match(r"^[\w]+\.[A-Z][\w]+$", base_key))

    def __get_class_if_exists(self, base_key: str) -> Any:
        valid_class_path = self.__validate_class_string(base_key)

        if not valid_class_path:
            raise AttributeNotFound("Attribute not found.")

        module_path, class_name = base_key.rsplit(".", 1)

        module = import_module(module_path)

        return getattr(module, class_name)

    def __get_base_key(self, key: Any) -> str:
        if isinstance(key, str):
            return key

        return f"{key.__module__}.{key.__name__}"

    def __resolve_binding(
        self, binding_resolver: Any, make_args: Dict[str, Any] = {}
    ) -> Any:
        if make_args:
            return binding_resolver(**make_args)

        if callable(binding_resolver):
            if inspect.isclass(binding_resolver):
                dependencies = self.__get_dependencies(binding_resolver)
                return binding_resolver(*dependencies)

            return binding_resolver()

        raise BindingResolutionException("Binding Resolution Exception")

    def __get_dependencies(self, class_info):
        args_info = inspect.getfullargspec(class_info)

        return [
            self.make(args_info.annotations[arg])
            for arg in args_info.args
            if arg != "self"
        ]
