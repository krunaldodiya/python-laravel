from Illuminate.Contracts.Http.Kernel import Kernel
from app.Http.Kernel import Kernel as HttpKernel

from bootstrap.app import application

kernel: HttpKernel = application.make(
    Kernel, {"app": application, "router": application.make("router")}
)

request = application.make("request")

response = kernel.handle(request.capture()).send()

kernel.terminate(request, response)
