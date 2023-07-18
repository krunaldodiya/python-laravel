class Dispatcher:
    def __init__(self, app) -> None:
        self.__app = app
        self.__listeners = {}

    def dispatch(self, event):
        callbacks = self.__listeners.get(event)

        for callback in callbacks:
            callback()

    def listen(self, event, callback):
        self.__listeners[event] = []

        self.__listeners[event].append(callback)
