from Illuminate.Contracts.Foundation.Application import Application


class RegisterProviders:
    _merge: list = []

    def bootstrap(self, app: Application) -> None:
        self.__app = app

        self._merge_additional_providers(self.__app)

        self.__app.register_configured_providers()

    def _merge_additional_providers(self, app):
        config = app.make("config")

        providers = config.get("app.providers", [])

        for provider in providers:
            if provider not in self._merge:
                self._merge.append(provider)

        config.set("app.providers", self._merge)

        self._merge = []

    @classmethod
    def merge(cls, providers):
        for provider in providers:
            if providers not in cls._merge:
                cls._merge.append(provider)
