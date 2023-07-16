from Illuminate.Foundation.Http.Kernel import Kernel as HttpKernel
from Illuminate.Http.Middleware.HandleCors import HandleCors
from app.Http.Middleware.Authenticate import Authenticate


class Kernel(HttpKernel):
    middleware = [
        HandleCors,
    ]

    middleware_groups = {
        "web": [],
        "api": [],
    }

    middleware_aliases = {
        "auth": Authenticate,
    }
