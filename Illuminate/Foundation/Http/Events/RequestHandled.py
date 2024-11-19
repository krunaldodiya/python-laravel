from Illuminate.Contracts.Http.Request import Request
from Illuminate.Contracts.Http.Response import Response


class RequestHandled:
    def __init__(self, request: Request, response: Response):
        self.request = request
        self.response = response
