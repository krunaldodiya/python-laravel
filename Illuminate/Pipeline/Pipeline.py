from functools import reduce
import inspect


class Pipeline:
    def __init__(self, app) -> None:
        self.__app = app
        self.__passable = None
        self.__method = "handle"
        self.__pipes = []
        self.__output = None
        self.__current_index = 0

    def send(self, passable):
        self.__passable = passable

        return self

    def via(self, method):
        self.__method = method

        return self

    def pipe(self, pipe):
        self.__pipes.append(pipe)

        return self

    def through(self, pipes):
        self.__pipes = pipes

        reduce(self.__resolve_pipe, self.__pipes, True)

        return self

    def pipes(self):
        return self.__pipes

    def then(self, destination: callable):
        return destination(self.__output)

    def then_return(self):
        return self.then(lambda passable: self.__output)

    def __resolve_pipe(self, should_continue, current_pipe):
        caller = None

        if inspect.isclass(current_pipe):
            object = self.__app.make(current_pipe)
            caller = self.__get_caller(object)
        elif callable(current_pipe):
            caller = current_pipe
        else:
            caller = self.__get_caller(current_pipe)

        should_continue = should_continue and caller is not None

        self.__manage_pipe(should_continue, caller)

    def __get_caller(self, obj):
        if hasattr(obj, "handle"):
            return getattr(obj, "handle")
        else:
            return getattr(obj, "__call__")

    def __manage_pipe(self, should_continue, current_pipe):
        if should_continue:
            pipes = self.pipes()

            next_index = self.__current_index + 1

            if next_index == len(pipes):
                next_pipe = lambda name: self.__output
            else:
                next_pipe = lambda name: pipes[next_index]

            output = current_pipe(self.__passable, next_pipe)

            if callable(output):
                self.__current_index = next_index

                return True

            self.__output = output

        return False
