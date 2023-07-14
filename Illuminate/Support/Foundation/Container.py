import inspect
from typing import Any, Dict, List


class Container:
    def __init__(self) -> None:
        self.__bindings = {}
        self.__singletons = {}

    @property
    def bindings(self):
        return self.__bindings

    @property
    def singletons(self):
        return self.__singletons

    def make(self, key: str, args: List[Any] = []):
        make_args = args if args else []

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

    def __resolve(self, key: str, make_args: List[Any]):
        try:
            base_key = self.__get_base_key(key)

            binding = self.__bindings.get(base_key, None)

            if not binding:
                raise Exception("No binding found for.", base_key)

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

    def __resolve_binding(self, binding: Dict[str, Any], make_args: List[Any]):
        try:
            binding_resolver = binding["binding_resolver"]

            if self.__is_function(binding_resolver):
                return binding_resolver()

            if self.__is_class(binding_resolver):
                return binding_resolver(*make_args)

            raise Exception("done")
        except Exception as e:
            raise Exception(e)

    def __is_function(self, key):
        return inspect.isfunction(key)

    def __is_class(self, key):
        return isinstance(key, type) and inspect.isclass(key)

    def __is_string(self, key):
        return isinstance(key, str)

    def __get_base_key(self, key):
        return key if self.__is_string(key) else key.__module__ + key.__name__
