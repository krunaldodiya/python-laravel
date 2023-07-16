from public.server import Server


class Request:
    def __init__(self, app) -> None:
        self.__app = app
        self.__server: Server = None

    @property
    def server(self):
        return self.__server

    def set_params(self, params):
        self.params = params

    def get(self, param):
        return self.params.get(param)

    def capture(self, server: Server):
        self.__server = server
