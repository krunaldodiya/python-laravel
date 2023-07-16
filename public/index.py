from Illuminate.Contracts.Http.Kernel import Kernel

from app.Http.Kernel import Kernel as HttpKernel

from bootstrap.app import application

kernel: HttpKernel = application.make(
    Kernel, {"app": application, "router": application.make("router")}
)
