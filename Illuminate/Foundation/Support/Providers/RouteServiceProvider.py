from importlib import import_module
from typing import Callable
from Illuminate.Support.Facades.Route import Route
from Illuminate.Support.ServiceProvider import ServiceProvider


class RouteServiceProvider(ServiceProvider):
    def __init__(self) -> None:
        self.__load_routes_using: Callable[[], None]

    def routes(self, callback):
        self.__load_routes_using = callback

        return self

    def register(self):
        self.booted(self.load_routes)

    def load_routes(self):
        self.__load_routes_using()

        for registered_path in Route.get_registered_paths():
            import_module(registered_path)
