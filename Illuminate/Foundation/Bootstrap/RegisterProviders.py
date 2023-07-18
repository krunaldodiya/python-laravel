from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from Illuminate.Foundation.Application import Application


class RegisterProviders:
    def bootstrap(self, app: Type["Application"]) -> None:
        app.register_configured_providers()
