from abc import ABC
from importlib import import_module
import inspect
from typing import Any, Dict


class Container(ABC):
    def __init__(self) -> None:
        self.__bindings = {}
        self.__singletons = {}

    @property
    def bindings(self):
        return self.__bindings

    @property
    def singletons(self):
        return self.__singletons

    def make(self, key: str, make_args: Dict[str, Any] = {}):
        return self.__resolve(key, make_args)

    def bind(self, key: str, binding_resolver):
        self.__set_binding(
            key,
            binding_resolver,
            False,
        )

    def singleton(self, key: str, binding_resolver):
        self.__set_binding(
            key,
            binding_resolver,
            True,
        )

    def __set_binding(self, key, binding_resolver, singleton):
        try:
            if not (isinstance(key, str) or self.__is_class(key)):
                raise Exception("key should be string or class object")

            base_key = self.__get_base_key(key)

            self.__bindings[base_key] = {
                "base_key": base_key,
                "binding_resolver": binding_resolver,
                "is_singleton": singleton,
            }
        except Exception as e:
            raise Exception(e)

    def __resolve(self, key: str, make_args: Dict[str, Any] = {}):
        try:
            base_key = self.__get_base_key(key)

            binding = self.__bindings.get(base_key, None)

            if not binding:
                return self.__check_module_exists(base_key, make_args)

            is_singleton = binding["is_singleton"]

            resolved_instance = None

            if is_singleton:
                try:
                    resolved_instance = self.__singletons[base_key]
                except KeyError:
                    resolved_instance = self.__resolve_binding(binding, make_args)
                    self.__singletons[base_key] = resolved_instance
            else:
                resolved_instance = self.__resolve_binding(binding, make_args)

            return resolved_instance
        except Exception as e:
            raise Exception(e)

    def __resolve_binding(self, binding: Dict[str, Any], make_args: Dict[str, Any]):
        try:
            binding_resolver = binding["binding_resolver"]

            if self.__is_function(binding_resolver):
                return binding_resolver()

            if self.__is_class(binding_resolver):
                return binding_resolver(**make_args)

            raise Exception("Binding Resolution Exception")
        except Exception as e:
            raise Exception(e)

    def __check_module_exists(self, base_key: str, make_args: Dict[str, Any]):
        try:
            splitted = base_key.split(".")
            module_path, class_name = ".".join(splitted[:-1]), splitted[-1]
            module = import_module(module_path, package=None)
            binding_resolver = getattr(module, class_name)

            return binding_resolver(**make_args)
        except ModuleNotFoundError:
            raise Exception(f"Class {class_name} does not exists")

    def __is_function(self, key):
        return inspect.isfunction(key)

    def __is_class(self, key):
        return isinstance(key, type) and inspect.isclass(key)

    def __is_string(self, key):
        return isinstance(key, str)

    def __get_base_key(self, key):
        return key if self.__is_string(key) else f"{key.__module__}.{key.__name__}"
