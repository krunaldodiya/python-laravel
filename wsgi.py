from Illuminate.Http.ServerBag.WSGIServer import WSGIServer


def main(environ, start_response):
    if environ.get("HTTP_REFERER"):
        return []

    WSGIServer.create_server(environ, start_response)

    from public.index import response

    return response
