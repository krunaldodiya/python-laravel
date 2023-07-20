from typing import TYPE_CHECKING, Type

from Illuminate.Foundation.Support.Providers.RouteServiceProvider import (
    RouteServiceProvider as ServiceProvider,
)
from Illuminate.View.ViewFactory import ViewFactory

if TYPE_CHECKING:
    from Illuminate.Foundation.Application import Application


class ViewServiceProvider(ServiceProvider):
    def __init__(self, app: Type["Application"]) -> None:
        self.__app = app

    def register(self):
        self.__app.singleton("view", lambda app: ViewFactory(self.__app))

    def boot(self):
        pass
