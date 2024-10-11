from Illuminate.Contracts.Foundation.Application import Application
from Illuminate.Http.ServerBag.WSGIServer import WSGIServer


class Request:
    def __init__(self, app: Application) -> None:
        self.app = app

        self.server = app.make("server")

        self.router = self.app.make("router")

        self.__dict__.update(self.server.__dict__)

    def __getattr__(self, name):
        return getattr(self.server, name)

    def __getitem__(self, key):
        return self.server[key]

    @staticmethod
    def capture(app):
        return Request.create_from_base(app)

    @staticmethod
    def create_from_base(app):
        server = WSGIServer.get_server()

        return Request.create_from(app, server)

    @staticmethod
    def create_from(app, server):
        app.instance("server", server)

        return Request(app)

    def get_params(self):
        return self.router.current_route.params

    def param(self, name):
        params = self.get_params()

        return params.get(name, None)
