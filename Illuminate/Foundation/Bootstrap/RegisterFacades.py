from Illuminate.Support.Facades.Facade import Facade

from Illuminate.Contracts.Foundation.Application import Application


class RegisterFacades:
    def bootstrap(self, app: Application) -> None:
        Facade.set_facade_application(app)
