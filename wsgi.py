import sys

from Illuminate.Http.ServerBag.WSGIServer import WSGIServer

from werkzeug.middleware.shared_data import SharedDataMiddleware


def clear_module_cache(module_name):
    if module_name in sys.modules:
        del sys.modules[module_name]


class WSGIApplication:
    def __init__(self) -> None:
        from bootstrap.app import app

        self.public_path = app.public_path()

    def __call__(self, environ, start_response):
        clear_module_cache("public.index")

        WSGIServer.create_server(environ, start_response)

        from public.index import response

        return response


app = WSGIApplication()

app = SharedDataMiddleware(app, {"/": str(app.public_path)})
