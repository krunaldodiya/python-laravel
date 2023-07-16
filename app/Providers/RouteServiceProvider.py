from typing import TYPE_CHECKING, Type

from Illuminate.Foundation.Support.Providers.RouteServiceProvider import (
    RouteServiceProvider as ServiceProvider,
)

if TYPE_CHECKING:
    from Illuminate.Foundation.Application import Application


class RouteServiceProvider(ServiceProvider):
    def __init__(self, app: Type["Application"]) -> None:
        self.__app = app

    def register(self):
        pass

    def boot(self):
        pass
