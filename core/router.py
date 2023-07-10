class Router:
    def __init__(self) -> None:
        self.routes = []

    def get(self, route, handler):
        if callable(handler):
            self.routes.append(
                {
                    "path": route,
                    "method": "GET",
                    "controller": None,
                    "method": handler,
                }
            )
        else:
            if not len(handler) == 2:
                raise Exception("Invalid route")

            controller, method = handler

            self.routes.append(
                {
                    "path": route,
                    "method": "GET",
                    "controller": controller,
                    "method": method,
                }
            )
