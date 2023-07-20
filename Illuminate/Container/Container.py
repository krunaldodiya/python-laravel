from abc import ABC, abstractmethod
from importlib import import_module
from typing import Any, Dict, TypeVar

import inspect
import re


class AttributeNotFound(Exception):
    pass


class BindingNotFound(Exception):
    pass


class BindingResolutionException(Exception):
    pass


class BuildingNewInstanceRequired(Exception):
    pass


class Container(ABC):
    def __init__(self) -> None:
        self.__bindings: Dict[str, Dict[str, Any]] = {}
        self.__instances: Dict[str, Any] = {}
        self.__resolved = {}
        self.__aliases = {}
        self.__abstract_aliases = {}

    @abstractmethod
    def bind(self, key: str, binding_resolver: Any) -> None:
        return self.__bind(key, binding_resolver, False)

    @abstractmethod
    def singleton(self, key: str, binding_resolver: Any) -> None:
        return self.__bind(key, binding_resolver, True)

    @abstractmethod
    def make(self, abstract: str, make_args: Dict[str, Any] = {}) -> Any:
        try:
            instance = self.__get_binding_if_exists(abstract, make_args)

            if instance:
                return self.__make_instance(abstract, instance)

            binding_resolver = self.__get_class_if_exists(abstract)

            return self.__resolve_binding(binding_resolver, make_args)
        except Exception as e:
            raise Exception(e)

    def instance(self, key, instance):
        base_key = self.get_base_key(key)
        abstract = self.get_alias(base_key)

        return self.__make_instance(abstract, instance)

    def alias(self, abstract_alias: str, alias: TypeVar("T")):
        if abstract_alias == alias:
            raise Exception(f"{abstract_alias} is aliased to itself")

        base_key = self.get_base_key(alias)

        self.__aliases[base_key] = abstract_alias
        self.__abstract_aliases[abstract_alias] = []
        self.__abstract_aliases[abstract_alias].append(base_key)

    def get_alias(self, abstract):
        try:
            alias = self.__aliases[abstract]
            return self.get_alias(alias)
        except KeyError:
            return abstract

    def get_aliases(self):
        return self.__aliases

    def get_abstract_aliases(self):
        return self.__abstract_aliases

    def get_bindings(self):
        return self.__bindings

    def get_instance(self, key):
        return self.__instances.get(key)

    def get_instances(self):
        return self.__instances

    def get_resolved(self):
        return self.__resolved

    def get_base_key(self, key: Any) -> str:
        if isinstance(key, str):
            return key

        if callable(key):
            return f"{key.__module__}.{key.__name__}"

        raise Exception("Invalid key type")

    def __bind(self, key: str, binding_resolver: Any, shared: bool):
        base_key = self.get_base_key(key)

        self.__bindings[base_key] = {
            "base_key": base_key,
            "binding_resolver": binding_resolver,
            "shared": shared,
        }

    def __make_instance(self, abstract, instance):
        self.__instances[abstract] = instance
        self.__resolved[abstract] = True

        return instance

    def __get_binding_if_exists(self, base_key: str, make_args: Dict[str, Any] = {}):
        binding = self.__bindings.get(base_key)
        instance = self.__instances.get(base_key)

        if binding and (not instance or not make_args):
            shared = binding["shared"]
            binding_resolver = binding["binding_resolver"]

            if not instance or not shared:
                instance = self.__resolve_binding(binding_resolver, make_args)

            return instance

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

    def __resolve_binding(
        self, binding_resolver: Any, make_args: Dict[str, Any] = {}
    ) -> Any:
        if make_args:
            return binding_resolver(**make_args)

        if callable(binding_resolver):
            if inspect.isclass(binding_resolver):
                dependencies = self.get_dependencies(binding_resolver)
                return binding_resolver(*dependencies)

            return binding_resolver()

        raise BindingResolutionException("Binding Resolution Exception")

    def get_dependencies(self, class_info):
        args_info = inspect.getfullargspec(class_info)

        return [
            self.make(args_info.annotations[arg])
            for arg in args_info.args
            if arg != "self"
        ]
