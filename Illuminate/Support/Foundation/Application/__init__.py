from typing import Iterator


from Illuminate.Support.Foundation.Container import Container
from Illuminate.Support.Foundation.Kernel import Kernel
from Illuminate.Support.Foundation.response_handler import ResponseHandler
from Illuminate.http_request import HttpRequest
from Illuminate.http_response import HttpResponse
from Illuminate.template import Template


class Application:
    def __init__(self) -> None:
        self.__container: Container = Container()

        self.__response_handler: ResponseHandler

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
        self.singleton("request", lambda: HttpRequest())
        self.singleton("response", lambda: HttpResponse())
        self.singleton("view", lambda: Template())

        return self

    def set_response_handler(self, response_handler: ResponseHandler):
        self.__response_handler = response_handler

    def __call__(self, *args, **kwargs) -> Iterator:
        return self.__response_handler(*args, **kwargs)
