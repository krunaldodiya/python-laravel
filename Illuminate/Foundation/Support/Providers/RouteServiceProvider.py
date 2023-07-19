from typing import Any, Callable
from Illuminate.Support.ServiceProvider import ServiceProvider


class RouteServiceProvider(ServiceProvider):
    def __init__(self) -> None:
        super().__init__()

        self.__load_routes_using: Callable[[], None]

    def routes(self, callback):
        self.__load_routes_using = callback

        return self

    def register(self):
        self.booted(self.load_routes)

    def load_routes(self):
        self.__load_routes_using()
