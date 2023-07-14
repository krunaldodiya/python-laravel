from Illuminate.Environment.LoadEnvironment import LoadEnvironment
from Illuminate.Support.Foundation.response_handler import response_handler
from Illuminate.router import Router


class Kernel:
    def __init__(self, app) -> None:
        self.__app = app

    def register(self) -> None:
        self.load_environment()
        self.register_framework()

    def load_environment(self) -> None:
        LoadEnvironment()

    def register_framework(self) -> None:
        self.__app.set_response_handler(response_handler)
        self.__app.singleton("router", lambda: Router())
