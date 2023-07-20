import sys

from importlib import import_module

from Illuminate.Http.ServerBag.WSGIServer import WSGIServer

MODULE_NAME = "public.index"


def clear_module_cache(module_name):
    if module_name in sys.modules:
        del sys.modules[module_name]


def main(environ, start_response):
    clear_module_cache(MODULE_NAME)

    WSGIServer.create_server(environ, start_response)

    module = import_module(MODULE_NAME)

    response = getattr(module, "response")

    return response
