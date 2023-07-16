from typing import TYPE_CHECKING, Any, Type

from Illuminate.Event.EventServiceProvider import EventServiceProvider
from Illuminate.Http.Request import Request
from Illuminate.Http.Response import Response
from Illuminate.Log.LogServiceProvider import LogServiceProvider
from Illuminate.Routing.RoutingServiceProvider import RoutingServiceProvider


from Illuminate.Container.Container import Container

from Illuminate.Providers.FrameworkServiceProvider import FrameworkServiceProvider
from Illuminate.Providers.ViewServiceProvider import ViewServiceProvider
from public.server import Server

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
        self.instance("app", self)

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

    async def run_kernel(self, kernel: Type["Kernel"], server: Type["Server"]):
        request: Request = self.make("request")

        response: Response = kernel.handle(request.capture(server))

        await response.send()

        kernel.terminate(request, response)
