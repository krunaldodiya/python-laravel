from typing import Any
from Illuminate.Container.Container import Container


class Application(Container):
    def bind(self, *args, **kwargs) -> None:
        return super().bind(*args, **kwargs)

    def singleton(self, *args, **kwargs) -> None:
        return super().singleton(*args, **kwargs)

    def make(self, *args, **kwargs) -> Any:
        return super().make(*args, **kwargs)


class Hello:
    pass


class Router:
    pass


app = Application()

# app.bind("router", Router)
app.bind("router", lambda: Router())

hello = app.make(Hello)
router = app.make("router")

print(hello)
print(router)
