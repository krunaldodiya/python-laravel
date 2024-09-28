from collections.abc import Callable
from typing import Any
from Illuminate.Contracts.Foundation.Application import Application
from Illuminate.Contracts.Http.Request import Request


class HandlePrecognitiveRequests:
    def __init__(self, app: Application) -> None:
        self.__app = app

    def handle(self, request: Request, next: Callable[[Any], Any]):
        return next(request)
