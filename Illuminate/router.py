class Router:
    def __init__(self) -> None:
        self.routes = []

    def get(self, route, handler):
        self.make(route, handler, "GET")

    def post(self, route, handler):
        self.make(route, handler, "POST")

    def __parse_handler(self, handler):
        if callable(handler):
            return {
                "callable": True,
                "action": handler,
                "module_path": None,
                "module_name": None,
                "action_name": None,
            }

        if isinstance(handler, list):
            module, method = handler

            if (
                len(handler) == 2
                and module.__module__.startswith("app.Http.Controllers")
                and isinstance(handler[1], str)
            ):
                return {
                    "callable": False,
                    "action": None,
                    "module_path": module.__module__,
                    "module_name": module.__name__,
                    "action_name": method,
                }

        raise Exception("Invalid route")

    def make(self, route, handler, requested_method):
        handler_data = self.__parse_handler(handler)

        data = {
            "path": route,
            "request_method": requested_method,
            **handler_data,
        }

        self.routes.append(data)
