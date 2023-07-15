from importlib import import_module

from Illuminate.Foundation.Application import Application


class App:
    def __init__(self) -> None:
        self.__application = None

    def __call__(self, environ, start_response):
        self.__application = Application(environ, start_response)

        import_module("public.index")

        return ["test".encode("utf-8")]

    def get_application(self):
        return self.__application


app = App()
