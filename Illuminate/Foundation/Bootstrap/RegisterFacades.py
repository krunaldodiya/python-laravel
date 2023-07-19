from typing import TYPE_CHECKING, Type

from Illuminate.Support.Facades.Facade import Facade

if TYPE_CHECKING:
    from Illuminate.Foundation.Application import Application


class RegisterFacades:
    def bootstrap(self, app: Type["Application"]) -> None:
        Facade.set_facade_application(app)
