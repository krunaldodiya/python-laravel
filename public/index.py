from Illuminate.Contracts.Http.Kernel import Kernel

from Illuminate.Http.Request import Request

from Illuminate.Http.ResponseFactory import ResponseFactory

from app.Http.Kernel import Kernel as HttpKernel

from bootstrap.app import app

kernel: HttpKernel = app.make(Kernel)

request: Request = Request.capture()

response: ResponseFactory = kernel.handle(request).send()

kernel.terminate(request, response)
