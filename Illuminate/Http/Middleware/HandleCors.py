from typing import Any


class HandleCors:
    def handle(self, request, next) -> Any:
        return next(request)
