from typing import Self
from Illuminate.Contracts.Foundation.Application import Application
from Illuminate.Http.ServerBag.WSGIServer import WSGIServer
from Illuminate.Http.RequestAdapter import RequestAdapter
from Illuminate.Routing.Route import Route


class Request:
    def __init__(self, app: Application) -> None:
        self.app = app

        self.request_adapter: RequestAdapter = app.make("request_adapter")

        self.request = self.request_adapter.request

        self.router = self.app.make("router")

        self.__dict__.update(self.request.__dict__)

    def __getattr__(cls, attribute, *args, **kwargs):
        return getattr(cls.request, attribute)

    def __getitem__(self, key):
        return self.request[key]

    @classmethod
    def capture(cls, app):
        return cls.create_from_base(app)

    @classmethod
    def create_from_base(cls, app):
        server = WSGIServer.get_server()

        return cls.create_from(app, server)

    @classmethod
    def create_from(cls, app: Application, request_adapter: RequestAdapter):
        app.instance("request_adapter", request_adapter)

        return cls(app)

    def current_route(self) -> Route:
        return self.router.current_route

    def get_route_params(self):
        current_route = self.current_route()

        return current_route.route_params

    def get_query_params(self):
        current_route = self.current_route()

        return current_route.query_params

    def route_param(self, name, default=None):
        params = self.get_route_params()

        return params.get(name, default)

    def query_param(self, name, default=None):
        query = self.get_query_params()

        return query.get(name, default)

    def get_url(self):
        return self.request_adapter.get_url()

    def get_full_url(self):
        return self.request_adapter.get_full_url()

    def set_route_resolver(self, route_resolver) -> Self:
        self.route_resolver = route_resolver

        return self
