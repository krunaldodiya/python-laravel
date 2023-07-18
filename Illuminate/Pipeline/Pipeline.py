from functools import reduce


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

    def through(self, pipes):
        self.__pipes = pipes

        reduce(self.__manage_pipe, self.__pipes, True)

        return self

    def then(self, destination: callable):
        return destination(self.__output)

    def then_return(self):
        return self.then(lambda passable: self.__output)

    def __manage_pipe(self, should_continue, current_pipe):
        if should_continue:
            next_index = self.__current_index + 1

            if next_index == len(self.__pipes):
                next_pipe = lambda name: self.__output
            else:
                next_pipe = lambda name: self.__pipes[next_index]

            output = current_pipe(self.__passable, next_pipe)

            if callable(output):
                self.__current_index = next_index

                return True

            self.__output = output

        return False
