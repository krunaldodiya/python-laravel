from Illuminate.Pipeline.Pipeline import Pipeline


pipeline = Pipeline("app")


def one(name, next):
    try:
        print("one")
        return next(name)
    except Exception as e:
        print("one", e)


def two(name, next):
    try:
        print("two")
        return next(name)
    except Exception as e:
        print("two", e)


def three(name, next):
    try:
        print("three")
        return next(name)
    except Exception as e:
        print("three", e)


output = pipeline.send("krunal").through([one, two, three]).then_return()

print(output)
