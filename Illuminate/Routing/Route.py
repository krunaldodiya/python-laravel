from typing import Any, Dict

from Illuminate.Routing.Controllers.HasMiddleware import Middleware


class Route:
    def __init__(
        self,
        router,
        methods,
        uri,
        action,
    ) -> None:
        self.__router = router

        self.__name: str = self.__router.attributes.get("name", None)

        self.__alias: str = self.__router.attributes.get("as", None)

        self.__prefix: str = self.__router.attributes.get("prefix", None)

        self.__middleware = self.__router.attributes.get("middleware", [])

        self.__computed_middleware = None

        self.__uri = f"{self.prefix.strip('/')}/{uri}" if self.prefix else uri

        self.__action = action

        self.__methods = methods

        self.__params = {}

    @property
    def name(self):
        return self.__name

    @property
    def alias(self):
        return self.__alias

    @property
    def prefix(self):
        return self.__prefix

    @property
    def middleware(self):
        return self.__middleware

    @property
    def computed_middleware(self):
        return self.__computed_middleware

    @property
    def uri(self):
        return self.__uri

    @property
    def action(self):
        return self.__action

    @property
    def methods(self):
        return self.__methods

    @property
    def params(self):
        return self.__params

    @property
    def router(self):
        return self.__router

    def run(self):
        action = None

        type = self.action.get("type")

        if type in ["controller", "callable"]:
            action = self.__run_controller()
        else:
            action = self.__run_callable()

        if not action:
            raise Exception("Invalid route action")

        dependencies = self.router.app.get_dependencies(action)

        return action(**dependencies)

    def __run_controller(self):
        controller_object = self.router.app.make(self.action["controller_class"])

        return getattr(controller_object, self.action["controller_action"])

    def __run_callable(self):
        return self.action["uses"]

    def gather_middleware(self):
        if not self.__computed_middleware:
            controller_middleware = self.__controller_middleware()

            self.__computed_middleware = self.__middleware + controller_middleware

        return self.__computed_middleware

    def __controller_middleware(self):
        controller_class = self.action.get("controller_class")

        controller_action = self.action.get("controller_action")

        middleware_method = getattr(controller_class, "middleware", lambda: [])

        middleware = [
            (
                middleware
                if isinstance(middleware, Middleware)
                else Middleware(middleware)
            )
            for middleware in middleware_method()
        ]

        return [
            middleware.name
            for middleware in middleware
            if middleware.filter(controller_action)
        ]

    def set_params(self, params: Dict[str, Any]):
        self.__params = params

        return self
