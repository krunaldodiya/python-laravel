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


class Application:
    def __init__(self) -> None:
        self.__container: Container = Container()

        self.__response_handler: ResponseHandler

        self.__providers = []

        self.__config = {"providers": PROVIDERS}

    @property
    def providers(self):
        return self.__providers

    def make(self, key: str):
        return self.__container.resolve(key)

    def resolve(self, key: str):
        return self.__container.resolve(key)

    def bind(self, key: str, binding_resolver):
        self.__container.set_binding(
            key,
            binding_resolver,
            False,
        )

    def singleton(self, key: str, binding_resolver):
        self.__container.set_singleton(
            key,
            binding_resolver,
            True,
        )

    def register_kernel(self):
        kernel = Kernel(self)

        self.singleton("kernel", lambda: kernel)

        kernel.register()

        return self

    def register_providers(self):
        for provider_class in self.__config["providers"]:
            provider = provider_class(self)
            provider.register()
            self.providers.append(provider)

        return self

    def set_response_handler(self, response_handler: ResponseHandler):
        self.__response_handler = response_handler

    def __call__(self, *args, **kwargs) -> Iterator:
        return self.__response_handler(*args, **kwargs)
