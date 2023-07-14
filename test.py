from Illuminate.Support.Foundation.Container import Container


class Application(Container):
    pass


app = Application()


class World:
    def __init__(self) -> None:
        self.name = "hello world"


class Hello:
    def __init__(self, world: World) -> None:
        self.world = world


class Test:
    def __init__(self, name: str, hello: Hello) -> None:
        self.name = name
        self.hello = hello


test = app.make(Test, {"hello": app.make(Hello)})
print(test)
