from Illuminate.http_request import HttpRequest
from Illuminate.http_response import HttpResponse


class FrameworkServiceProvider:
    def __init__(self, app) -> None:
        self.__app = app

    def register(self):
        print("registering framework")

    def boot(self):
        self.__app.bind("request", lambda: HttpRequest(self.__app))
        self.__app.bind("response", lambda: HttpResponse(self.__app))
