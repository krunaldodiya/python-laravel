from Illuminate.Support.Foundation.Application import Application
from solar import Solar

app = Application()


class Hello:
    def __init__(self) -> None:
        self.name = "hello"


class Test:
    def __init__(self, name: str, hello: Hello) -> None:
        self.name = name
        self.hello = hello


app.singleton("test", lambda: Test("krunal", Hello()))

solar = app.make(Solar)

print(solar)
