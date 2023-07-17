from public.server import Server


async def send_response(scope, receive, send, response):
    status = response["status"]
    headers = response["headers"]
    body = response["body"]

    await send(
        {
            "type": "http.response.start",
            "status": status,
            "headers": headers,
        }
    )

    await send(
        {
            "type": "http.response.body",
            "body": body,
        }
    )


async def main(scope, receive, send):
    assert scope["type"] == "http"

    from public.index import application, kernel

    application.bind(
        "server",
        lambda: Server(
            scope,
            receive,
            send,
            lambda response: send_response(scope, receive, send, response),
        ),
    )

    await application.run_kernel(kernel)
