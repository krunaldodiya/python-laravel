import inspect
import types
from typing import Callable


class Dispatcher:
    def __init__(self, app) -> None:
        self.__app = app
        self.__listeners = {}

    def dispatch(self, event, args={}):
        callbacks = self.__listeners.get(event, [])

        for callback in callbacks:
            self.handle_callback(callback, event, args)

    def handle_callback(self, callback, event, args):
        if isinstance(callback, types.FunctionType):
            callback(event)
        elif inspect.isclass(callback):
            callback(**args).handle(event)
        else:
            return "Unknown type"

    def listen(self, event, callback):
        self.__listeners[event] = []

        self.__listeners[event].append(callback)
