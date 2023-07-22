from typing import Any, Dict
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

app.bind(Test, lambda app, data: Test(data["name"]))

test = app.make(Test, {"name": "krunal"})

print(test)
