from Illuminate.Contracts.Foundation.Application import Application
from Illuminate.Exceptions.Handler import Handler


class HandleExceptions:
    def bootstrap(self, app: Application) -> None:
        self.__app = app

        self.__app.singleton("exception_handler", lambda app: Handler(self.__app))
