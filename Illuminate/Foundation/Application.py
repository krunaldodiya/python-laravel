from typing import TYPE_CHECKING, Any, Dict, Type

from Illuminate.Event.EventServiceProvider import EventServiceProvider
from Illuminate.Http.Request import Request
from Illuminate.Http.Response import Response
from Illuminate.Log.LogServiceProvider import LogServiceProvider
from Illuminate.Routing.RoutingServiceProvider import RoutingServiceProvider


from Illuminate.Container.Container import Container

from Illuminate.Providers.FrameworkServiceProvider import FrameworkServiceProvider
from Illuminate.Providers.ViewServiceProvider import ViewServiceProvider
from public.server import Server

from Illuminate.Routing.Router import Router

PROVIDERS = [
    FrameworkServiceProvider,
    ViewServiceProvider,
]


if TYPE_CHECKING:
    from Illuminate.Foundation.Http.Kernel import Kernel


class Application(Container):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)

        return cls.__instance

    def __init__(self) -> None:
        super().__init__()

        self.__base_path: str = None

        self.__has_been_bootstrapped = False

        self.__service_providers = {}

        self.__loaded_providers = {}

        self.__container_aliases = {
            "app": [Application, Container],
            "request": [Request],
            "response": [Response],
            "router": [Router],
        }

        self.__register_base_bindings()
        self.__register_base_providers()
        self.__register_container_aliases()

    @property
    def base_path(self):
        return self.__base_path

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

    def boot(self) -> Any:
        for service_provider in self.service_providers:
            service_provider.boot()

    async def run_kernel(self, kernel: Type["Kernel"], server: Type["Server"]):
        request: Request = Request.capture(self, server)

        response: Response = kernel.handle(request)

        await response.send()

        kernel.terminate(request, response)
