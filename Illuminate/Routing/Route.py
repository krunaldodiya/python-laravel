from typing import Any, Dict


class Route:
    def __init__(self, attributes: Dict[str, Any], methods, uri, action) -> None:
        self.__name: str = attributes.get("name", "")

        self.__as: str = attributes.get("as", "")

        self.__prefix: str = attributes.get("prefix", "")

        self.__middleware = attributes.get("middleware", [])

        self.__computed_middleware = None

        self.__methods = methods

        self.__uri = f"{self.__prefix.strip('/')}/{uri}" if self.__prefix else uri

        self.__action = action

        self.__router = None

        self.__app = None

        self.__params = {}

    @property
    def params(self):
        return self.__params

    @property
    def methods(self):
        return self.__methods

    @property
    def uri(self):
        return self.__uri

    @property
    def action(self):
        return self.__action

    @property
    def middleware(self):
        return self.__middleware

    def set_router(self, router):
        self.__router = router
        return self

    def set_application(self, app):
        self.__app = app
        return self

    def run(self):
        action = None

        type = self.action.get("type")

        if type == "controller":
            action = self.__run_controller()
        else:
            action = self.__run_callable()

        if not action:
            raise Exception("Invalid route action")

        dependencies = self.__app.get_dependencies(action)

        return action(**dependencies)

    def __get_controller(self):
        return self.__app.make(self.action["controller_class"])

    def __run_controller(self):
        controller_object = self.__get_controller()

        return getattr(controller_object, self.action["controller_action"])

    def __run_callable(self):
        return self.action["uses"]

    def gather_middleware(self):
        if not self.__computed_middleware:
            self.__computed_middleware = (
                self.__middleware + self.__controller_middleware()
            )

        return self.__computed_middleware

    def __controller_middleware(self):
        type = self.action.get("type")

        if not type == "controller":
            return []

        controller_object = self.__get_controller()

        return getattr(controller_object, "middleware", [])

    def set_params(self, params: Dict[str, Any]):
        self.__params = params

        return self
