from Illuminate.Contracts.Foundation.Application import Application


class RegisterProviders:
    def bootstrap(self, app: Application) -> None:
        self.__app = app

        self.__app.register_configured_providers()
