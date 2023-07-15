from importlib import import_module
from Illuminate.Http.Request import Request

from Illuminate.Support.Facades.Response import Response

from Illuminate.Contracts.Http.Kernel import Kernel

from app.Http.Kernel import Kernel as HttpKernel

from bootstrap.app import application


class App:
    def __call__(self, environ, start_response):
        print("test")

        application.set_environ(environ)

        application.set_response_handler(start_response)

        kernel: HttpKernel = application.make(
            Kernel, {"app": application, "router": application.make("router")}
        )

        request: Request = application.make("request")

        response: Response = kernel.handle(request.capture()).send()

        return kernel.terminate(request, response)


app = App()
