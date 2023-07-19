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
