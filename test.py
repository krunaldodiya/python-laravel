from Illuminate.Support.Foundation.Application import Application

app = Application()


class Test:
    def __init__(self, name) -> None:
        self.name = name


app.singleton("test", Test)

test = app.make("test", [{"name": "krunal"}])

print(test.name)
