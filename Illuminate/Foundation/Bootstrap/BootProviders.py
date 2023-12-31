from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from Illuminate.Foundation.Application import Application


class BootProviders:
    def bootstrap(self, app: Type["Application"]) -> None:
        app.boot()
