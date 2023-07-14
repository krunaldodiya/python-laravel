from Illuminate.template import Template


class ViewServiceProvider:
    def __init__(self, app) -> None:
        self.__app = app

    def register(self):
        self.__app.singleton("view", lambda: Template(self.__app))

    def boot(self):
        pass
