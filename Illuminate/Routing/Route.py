from importlib import import_module


class Route:
    def __init__(self, methods, uri, action) -> None:
        self.__methods = methods
        self.__uri = uri
        self.__action = action

        self.__router = None
        self.__app = None

    @property
    def methods(self):
        return self.__methods

    @property
    def uri(self):
        return self.__uri

    @property
    def action(self):
        return self.__action

    def set_router(self, router):
        self.__router = router
        return self

    def set_application(self, app):
        self.__app = app
        return self

    def run(self):
        if self.action.get("controller_action"):
            return self.__run_controller()
        else:
            return self.__run_callable()

    def __run_callable(self):
        return self.action["uses"](self.__router.current_request)

    def __run_controller(self):
        controller_module = import_module(
            self.action["controller_module"], package=None
        )

        controller_class = getattr(controller_module, self.action["controller_name"])

        controller_object = self.__app.make(controller_class)

        controller_action = getattr(controller_object, self.action["controller_action"])

        return controller_action(self.__router.current_request)
