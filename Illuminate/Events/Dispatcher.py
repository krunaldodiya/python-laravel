import inspect

from typing import Any, Dict


class Dispatcher:
    def __init__(self, app) -> None:
        self.__app = app
        self.__listeners: Dict[Any, Any] = {}

    def dispatch(self, event, args={}):
        callbacks = self.__listeners.get(event, [])

        for callback in callbacks:
            self.handle_callback(callback, event, args)

    def handle_callback(self, callback, event, args):
        if inspect.isclass(callback):
            callback(**args).handle(event)
        else:
            callback(**args)

    def listen(self, event, callback):
        self.__listeners.setdefault(event, [])

        self.__listeners[event].append(callback)
