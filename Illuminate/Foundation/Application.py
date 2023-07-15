from typing import Any, Iterator
from Illuminate.Event.EventServiceProvider import EventServiceProvider
from Illuminate.Log.LogServiceProvider import LogServiceProvider
from Illuminate.Routing.RoutingServiceProvider import RoutingServiceProvider


from Illuminate.Container.Container import Container
from Illuminate.Foundation.response_handler import ResponseHandler

from Illuminate.Providers.FrameworkServiceProvider import FrameworkServiceProvider
from Illuminate.Providers.ViewServiceProvider import ViewServiceProvider

PROVIDERS = [
    FrameworkServiceProvider,
    ViewServiceProvider,
]


class Application(Container):
    def __init__(self, environ, response_handler) -> None:
        super().__init__()

        self.__base_path: str = None

        self.__environ: dict = environ

        self.__response_handler: ResponseHandler = response_handler

        self.__providers = []

        self.__register_base_bindings()
        self.__register_base_providers()

    @property
    def base_path(self):
        return self.__base_path

    @property
    def providers(self):
        return self.__providers

    def set_base_path(self, base_path):
        self.__base_path = base_path

    def __register_base_bindings(self):
        self.bind("app", lambda: self)

    def __register_base_providers(self):
        self.__register_provider(EventServiceProvider(self))
        self.__register_provider(LogServiceProvider(self))
        self.__register_provider(RoutingServiceProvider(self))

    def __register_provider(self, provider):
        self.providers.append(provider)
        provider.register()

    def bind(self, *args, **kwargs) -> None:
        return super().bind(*args, **kwargs)

    def singleton(self, *args, **kwargs) -> None:
        return super().singleton(*args, **kwargs)

    def make(self, *args, **kwargs) -> Any:
        return super().make(*args, **kwargs)

    def instance(self) -> Any:
        return self
