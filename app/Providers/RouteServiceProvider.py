from typing import TYPE_CHECKING, Type

from Illuminate.Foundation.Support.Providers.RouteServiceProvider import (
    RouteServiceProvider as ServiceProvider,
)
from Illuminate.Support.Facades.Route import Route

if TYPE_CHECKING:
    from Illuminate.Foundation.Application import Application


class RouteServiceProvider(ServiceProvider):
    def __init__(self, app: Type["Application"]) -> None:
        self.__app = app

    def boot(self):
        def load_routes():
            Route.register_path("routes.web")

        self.routes(load_routes)
