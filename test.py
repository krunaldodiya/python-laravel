from Illuminate.Pipeline.Pipeline import Pipeline


pipeline = Pipeline("app")


def one(passable, next):
    try:
        return next(passable)
    except Exception as e:
        print("one", e)


def two(passable, next):
    try:
        return "two"
    except Exception as e:
        print("two", e)


def three(passable, next):
    try:
        return next(passable)
    except Exception as e:
        print("three", e)


def hello(output):
    return output


output = pipeline.send("krunal").through([one, two, three]).then_return()

print(output)
