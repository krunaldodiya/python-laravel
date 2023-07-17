from Illuminate.Pipeline.Pipeline import Pipeline


pipeline = Pipeline("app")


def eat(name, next):
    print(f"eat: {name}")
    return next


def sleep(name, next):
    print(f"sleep: {name}")
    return next


pipeline.send("krunal").through([eat, sleep]).then_return()
