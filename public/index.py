from Illuminate.Contracts.Http.Kernel import Kernel

from Illuminate.Http.Request import Request

from Illuminate.Http.ResponseFactory import ResponseFactory

from app.Http.Kernel import Kernel as HttpKernel

from bootstrap.app import app


class Test:
    pass


app.singleton("test", lambda app: Test())

test = app.make("test")

print(test)

# kernel: HttpKernel = app.make(Kernel, {"router": app.make("router")})

# request: Request = Request.capture()

# response: ResponseFactory = kernel.handle(request).send()

# kernel.terminate(request, response)
