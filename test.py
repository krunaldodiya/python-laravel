from typing import Any, Dict
from Illuminate.Container.Container import Container


class World:
    def __init__(self) -> None:
        pass


class Hello:
    def __init__(self) -> None:
        pass


class Application(Container):
    def bind(self, key: str, binding_resolver: Any) -> None:
        return super().bind(key, binding_resolver)

    def singleton(self, key: str, binding_resolver: Any) -> None:
        return super().singleton(key, binding_resolver)

    def make(self, key: str, make_args: Dict[str, Any] = ...) -> Any:
        return super().make(key, make_args)

    def instance(self, key, instance):
        return super().instance(key, instance)


if __name__ == "__main__":
    app = Application()

    hello = app.make(Hello)

    print(hello)
