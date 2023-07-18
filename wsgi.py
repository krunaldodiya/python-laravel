from importlib import import_module

from Illuminate.Http.ServerBag import ServerBag

from Illuminate.Http.ResponseFactory import ResponseFactory
from Illuminate.Support.Facades.App import App


async def main(scope, receive, send):
    assert scope["type"] == "http"

    server: ServerBag = App.instance("server", ServerBag(scope, receive, send))

    import_module("public.index")

    response: ResponseFactory = App.make("response")

    await response.send_async(server)
