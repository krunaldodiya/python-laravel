from typing import Iterator


from Illuminate.Support.Foundation.Container import Container
from Illuminate.Support.Foundation.Kernel import Kernel
from Illuminate.Support.Foundation.response_handler import ResponseHandler

from Illuminate.Providers.FrameworkServiceProvider import FrameworkServiceProvider
from Illuminate.Providers.RouteServiceProvider import RouteServiceProvider
from Illuminate.Providers.ViewServiceProvider import ViewServiceProvider

PROVIDERS = [
    FrameworkServiceProvider,
    RouteServiceProvider,
    ViewServiceProvider,
]


class Application(Container):
    def __init__(self) -> None:
        super().__init__()

        self.__response_handler: ResponseHandler

        self.__providers = []

        self.__config = {"providers": PROVIDERS}

    @property
    def providers(self):
        return self.__providers

    def register_kernel(self):
        kernel = Kernel(self)

        self.singleton("kernel", lambda: kernel)

        kernel.register()

        return self

    def register_providers(self):
        for provider_class in self.__config["providers"]:
            provider = provider_class(self)
            self.providers.append(provider)

        for provider in self.providers:
            provider.register()

        for provider in self.providers:
            provider.boot()

        return self

    def set_response_handler(self, response_handler: ResponseHandler):
        self.__response_handler = response_handler

    def __call__(self, *args, **kwargs) -> Iterator:
        return self.__response_handler(*args, **kwargs)
