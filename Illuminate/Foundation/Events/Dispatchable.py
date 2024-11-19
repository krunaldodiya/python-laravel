from Illuminate.Collections.helpers import event


class Dispatchable:
    @classmethod
    def dispatch(cls, *args, **kwargs):
        return event(cls(*args, **kwargs))
