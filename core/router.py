class Router:
    def __init__(self) -> None:
        self.routes = []

    def get(self, route, handler):
        self.routes.append(
            {
                "path": route,
                "method": "GET",
                "handler": handler,
            }
        )
