from Illuminate.Foundation.Events.Dispatchable import Dispatchable
from Illuminate.Http.Request import Request


class Routing(Dispatchable):
    def __init__(self, request: Request):
        self.request = request
