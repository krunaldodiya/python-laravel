from typing import TYPE_CHECKING, Type

from Illuminate.Foundation.Support.Providers.EventServiceProvider import (
    EventServiceProvider as ServiceProvider,
)

if TYPE_CHECKING:
    from Illuminate.Foundation.Application import Application


class EventServiceProvider(ServiceProvider):
    def __init__(self, app: Type["Application"]) -> None:
        self.__app = app

    def boot(self):
        pass
