from Illuminate.Http.Request import Request
from Illuminate.Routing.RouteCollection import RouteCollection


class UrlGenerator:
    def __init__(
        self, routes: RouteCollection, request: Request, asset_root: str
    ) -> None:
        self._routes = routes
        self._asset_root = asset_root
        self._request = None

        self.set_request(request)

    def set_request(self, request: Request):
        self._request = request
