from Illuminate.Contracts.Foundation.Application import Application
from Illuminate.Contracts.Http.Kernel import Kernel as HttpKernelContract
from Illuminate.Foundation.Bootstrap.RegisterProviders import RegisterProviders
from Illuminate.Foundation.Http.Kernel import Kernel as HttpKernel
from Illuminate.Contracts.Console.Kernel import Kernel as ConsoleKernelContract
from Illuminate.Foundation.Console.Kernel import Kernel as ConsoleKernel


class ApplicationBuilder:
    def __init__(self, application: Application):
        self.__application = application

    def with_routing(self):
        return self

    def with_middleware(self):
        return self

    def with_exceptions(self):
        return self

    def with_kernels(self):
        self.__application.singleton(HttpKernelContract, HttpKernel)
        self.__application.singleton(ConsoleKernelContract, ConsoleKernel)

        return self

    def with_events(self):
        return self

    def with_commands(self):
        return self

    def with_providers(self, providers=[]):
        RegisterProviders.merge(providers)

        return self

    def create(self):
        return self.__application
