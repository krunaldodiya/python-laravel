from typing import Callable, List, Tuple
from Illuminate.file_loader import load_files
from Illuminate.http_response import HttpResponse


ResponseHandler = Callable[[str, List[Tuple]], None]


def response_handler(environ: dict, start_response: ResponseHandler):
    from wsgi import application

    response = application.resolve("response")

    print(response)

    # request = self.resolve("request")

    # load_files("routes")

    # request.initialize(environ)

    # http_response: HttpResponse = self.make_response()

    # start_response(http_response.status, http_response.response_headers)

    # return [http_response.response_body]
