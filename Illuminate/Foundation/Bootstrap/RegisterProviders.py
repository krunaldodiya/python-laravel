from Illuminate.Contracts.Foundation.Application import Application


class RegisterProviders:
    def bootstrap(self, app: Application) -> None:
        app.register_configured_providers()
