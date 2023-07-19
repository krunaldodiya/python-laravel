from pathlib import Path
from typing import Any, Dict
from Illuminate.Events.Dispatcher import Dispatcher

from Illuminate.Events.EventServiceProvider import EventServiceProvider
from Illuminate.Http.Request import Request
from Illuminate.Http.ResponseFactory import ResponseFactory
from Illuminate.Log.LogServiceProvider import LogServiceProvider
from Illuminate.Routing.RoutingServiceProvider import RoutingServiceProvider


from Illuminate.Container.Container import Container

from Illuminate.Providers.FrameworkServiceProvider import FrameworkServiceProvider
from Illuminate.Providers.ViewServiceProvider import ViewServiceProvider

from Illuminate.Routing.Router import Router

PROVIDERS = [
    FrameworkServiceProvider,
    ViewServiceProvider,
]


class Application(Container):
    def __init__(self, base_path=None) -> None:
        super().__init__()

        self.__environment = "local"

        self.__app_path = None
        self.__base_path = None
        self.__config_path = None
        self.__database_path = None
        self.__public_path = None
        self.__resources_path = None
        self.__storage_path = None
        self.__lang_path = None
        self.__bootstrap_path = None

        self.__has_been_bootstrapped = False

        self.__service_providers = {}

        self.__loaded_providers = {}

        self.__container_aliases = {
            "app": [Application, Container],
            "request": [Request],
            "response": [ResponseFactory],
            "router": [Router],
            "events": [Dispatcher],
        }

        if base_path:
            self.set_base_path(base_path)

        self.__register_base_bindings()
        self.__register_base_providers()
        self.__register_container_aliases()

    @property
    def has_been_bootstrapped(self):
        return self.__has_been_bootstrapped

    @property
    def service_providers(self):
        return [provider for provider in self.__service_providers.values()]

    @property
    def loaded_providers(self):
        return self.__loaded_providers

    def bootstrap_with(self, bootstrappers):
        for bootstrapper in bootstrappers:
            self.make(bootstrapper).bootstrap(self)

        self.__has_been_bootstrapped = True

    def set_base_path(self, base_path):
        self.__base_path = base_path
        self.__bind_path_in_container()

        return self

    def join_paths(self, base_path, path):
        return Path().joinpath(base_path, path)

    def base_path(self, path=""):
        return self.join_paths(self.__base_path, path)

    def app_path(self, path=""):
        return self.join_paths(
            self.__app_path if self.__app_path else self.base_path("app"),
            path,
        )

    def use_app_path(self, path):
        self.__app_path = path
        self.instance("path", path)
        return self

    def config_path(self, path=""):
        return self.join_paths(
            self.__config_path if self.__config_path else self.base_path("config"),
            path,
        )

    def use_config_path(self, path):
        self.__config_path = path
        self.instance("path.config", path)
        return self

    def database_path(self, path=""):
        return self.join_paths(
            self.__database_path
            if self.__database_path
            else self.base_path("database"),
            path,
        )

    def use_database_path(self, path):
        self.__database_path = path
        self.instance("path.database", path)
        return self

    def public_path(self, path=""):
        return self.join_paths(
            self.__public_path if self.__public_path else self.base_path("public"),
            path,
        )

    def use_public_path(self, path):
        self.__public_path = path
        self.instance("path.public", path)
        return self

    def resources_path(self, path=""):
        return self.join_paths(
            self.__resources_path
            if self.__resources_path
            else self.base_path("resources"),
            path,
        )

    def use_resources_path(self, path):
        self.__resources_path = path
        self.instance("path.resources", path)
        return self

    def storage_path(self, path=""):
        return self.join_paths(
            self.__storage_path if self.__storage_path else self.base_path("storage"),
            path,
        )

    def use_storage_path(self, path):
        self.__storage_path = path
        self.instance("path.storage", path)
        return self

    def lang_path(self, path=""):
        return self.join_paths(
            self.__lang_path if self.__lang_path else self.base_path("lang"),
            path,
        )

    def use_lang_path(self, path):
        self.__lang_path = path
        self.instance("path.lang", path)
        return self

    def bootstrap_path(self, path=""):
        return self.join_paths(
            self.__bootstrap_path
            if self.__bootstrap_path
            else self.base_path("bootstrap"),
            path,
        )

    def use_bootstrap_path(self, path):
        self.__bootstrap_path = path
        self.instance("path.bootstrap", path)
        return self

    def __bind_path_in_container(self):
        self.instance("path", self.app_path())
        self.instance("path.base", self.base_path())
        self.instance("path.config", self.config_path())
        self.instance("path.database", self.database_path())
        self.instance("path.public", self.public_path())
        self.instance("path.resources", self.resources_path())
        self.instance("path.storage", self.storage_path())
        self.instance("path.lang", self.lang_path())
        self.instance("path.bootstrap", self.bootstrap_path())

    def __register_base_bindings(self):
        self.instance("app", self)
        self.instance(Container, self)

    def __register_base_providers(self):
        self.__register_provider(EventServiceProvider)
        self.__register_provider(LogServiceProvider)
        self.__register_provider(RoutingServiceProvider)

    def __register_provider(self, provider_class):
        base_key = self.get_base_key(provider_class)

        provider = provider_class(self)

        registered = self.get_provider(base_key)

        if registered:
            return registered

        self.__service_providers[base_key] = provider

        provider.register()

        self.__loaded_providers[base_key] = True

    def __register_container_aliases(self):
        for abstract_alias, aliases in self.__container_aliases.items():
            for alias in aliases:
                self.alias(abstract_alias, alias)

    def get_provider(self, base_key):
        return self.__service_providers.get(base_key)

    def bind(self, *args, **kwargs) -> None:
        return super().bind(*args, **kwargs)

    def singleton(self, *args, **kwargs) -> None:
        return super().singleton(*args, **kwargs)

    def make(self, key: str, make_args: Dict[str, Any] = {}) -> Any:
        base_key = self.get_base_key(key)
        abstract = self.get_alias(base_key)

        return super().make(abstract, make_args)

    def register_configured_providers(self) -> Any:
        config = self.make("config")
        providers = config["app.providers"]

        for provider_class in providers:
            self.__register_provider(provider_class)

    def boot(self) -> Any:
        for service_provider in self.service_providers:
            service_provider.boot()

            callback = service_provider.booted_callbacks.get(service_provider.__class__)

            if callback:
                callback()

    def detect_environment(self, callback):
        self.__environment = callback()
