from importlib import import_module

from Illuminate.Http.ResponseFactory import ResponseFactory

from Illuminate.Http.ServerBag import ServerBag


async def main(scope, receive, send):
    assert scope["type"] == "http"

    from bootstrap.app import app

    server: ServerBag = app.instance("server", ServerBag(scope, receive, send))

    response: ResponseFactory = app.make("response")

    import_module("public.index")

    await response.send_async(server)
