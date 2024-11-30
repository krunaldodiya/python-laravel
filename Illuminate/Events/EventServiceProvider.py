from typing import TYPE_CHECKING, Type
from Illuminate.Events.Dispatcher import Dispatcher
from Illuminate.Support.ServiceProvider import ServiceProvider

if TYPE_CHECKING:
    from Illuminate.Foundation.Application import Application


class EventServiceProvider(ServiceProvider):
    def __init__(self, app: Type["Application"]) -> None:
        self.__app = app

    def register(self):
        self.__app.singleton("events", lambda app: Dispatcher(self.__app))

    def boot(self):
        pass
