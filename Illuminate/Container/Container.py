from abc import ABC, abstractmethod
from importlib import import_module
from typing import Any, Dict

import inspect
import re


class AttributeNotFound(Exception):
    pass


class BindingNotFound(Exception):
    pass


class BindingResolutionException(Exception):
    pass


class Container(ABC):
    def __init__(self) -> None:
        self.__bindings: Dict[str, Dict[str, Any]] = {}
        self.__instances: Dict[str, Any] = {}
        self.__resolved = {}

    def __bind(self, key: str, binding_resolver: Any, shared: bool):
        base_key = self.get_base_key(key)

        self.__bindings[base_key] = {
            "base_key": base_key,
            "binding_resolver": binding_resolver,
            "shared": shared,
        }

    @abstractmethod
    def bind(self, key: str, binding_resolver: Any) -> None:
        return self.__bind(key, binding_resolver, False)

    @abstractmethod
    def singleton(self, key: str, binding_resolver: Any) -> None:
        return self.__bind(key, binding_resolver, True)

    @abstractmethod
    def make(self, key: str, make_args: Dict[str, Any] = {}) -> Any:
        try:
            base_key = self.get_base_key(key)
            instance = self.__get_binding_if_exists(base_key, make_args)

            return self.instance(base_key, instance)
        except BindingNotFound:
            binding_resolver = self.__get_class_if_exists(base_key)
            instance = self.__resolve_binding(binding_resolver, make_args)

            return self.instance(base_key, instance)

    def instance(self, key, instance):
        base_key = self.get_base_key(key)

        self.__instances[base_key] = instance
        self.__resolved[base_key] = True

        return instance

    def get_bindings(self):
        return self.__bindings

    def get_instances(self):
        return self.__instances

    def get_resolved(self):
        return self.__resolved

    def __get_binding_if_exists(self, base_key: str, make_args: Dict[str, Any] = {}):
        binding = self.__bindings.get(base_key)

        if not binding:
            raise BindingNotFound("Binding not found.")

        shared = binding["shared"]

        binding_resolver = binding["binding_resolver"]

        instance = self.__instances.get(base_key)

        if not instance or not shared:
            instance = self.__resolve_binding(binding_resolver, make_args)

        return instance

    def __validate_class_string(self, base_key: str):
        return bool(re.match(r"^[\w]+\.[\w]+\.[A-Z][\w.]*$", base_key))

    def __get_class_if_exists(self, base_key: str) -> Any:
        valid_class_path = self.__validate_class_string(base_key)

        if not valid_class_path:
            raise AttributeNotFound("Attribute not found.")

        module_path, class_name = base_key.rsplit(".", 1)

        module = import_module(module_path)

        return getattr(module, class_name)

    def get_base_key(self, key: Any) -> str:
        if isinstance(key, str):
            return key

        if callable(key):
            return f"{key.__module__}.{key.__name__}"

        raise Exception("Invalid key type")

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
