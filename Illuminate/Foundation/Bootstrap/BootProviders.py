from Illuminate.Contracts.Foundation.Application import Application


class BootProviders:
    def bootstrap(self, app: Application) -> None:
        self.__app = app

        self.__app.boot()
