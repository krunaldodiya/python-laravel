from typing import Any

from Illuminate.Container.Container import Container


class Application(Container):
    def bind(self, *args, **kwargs) -> None:
        return super().bind(*args, **kwargs)

    def singleton(self, *args, **kwargs) -> None:
        return super().singleton(*args, **kwargs)

    def make(self, *args, **kwargs) -> Any:
        return super().make(*args, **kwargs)


class Test:
    def __init__(self, name) -> None:
        self.name = name


app = Application()

router = app.bind("router", lambda: "test")

router = app.make("router")

print("router", router)
