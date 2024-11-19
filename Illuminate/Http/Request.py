from typing import Any, Dict, Self
from Illuminate.Collections.helpers import collect
from Illuminate.Contracts.Foundation.Application import Application
from Illuminate.Http.Concerns.InteractsWithContentTypes import InteractsWithContentTypes
from Illuminate.Http.ServerBag.WSGIServer import WSGIServer
from Illuminate.Http.RequestAdapter import RequestAdapter
from Illuminate.Http.WSGIRequestAdapter import WSGIRequestAdapter
from Illuminate.Routing.Route import Route


class Request(InteractsWithContentTypes):
    def __init__(self, app: Application) -> None:
        self.app = app

        self.request_adapter: RequestAdapter = app.make("request_adapter")

        self.router = self.app.make("router")

    @classmethod
    def capture(cls, app):
        return cls.create_from_base(app)

    @classmethod
    def create_from_base(cls, app):
        server = WSGIServer.get_server()

        request_adapter = WSGIRequestAdapter(server)

        return cls.create_from(app, request_adapter)

    @classmethod
    def create_from(cls, app: Application, request_adapter: RequestAdapter):
        app.instance("request_adapter", request_adapter)

        return cls(app)

    def set_route_resolver(self, route_resolver) -> Self:
        self.route_resolver = route_resolver

        return self

    def current_route(self) -> Route:
        return self.router.current_route

    def get_route_params(self):
        current_route = self.current_route()

        return current_route.route_params

    def route_param(self, name, default=None):
        params = self.get_route_params()

        return params.get(name, default)

    def query_param(self, name, default=None):
        query = self.query()

        return query.get(name, default)

    def segment(self, number=1):
        if number < 1:
            raise None

        segments = self.segments()

        return segments.get(number - 1)

    def segments(self):
        url = self.get_url().strip("/")

        return collect(url.split("/") if isinstance(url, str) else [])

    def get_input_source(self) -> Dict[Any, Any]:
        if self.is_json():
            return self.json()

        method = self.get_method()

        if method in ["GET", "HEAD"]:
            return self.query()

        return self.form()

    def input(self) -> Dict[Any, Any]:
        get_input_source_data = self.get_input_source()

        query_data = self.query()

        data = {**get_input_source_data, **query_data}

        return data

    def all(self) -> Dict[Any, Any]:
        input_data = self.input()

        all_files_data = self.all_files()

        data = {**input_data, **all_files_data}

        return data

    def header(self, key) -> Any:
        return self.headers().get(key)

    def session(self, key) -> Any:
        return self.sessions().get(key)

    def cookie(self, key) -> Any:
        return self.cookies().get(key)

    def get_url(self) -> str:
        return self.request_adapter.get_url()

    def get_full_url(self) -> str:
        return self.request_adapter.get_full_url()

    def get_method(self) -> str:
        return self.request_adapter.get_method()

    def user(self) -> Any:
        return self.request_adapter.get_user()

    def json(self) -> Dict[Any, Any]:
        return self.request_adapter.json_data()

    def query(self) -> Dict[Any, Any]:
        return self.request_adapter.query_data()

    def post(self) -> Dict[Any, Any]:
        return self.request_adapter.post_data()

    def form(self) -> Dict[Any, Any]:
        return self.request_adapter.form_data()

    def all_files(self) -> Dict[Any, Any]:
        return self.request_adapter.files_data()

    def headers(self) -> Dict[Any, Any]:
        return self.request_adapter.headers_data()

    def sessions(self) -> Dict[Any, Any]:
        return self.request_adapter.sessions_data()

    def cookies(self) -> Dict[Any, Any]:
        return self.request_adapter.cookies_data()
