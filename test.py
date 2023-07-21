from Illuminate.Foundation.Application import Application


app = Application()

test = app.instance("test", "hello")
another = app.make("test")

print(test)
print(another)
