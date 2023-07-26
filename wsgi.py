import sys

from importlib import import_module

from Illuminate.Http.ServerBag.WSGIServer import WSGIServer

from werkzeug.middleware.shared_data import SharedDataMiddleware


def clear_module_cache(module_name):
    if module_name in sys.modules:
        del sys.modules[module_name]


class WSGIApplication:
    def __init__(self) -> None:
        from bootstrap.app import app

        self.public_path = app.public_path()

        self.events = app.make("events")

        self.response = None

    def __call__(self, environ, start_response):
        try:
            clear_module_cache("public.index")

            WSGIServer.create_server(environ, start_response)

            self.events.listen(
                "response_sent",
                lambda response: self.on_response(response, start_response),
            )

            import_module("public.index")
        finally:
            return self.response

    def on_response(self, response, start_response):
        start_response(response.get_status_code(), response.get_headers())

        self.response = [response.get_content().encode("utf-8")]


app = WSGIApplication()

app = SharedDataMiddleware(app, {"/": str(app.public_path)})
