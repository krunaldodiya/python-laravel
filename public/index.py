from Illuminate.Contracts.Http.Kernel import Kernel

from Illuminate.Http.Request import Request

from Illuminate.Http.Response import Response

from app.Http.Kernel import Kernel as HttpKernel

from bootstrap.app import application

kernel: HttpKernel = application.make(
    Kernel, {"app": application, "router": application.make("router")}
)

request: Request = application.make("request")

response: Response = kernel.handle(request.capture()).send()

kernel.terminate(request, response)
