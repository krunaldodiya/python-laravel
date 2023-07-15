from datetime import time
from typing import Callable, List, Tuple
from Illuminate.file_loader import load_files
from Illuminate.http_response import HttpResponse


ResponseHandler = Callable[[str, List[Tuple]], None]


def response_handler(environ: dict, start_response: ResponseHandler):
    from wsgi import application

    application.bind("start_time", time())
    application.bind("environ", environ)

    _ = application.make("request")
    response = application.make("response")

    start_response(
        response.get_status_code(),
        response.get_headers(),
    )

    return iter([response.get_response_content()])
