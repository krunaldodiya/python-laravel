from Illuminate.Contracts.Http.Kernel import Kernel

from Illuminate.Http.Request import Request

from Illuminate.Http.ResponseFactory import ResponseFactory
from Illuminate.Support.Facades.Log import Log

from app.Http.Kernel import Kernel as HttpKernel

from bootstrap.app import app

kernel: HttpKernel = app.make(Kernel, {"app": app, "router": app.make("router")})

request: Request = Request.capture(app)

response: ResponseFactory = kernel.handle(request)

response.send()

kernel.terminate(request, response)

config = app.make("config")

Log.dd(config["app"])
