from Illuminate.Contracts.Http.Kernel import Kernel
from Illuminate.Contracts.Http.Response import Response
from Illuminate.Http.Request import Request
from app.Http.Kernel import Kernel as HttpKernel
from bootstrap.app import app

kernel: HttpKernel = app.make(Kernel)

request: Request = Request.capture(app)

response: Response = kernel.handle(request)

kernel.terminate(request, response)
