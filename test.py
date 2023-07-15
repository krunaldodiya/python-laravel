# from container import Container


import inspect
from Illuminate.Support.Foundation.Container import Container


app = Container()


class World:
    def __init__(self) -> None:
        self.greet = "hello world"


class Hello:
    def __init__(self, name: str, world: World) -> None:
        self.name = name
        self.world = world


class Test:
    def __init__(self, hello: Hello) -> None:
        self.hello = hello


# app.bind(Hello, lambda: {"name": "krunal", "world": app.make(World)})

test = app.make(Test)

print(test)
