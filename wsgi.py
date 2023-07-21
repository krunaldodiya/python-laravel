import sys

from Illuminate.Http.ServerBag.WSGIServer import WSGIServer


def clear_module_cache(module_name):
    if module_name in sys.modules:
        del sys.modules[module_name]


def main(environ, start_response):
    clear_module_cache("public.index")

    WSGIServer.create_server(environ, start_response)

    from public.index import response

    return response
