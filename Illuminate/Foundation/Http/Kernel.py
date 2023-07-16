from typing import TYPE_CHECKING, Type

from Illuminate.Http.Request import Request
from Illuminate.Http.Response import Response


if TYPE_CHECKING:
    from Illuminate.Foundation.Application import Application
    from Illuminate.Routing.Router import Router


class Kernel:
    def __init__(self, app: Type["Application"], router: Type["Router"]) -> None:
        self.__app = app
        self.__router = router

    def handle(self, request: Request) -> Response:
        response = self.__app.make("response")

        return response

    def terminate(self, request: Request, response: Response):
        print("terminating request")
