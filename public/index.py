from Illuminate.Contracts.Http.Kernel import Kernel
from Illuminate.Http.Request import Request
from Illuminate.Http.ResponseFactory import ResponseFactory
from Illuminate.Support.Facades.Debug import Debug

from app.Http.Kernel import Kernel as HttpKernel

from bootstrap.app import application

kernel: HttpKernel = application.make(
    Kernel, {"app": application, "router": application.make("router")}
)

request: Request = Request.capture()

response: ResponseFactory = kernel.handle(request)

response.send()

Debug.dd(kernel.router)

kernel.terminate(request, response)
