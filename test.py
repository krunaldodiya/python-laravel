from Illuminate.Support.Foundation.Container import Container


class Application(Container):
    pass


app = Application()


class World:
    def __init__(self) -> None:
        self.greet = "hello world"


class Hello:
    def __init__(self, world: World) -> None:
        self.world = world


class Test:
    def __init__(self, hello: Hello) -> None:
        self.hello = hello


test = app.make(Test, {"hello": app.make(Hello)})

print(test.hello.world.greet)
