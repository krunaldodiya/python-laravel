from Illuminate.Contracts.Http.Request import Request


class RequestReceived:
    def __init__(self, request: Request):
        self.request = request
