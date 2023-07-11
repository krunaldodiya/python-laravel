class Controller:
    def __init_subclass__(cls) -> None:
        cls.app.singleton(cls.__name__, lambda _: cls())
