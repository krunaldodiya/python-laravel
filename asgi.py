from importlib import import_module

from Illuminate.Http.ResponseFactory import ResponseFactory

from Illuminate.Http.ServerBag.ASGIServer import ASGIServer


async def main(scope, receive, send):
    assert scope["type"] == "http"

    ASGIServer.init(scope, receive, send)

    from bootstrap.app import app

    response: ResponseFactory = app.make("response")

    import_module("public.index")

    await response.send_async()
