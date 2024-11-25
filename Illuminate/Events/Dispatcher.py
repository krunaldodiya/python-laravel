import inspect

from typing import Any, Dict
from Illuminate.Support.helpers import is_class, is_class_instance


class Dispatcher:
    def __init__(self, app) -> None:
        self.__app = app
        self.__listeners: Dict[Any, Any] = {}

    def dispatch(self, event, args=[]):
        event_name = self.parse_event_name(event)

        callbacks = self.__listeners.get(event_name, [])

        for callback in callbacks:
            self.handle_callback(callback, event, args)

    def listen(self, event, callback):
        event_name = self.parse_event_name(event)

        self.__listeners.setdefault(event_name, [])

        self.__listeners[event_name].append(callback)

    def handle_callback(self, callback, event, args):
        if inspect.isclass(callback):
            callback(*args).handle(event)
        else:
            callback(*args)

    def parse_event_name(self, event):
        if isinstance(event, str):
            return event

        if is_class(event):
            return event.__name__

        if is_class_instance(event):
            return event.__class__.__name__

        raise Exception("Invalid event name", event)
