from typing import Any

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
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)

        return cls.__instance

    def __init__(self) -> None:
        super().__init__()

        self.__base_path: str = None

        self.__environ: dict = None

        self.__response_handler: ResponseHandler = None

        self.__providers = []

        self.__register_base_bindings()

        self.__register_base_providers()

    @property
    def base_path(self):
        return self.__base_path

    @property
    def environ(self):
        return self.__environ

    @property
    def response_handler(self):
        return self.__response_handler

    @property
    def providers(self):
        return self.__providers

    def set_environ(self, environ):
        self.__environ = environ

    def set_response_handler(self, response_handler):
        self.__response_handler = response_handler

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
