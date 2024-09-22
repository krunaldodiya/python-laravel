from Illuminate.Contracts.Foundation.Application import Application


class BootProviders:
    def bootstrap(self, app: Application) -> None:
        app.boot()
