from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from Illuminate.Foundation.Application import Application


class RegisterFacades:
    def bootstrap(self, app: Type["Application"]) -> None:
        pass
