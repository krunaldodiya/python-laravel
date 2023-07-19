from Illuminate.Http.Request import Request
from Illuminate.Routing.RouteCollection import RouteCollection


class UrlGenerator:
    def __init__(
        self, routes: RouteCollection, request: Request, asset_url: str
    ) -> None:
        self.__routes = routes
        self.__request = request
        self.__asset_url = asset_url
