from importlib import import_module
from Illuminate.Http.ResponseFactory import ResponseFactory
from Illuminate.Support.Facades.App import App
from public.server import Server


async def main(scope, receive, send):
    assert scope["type"] == "http"

    App.bind("server", lambda: Server(scope, receive, send))

    import_module("public.index")

    response: ResponseFactory = App.make("response")

    await response.send_async()
