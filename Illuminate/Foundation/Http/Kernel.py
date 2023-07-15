from Illuminate.Foundation.Application import Application
from Illuminate.Http.Request import Request
from Illuminate.Http.Response import Response
from Illuminate.Routing.Router import Router


class Kernel:
    def __init__(self, app: Application, router: Router) -> None:
        self.__app = app
        self.__router = router

    def handle(self, request: Request) -> Response:
        response = self.__app.make("response")

        return response
