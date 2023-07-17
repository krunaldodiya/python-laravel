class Pipeline:
    def __init__(self, app) -> None:
        self.__app = app
        self.__passable = None
        self.__pipes = []
        self.__destination = None
        self.__output = None

    def send(self, passable):
        self.__passable = passable

        return self

    def through(self, pipes):
        self.__pipes = pipes

        for current_index, current_pipe in enumerate(self.__pipes):
            try:
                next_pipe = self.__get_next_pipe(current_index)

                output = current_pipe(self.__passable, next_pipe)

                if output and output != next_pipe:
                    self.__output = output
            except Exception as e:
                raise Exception(e)

        return self

    def then(self, destination: callable):
        self.__destination = destination

        return self.__destination(self.__output)

    def then_return(self):
        return self.__output

    def __get_next_pipe(self, current_index):
        if current_index + 1 == len(self.__pipes):
            return None
        else:
            return self.__pipes[current_index]
