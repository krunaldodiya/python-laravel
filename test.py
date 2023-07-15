# from container import Container


import inspect
import random
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


class Singleton:
    def __init__(self) -> None:
        self.random = random.randint(0, 100)


app.bind(Hello, lambda: Hello("krunal", app.make(World)))

s1 = app.make(Singleton)
s2 = app.make(Singleton)

print(s1 == s2)
