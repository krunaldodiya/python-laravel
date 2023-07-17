from public.server import Server


async def main(scope, receive, send):
    assert scope["type"] == "http"

    from public.index import application, kernel

    application.bind("server", lambda: Server(scope, receive, send))

    await application.run_kernel(kernel)
