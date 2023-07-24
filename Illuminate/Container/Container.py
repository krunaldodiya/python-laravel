from abc import ABC, abstractmethod
from importlib import import_module
import inspect
from typing import Any, Dict, TypeVar
from inspect import getfullargspec, signature


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
    def make(self, key: str, make_args: Dict[str, Any] = {}) -> Any:
        try:
            base_key = self.get_base_key(key)
            abstract = self.get_alias(base_key)

            return self.__make(abstract, make_args)
        except Exception as e:
            raise Exception(e)

    def __make(self, abstract: str, make_args: Dict[str, Any] = {}) -> Any:
        try:
            instance = self.__resolve_binding_if_exists(abstract, make_args)

            if instance:
                return instance

            instance = self.get_instance(abstract)

            if instance and not make_args:
                return instance

            instance = self.__resolve_class_if_exists(abstract, make_args)

            return instance
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
        abstract = self.get_alias(base_key)

        self.__bindings[abstract] = {
            "abstract": abstract,
            "binding_resolver": binding_resolver,
            "shared": shared,
        }

    def __make_instance(self, abstract, instance):
        self.__instances[abstract] = instance
        return instance

    def __resolve_binding_if_exists(
        self, abstract: str, make_args: Dict[str, Any] = {}
    ):
        binding = self.__bindings.get(abstract)

        if not binding:
            return None

        binding_resolver = binding["binding_resolver"]

        shared = binding["shared"]

        if shared and (abstract in self.__instances):
            return self.__instances[abstract]

        instance = self.__resolve(abstract, binding_resolver, make_args)

        if shared:
            self.__instances[abstract] = instance

        return instance

    def __check_if_module_exists(self, abstract: str):
        splitted = abstract.rsplit(".", 1)

        if len(splitted) < 2:
            raise Exception(f"class {abstract} not found")

        return splitted[0], splitted[1]

    def __resolve_class_if_exists(
        self, abstract: str, make_args: Dict[str, Any] = {}
    ) -> Any:
        try:
            module_path, class_name = self.__check_if_module_exists(abstract)

            module = import_module(module_path)

            binding_resolver = getattr(module, class_name)

            instance = self.__resolve(abstract, binding_resolver, make_args)

            return instance
        except Exception as e:
            raise Exception(e)

    def __resolve(
        self,
        abstract: str,
        binding_resolver: Any,
        make_args: Dict[str, Any],
    ) -> Any:
        instance = None

        if inspect.isfunction(binding_resolver):
            total_params = len(signature(binding_resolver).parameters)

            if total_params >= 2:
                instance = binding_resolver(self, make_args)
            elif total_params == 1:
                instance = binding_resolver(self)
            else:
                instance = binding_resolver()

        if inspect.isclass(binding_resolver):
            dependencies = (
                make_args if make_args else self.get_dependencies(binding_resolver)
            )

            instance = binding_resolver(**dependencies)

        if instance:
            self.__resolved[abstract] = True
            return instance
        else:
            raise BindingResolutionException("Binding Resolution Exception")

    def get_dependencies(self, class_info):
        args_info = getfullargspec(class_info)

        return {
            arg: self.make(args_info.annotations[arg])
            for arg in args_info.args
            if arg != "self"
        }
