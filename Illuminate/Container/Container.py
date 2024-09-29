import inspect

from abc import ABC, abstractmethod
from importlib import import_module
from typing import Any, Dict, Callable, Optional
from inspect import signature, getfullargspec


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
        self.__resolved: Dict[str, bool] = {}
        self.__aliases: Dict[str, str] = {}
        self.__abstract_aliases: Dict[str, list] = {}

    @abstractmethod
    def bind(self, key: str, binding_resolver: Callable) -> None:
        self.__bind(key, binding_resolver, False)

    @abstractmethod
    def singleton(self, key: str, binding_resolver: Callable) -> None:
        self.__bind(key, binding_resolver, True)

    @abstractmethod
    def make(self, key: str, make_args: Optional[Dict[str, Any]] = None) -> Any:
        make_args = make_args or {}
        base_key = self.get_base_key(key)
        abstract = self.get_alias(base_key)

        return self.__make(abstract, make_args)

    def __make(self, abstract: str, make_args: Dict[str, Any] = {}) -> Any:
        instance = self.__resolve_binding_if_exists(abstract, make_args)

        if instance:
            return instance

        instance = self.get_instance(abstract)

        if instance and not make_args:
            return instance

        return self.__resolve_class_if_exists(abstract, make_args)

    def bind_if(self, key: str, binding_resolver: Callable) -> None:
        if not self.bound(key):
            self.__bind(key, binding_resolver, False)

    def bound(self, key: str) -> Optional[Any]:
        base_key = self.get_base_key(key)
        abstract = self.get_alias(base_key)

        binding = self.__bindings.get(abstract)
        instance = self.__instances.get(abstract)

        return instance if binding and instance else None

    def instance(self, key: str, instance: Any) -> Any:
        base_key = self.get_base_key(key)
        abstract = self.get_alias(base_key)
        return self.__make_instance(abstract, instance)

    def alias(self, abstract_alias: str, alias: str) -> None:
        if abstract_alias == alias:
            raise Exception(f"{abstract_alias} cannot alias itself")

        base_key = self.get_base_key(alias)
        self.__aliases[base_key] = abstract_alias
        self.__abstract_aliases.setdefault(abstract_alias, []).append(base_key)

    def get_alias(self, abstract: str) -> str:
        return self.__aliases.get(abstract, abstract)

    def get_aliases(self) -> Dict[str, str]:
        return self.__aliases

    def get_abstract_aliases(self) -> Dict[str, list]:
        return self.__abstract_aliases

    def get_bindings(self) -> Dict[str, Dict[str, Any]]:
        return self.__bindings

    def get_instance(self, key: str) -> Optional[Any]:
        return self.__instances.get(key)

    def get_instances(self) -> Dict[str, Any]:
        return self.__instances

    def get_resolved(self) -> Dict[str, bool]:
        return self.__resolved

    def get_base_key(self, key: Any) -> str:
        if isinstance(key, str):
            return key
        if callable(key):
            return f"{key.__module__}.{key.__name__}"
        raise Exception("Invalid key type")

    def __bind(self, key: str, binding_resolver: Callable, shared: bool) -> None:
        base_key = self.get_base_key(key)
        abstract = self.get_alias(base_key)

        self.__bindings[abstract] = {
            "abstract": abstract,
            "binding_resolver": binding_resolver,
            "shared": shared,
        }

    def __make_instance(self, abstract: str, instance: Any) -> Any:
        self.__instances[abstract] = instance
        return instance

    def __resolve_binding_if_exists(
        self, abstract: str, make_args: Dict[str, Any] = {}
    ) -> Optional[Any]:
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

    def __check_if_module_exists(self, abstract: str) -> tuple:
        splitted = abstract.rsplit(".", 1)

        if len(splitted) < 2:
            raise Exception(f"Class {abstract} not found")

        return splitted[0], splitted[1]

    def __resolve_class_if_exists(
        self, abstract: str, make_args: Dict[str, Any] = {}
    ) -> Any:
        try:
            module_path, class_name = self.__check_if_module_exists(abstract)

            module = import_module(module_path)

            binding_resolver = getattr(module, class_name)

            return self.__resolve(abstract, binding_resolver, make_args)
        except Exception as e:
            raise BindingResolutionException(f"Error resolving class: {str(e)}")

    def __resolve(
        self,
        abstract: str,
        binding_resolver: Callable,
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
            raise BindingResolutionException(
                f"Binding Resolution Exception for key {abstract} and class {binding_resolver}"
            )

    def get_dependencies(self, class_info) -> Dict[str, Any]:
        args_info = getfullargspec(class_info)

        return {
            arg: self.make(args_info.annotations[arg])
            for arg in args_info.args
            if arg != "self"
        }

    def get_resolved_dependencies(self, abstract: str) -> Dict[str, Any]:
        if abstract not in self.__resolved:
            raise BindingResolutionException(f"{abstract} is not resolved")

        return {abstract: self.__instances.get(abstract)}

    def clear_resolved(self) -> None:
        self.__resolved.clear()

    def __bind(self, key: str, binding_resolver: Any, shared: bool) -> None:
        base_key = self.get_base_key(key)
        abstract = self.get_alias(base_key)

        self.__bindings[abstract] = {
            "abstract": abstract,
            "binding_resolver": binding_resolver,
            "shared": shared,
        }

    def instance(self, key: str, instance: Any) -> Any:
        base_key = self.get_base_key(key)
        abstract = self.get_alias(base_key)

        return self.__make_instance(abstract, instance)

    def __make_instance(self, abstract: str, instance: Any) -> Any:
        self.__instances[abstract] = instance
        return instance

    def alias(self, abstract_alias: str, alias: str) -> None:
        if abstract_alias == alias:
            raise Exception(f"{abstract_alias} is aliased to itself")

        base_key = self.get_base_key(alias)

        self.__aliases[base_key] = abstract_alias
        self.__abstract_aliases.setdefault(abstract_alias, []).append(base_key)

    def get_alias(self, abstract: str) -> str:
        try:
            alias = self.__aliases[abstract]
            return self.get_alias(alias)
        except KeyError:
            return abstract

    def get_bindings(self) -> Dict[str, Any]:
        return self.__bindings

    def get_instances(self) -> Dict[str, Any]:
        return self.__instances

    def get_resolved(self) -> Dict[str, bool]:
        return self.__resolved

    def get_aliases(self) -> Dict[str, str]:
        return self.__aliases

    def get_abstract_aliases(self) -> Dict[str, Any]:
        return self.__abstract_aliases

    def bound(self, key: str) -> bool:
        base_key = self.get_base_key(key)
        abstract = self.get_alias(base_key)

        binding = self.__bindings.get(abstract)
        instance = self.__instances.get(abstract)

        return binding is not None and instance is not None

    def has(self, key: str) -> bool:
        base_key = self.get_base_key(key)
        abstract = self.get_alias(base_key)

        return abstract in self.__bindings

    def forget_instance(self, key: str) -> None:
        base_key = self.get_base_key(key)
        abstract = self.get_alias(base_key)

        if abstract in self.__instances:
            del self.__instances[abstract]

    def forget_binding(self, key: str) -> None:
        base_key = self.get_base_key(key)
        abstract = self.get_alias(base_key)

        if abstract in self.__bindings:
            del self.__bindings[abstract]
            self.forget_instance(abstract)

    def reset(self) -> None:
        self.__bindings.clear()
        self.__instances.clear()
        self.__resolved.clear()
        self.__aliases.clear()
        self.__abstract_aliases.clear()
