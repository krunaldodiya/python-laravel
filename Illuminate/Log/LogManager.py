from Illuminate.Log.Logger import Logger


class LogManager:
    def __init__(self, app) -> None:
        self.__app = app
        self.__logger = Logger(self.__app)

    def log(self, info) -> None:
        return self.__logger.log(info)

    def dd(self, info) -> None:
        return self.__logger.dd(info)
