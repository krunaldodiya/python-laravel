from Illuminate.Foundation.Http.Kernel import Kernel as HttpKernel
from app.Http.Middleware.Authenticate import Authenticate


class Kernel(HttpKernel):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.middleware = []

        self.middleware_groups = {
            "web": [],
            "api": [],
        }

        self.middleware_aliases = {
            "auth": Authenticate,
        }
