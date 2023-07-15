from Illuminate.Contracts.Http.Kernel import Kernel

from Illuminate.Foundation.Application import Application

from app.Http.Kernel import Kernel as HttpKernel

application: Application = Application()

application.singleton(Kernel, HttpKernel)
