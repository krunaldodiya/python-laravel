from public.server import Server


async def main(scope, receive, send):
    assert scope["type"] == "http"

    from public.index import application, kernel

    server = Server(scope, receive, send)

    await application.run_kernel(kernel, server)
